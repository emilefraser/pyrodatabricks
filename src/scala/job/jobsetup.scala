package cloud.spark.util

import java.io.{File, FileNotFoundException}
import com.typesafe.config.{Config, ConfigFactory}
import org.apache.spark.sql.SparkSession
import org.apache.spark.SparkConf
import com.databricks.dbutils_v1.DBUtilsHolder.dbutils
import org.apache.spark.internal.Logging
import scala.io.Source

/**
 * Defines the main function for job execution
 *
 * @author Bijoy Chaudhury
 */
trait JobSetup extends Logging {

  def main(args: Array[String]) {
    logInfo(s" === Number of arguments passed: ${args.length}")
    args.foreach( arg => logInfo(s" === The passed arguments - $arg"))

    if( args.length > 0) {
      try {

        val configFile = new File(args(0))
        logInfo(s" === Param file exists: ${configFile.exists()}")

        // read the config file and generate string value
        val confSource = Source.fromFile(args(0))
        val confString = try confSource.mkString finally confSource.close()

        logInfo(s" === Content of the config file --- \n $confString")

        implicit val config: Config = ConfigFactory.parseString(confString).getConfig("spark")
        implicit val spark: SparkSession = prepareSparkSession(config)

        executeJob(spark,config)

      }
      catch {
        case ex: FileNotFoundException =>  logError(s" === Couldn't locate the param file:  ${args(0)} \n ${ex.getMessage}")
                                            sys.exit(1)
        case ex: Exception => logError(s" === ERROR occurred while executing the job: ${ex.getMessage}")
                              println(s" === Application Error: ${ex.printStackTrace()}")
                              sys.exit(1)
      }
    } else {
      logError(s" === Supply only the application.conf file ..exiting!!!")
      sys.exit(1)
    }
  }

  /**
   * Configure the spark session object
   * @param config application configurations
   * @return SparkSession
   */
  def prepareSparkSession(config: Config): SparkSession = {

    val storageAccounts = config.getStringList("storageAccount.names")
    val oauth2Enabled = config.getBoolean("storageAccount.oauth2.enable")
    val sparkSerializer = if(config.hasPath("spark.serializer")) config.getString("spark.serializer") else "org.apache.spark.serializer.KryoSerializer"

    // set spark conf
    val localSparkConf = new SparkConf()
      .setAppName(config.getString("spark.applicationName"))
      .setMaster(config.getString("spark.master"))
      .set("spark.serializer", sparkSerializer)
      .set("spark.sql.legacy.timeParserPolicy","LEGACY") //allows parsing date format '2021-04-09 12:15:00.000000 UTC'

    // create spark session
    val spark = SparkSession
      .builder()
      .config(localSparkConf)
      .getOrCreate()

    // configure storage accounts
    if (oauth2Enabled) {
      val clientId = config.getString("storageAccount.clientId")
      val tenantId = config.getString("storageAccount.tenantId")
      val secretScope = config.getString("storageAccount.secretScope")
      val secretKey = config.getString("storageAccount.secretKey")
      storageAccounts.forEach(saName => {
        spark.conf.set(s"fs.azure.account.auth.type.$saName.dfs.core.windows.net", "OAuth")
        spark.conf.set(s"fs.azure.account.oauth.provider.type.$saName.dfs.core.windows.net",
          "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
        spark.conf.set(s"fs.azure.account.oauth2.client.id.$saName.dfs.core.windows.net", clientId)
        spark.conf.set(s"fs.azure.account.oauth2.client.secret.$saName.dfs.core.windows.net",
          dbutils.secrets.get(scope = secretScope, key = secretKey))
        spark.conf.set(s"fs.azure.account.oauth2.client.endpoint.$saName.dfs.core.windows.net",
          s"https://login.microsoftonline.com/$tenantId/oauth2/token")
      })
    }

    spark
  }

  /**
   * Abstract function to be implemented by the derived classes
   * @param spark implicit sparkSession object
   * @param config implicit config object
   */
  def executeJob(implicit spark:  SparkSession, config: Config): Unit

}
