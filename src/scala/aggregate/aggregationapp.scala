package cloud.spark.agg

import cloud.spark.util.JobSetup
import com.typesafe.config.Config
import org.apache.spark.sql.{AnalysisException, DataFrame, SparkSession}
import org.apache.commons.lang.exception.ExceptionUtils
import com.databricks.dbutils_v1.DBUtilsHolder.dbutils
import org.apache.spark.internal.Logging

/**
 * The main consumer application object to be executed at runtime
 *
 * @author Bijoy Chaudhury
 */
object AggregationApp extends JobSetup with Logging {
  /**
   * Define the data ingestion logic
   *
   * @param spark implicit sparkSession object
   */
  def executeJob(implicit spark: SparkSession, config: Config): Unit = {

    val sparkAppName = config.getString("spark.applicationName")
    val logLevel = config.getString("spark.logLevel")

    val aggLatency = config.getInt("app.aggLatency")
    val aggCatchupLimitDays = config.getInt("app.aggCatchupLimitDays")
    val aggModule = config.getString("app.aggModule") // hourly,daily
    val aggMode = config.getString("app.aggMode") // delta, adhoc
    val aggDate = if (aggMode.equals("adhoc")) config.getString("app.aggDate") else "NA"
    val aggStartHour = if (aggModule.equals("hourly") && aggMode.equals("adhoc")) config.getString("app.aggStartHour") else "NA"
    val aggEndHour = if (aggModule.equals("hourly") && aggMode.equals("adhoc")) config.getString("app.aggEndHour") else "NA"

    val aggProcessingType = config.getString("app.aggProcessingType") // singleStage, multiStage
    val aggEnrichmentEnable = config.getBoolean("app.aggEnrichmentEnable") // true/false
    val dailyPartitionName = config.getString("app.dailyPartitionName")
    val hourlyPartitionName = if (config.hasPath("app.hourlyPartitionName")) config.getString("app.hourlyPartitionName") else ""

    val aggTargetDataFormat = config.getString("app.aggTargetDataFormat")
    val aggSourceDataFormat = config.getString("app.aggSourceDataFormat")

    // enrichment config
    val enrichmentDataPaths = if (aggEnrichmentEnable) config.getString("app.enrichmentDataPaths").split(",") else null
    val enrichmentDataFormats = if (aggEnrichmentEnable) config.getString("app.enrichmentDataFormats").split(",") else null
    val enrichmentDataAliases = if (aggEnrichmentEnable) config.getString("app.enrichmentDataAliases").split(",") else null

    val aggOutDataPaths = config.getString("app.aggOutDataPaths").split(",")
    val aggQueryAliases = config.getString("app.aggQueryAliases").split(",")
    val aggQueryPaths = config.getString("app.aggQueryPaths").split(",")
    val aggDropTempDataEnable =  if(aggProcessingType.equals("multiStage")) config.getBoolean("app.aggDropTempDataEnable") else false

    // tokens for replacement. for hourly pass datePart, hourPartStart, hourPartEnd
    val queryDatePartToken = config.getString("app.queryDatePartToken")
    val queryHourPartStartToken = if (config.hasPath("app.queryHourPartStartToken")) config.getString("app.queryHourPartStartToken") else ""
    val queryHourPartEndToken = if (config.hasPath("app.queryHourPartEndToken")) config.getString("app.queryHourPartEndToken") else ""

    // read storage account configs
    val storageAccountUrl = config.getString("storageAccount.url")
    val aggSourceHome = config.getString("app.aggSourceHome")
    val sourceDir = AggregationUtil.preparePath(aggSourceHome, storageAccountUrl)
    val targetDir = AggregationUtil.preparePath(aggOutDataPaths(aggOutDataPaths.length - 1), storageAccountUrl) // last output path

    // define local variables
    var isFirstTimeExecution = false
    var tgtDf: DataFrame = null
    var finalDf: DataFrame = null
    var aggRangeList: List[(String, String, String)] = List()
    var last_agg_dt = ""
    var last_agg_hr = ""
    var eligible_agg_dt = ""
    var eligible_agg_hr = ""
    var formattedQuery = ""

    try {
      spark.sparkContext.setLogLevel(logLevel)

      logInfo(s" === Validating config parameters for application $sparkAppName")
      if (!AggregationUtil.validateParams(aggEnrichmentEnable, enrichmentDataPaths, enrichmentDataAliases, enrichmentDataFormats, aggProcessingType,
        aggModule, aggMode, aggOutDataPaths, aggQueryAliases, aggQueryPaths)) {
        logError(s" === Parameters validation failed!!!")
        sys.exit(1)
      }

      logInfo(s" === Processing mode is '${aggProcessingType}'")
      logInfo(s" === Data input format : '${aggSourceDataFormat}'  Data output format : '${aggTargetDataFormat}'")
      logInfo(s" === Data aggregation module:'${aggModule}'  mode:'${aggMode}'  processingType:'${aggProcessingType}'")

      // step1: read source data
      logInfo(s" === Registering source dataframe path '$sourceDir' as '${aggQueryAliases(0)}' table")
      val srcDf = spark.read.format(aggSourceDataFormat).load(sourceDir)
      srcDf.createOrReplaceTempView(aggQueryAliases(0))

      // step2: load target data
      try {
        logInfo(s"Loading target directory ${targetDir}")
        tgtDf = spark.read.format(aggTargetDataFormat).load(targetDir)
      } catch {
        case ex: AnalysisException => {
          logWarning(s"Error occurred while trying to read data from ${targetDir}. Perhaps no data is available to read. " +
            s"\n Error Description: ${ex.getMessage()}")
          isFirstTimeExecution = true
        }
      }

      // register UDFs and spark conf
      spark.udf.register("epochToTzTs", AggregationUtil.fromUtcTimestamp _)

      // register enrichment table in memory
      if (aggEnrichmentEnable) {
        for (index <- enrichmentDataPaths.indices) {
          val path = AggregationUtil.preparePath(enrichmentDataPaths(index), storageAccountUrl)
          val format = enrichmentDataFormats(index)
          val alias = enrichmentDataAliases(index)
          logInfo(s" === Enrichment: registering path '${path}' with '${format}' format as '${alias}' temp table ")
          spark.read.format(format).load(path).createOrReplaceTempView(alias)
        }
      }

      aggModule match {
        case "hourly" => {
          aggMode match {
            // resume from last aggregated hour
            case "delta" => aggRangeList = {
              // ------ Identify max date-hour for aggregation -------
              logInfo(s" === Identifying max date-hour available in source data")
              val srcMaxDtHr = AggregationUtil.getDataMaxDtHr(srcDf, dailyPartitionName, hourlyPartitionName)
              logInfo(s" === Source maxDate:${srcMaxDtHr._1}  maxHour:${srcMaxDtHr._2}  latency to be applied:-${aggLatency} hours")
              val eligible_dt_hr = AggregationUtil.hourAdd(srcMaxDtHr._1 + srcMaxDtHr._2, -(aggLatency), "yyyy-MM-ddHH")
              eligible_agg_dt = eligible_dt_hr.substring(0, 10)
              eligible_agg_hr = eligible_dt_hr.substring(10)

              var tgtMaxDtHr: (String, String) = null
              logInfo(s" === Identifying max date-hour available in target data")
              if (isFirstTimeExecution)
                tgtMaxDtHr = AggregationUtil.getDataMinDtHr(srcDf, dailyPartitionName, hourlyPartitionName)
              else
                tgtMaxDtHr = AggregationUtil.getDataMaxDtHr(tgtDf, dailyPartitionName, hourlyPartitionName)

              last_agg_dt = tgtMaxDtHr._1
              last_agg_hr = tgtMaxDtHr._2

              logInfo(s" === last_agg_dt:$last_agg_dt  last_agg_hr:$last_agg_hr  eligible_agg_dt:$eligible_agg_dt  eligible_agg_hr:$eligible_agg_hr")

              AggregationUtil.prepareHrlyAggBoundary(last_agg_dt, last_agg_hr, eligible_agg_dt, eligible_agg_hr, aggCatchupLimitDays, isFirstTimeExecution)
            }

            // Aggregate the supplied  date
            case "adhoc" => //aggRangeList:+= ((aggDate,"00","23"))
              aggDate.split(",").foreach(part_val => aggRangeList :+= ((part_val, aggStartHour, aggEndHour)))

            // Exit processing due to invalid mode
            case _ => {
              logError(s" === Unsupported aggregation mode '${aggMode}'")
              sys.exit(1)
            }
          }
        }

        case "daily" => {
          aggMode match {
            // resume from last aggregated hour
            case "delta" => {
              logInfo(s" === Identifying max date available in source data")
              val srcMinMaxDt = AggregationUtil.getDataMinMaxDate(srcDf, dailyPartitionName)
              logInfo(s" === Source maxDate:${srcMinMaxDt._2}  minDate:${srcMinMaxDt._1}  latency to be applied:-${aggLatency} days")
              eligible_agg_dt = AggregationUtil.dateAdd(srcMinMaxDt._2, -aggLatency, "yyyy-MM-dd") // max date -  latency

              if (isFirstTimeExecution)
                last_agg_dt = srcMinMaxDt._1 // min date
              else {
                val tgtMinMaxDt = AggregationUtil.getDataMinMaxDate(tgtDf, dailyPartitionName)
                last_agg_dt = tgtMinMaxDt._2 // max date
              }
              logInfo(s" === last_agg_dt:$last_agg_dt eligible_agg_dt:$eligible_agg_dt")

              aggRangeList = AggregationUtil.prepareDlyAggBoundary(last_agg_dt, eligible_agg_dt, aggCatchupLimitDays)
            }

            // Aggregate the supplied  date
            case "adhoc" => aggDate.split(",").foreach(part_val => aggRangeList :+= ((part_val, "NA", "NA")))

            // Exit processing due to invalid mode
            case _ => {
              logError(s" === Unsupported aggregation mode '${aggMode}'")
              sys.exit(1)
            }
          }

        }
      }

      logInfo(s" === The aggregation boundary: ${aggRangeList.mkString("|")}")

      // ------- Perform aggregation ---------
      aggProcessingType match {
        case "singleStage" => {
          aggRangeList.foreach(dateVal => {

            formattedQuery = AggregationUtil.prepareQuery(aggModule, aggQueryPaths(0), dateVal, queryDatePartToken, queryHourPartStartToken, queryHourPartEndToken, true)
            logInfo(s" === Aggregation '$aggModule': formatted query to be executed: \n ${formattedQuery}")
            finalDf = spark.sql(formattedQuery)

            logInfo(s" === Aggregating $dailyPartitionName=${dateVal._1} ${hourlyPartitionName}_start=${dateVal._2} ${hourlyPartitionName}_end=${dateVal._3}")

            // create DF writer
            var dfWriter = finalDf.write
              .format(aggTargetDataFormat)
              .mode("overwrite")
              .option("mergeSchema", "true")

            // add option to overwrite delta partitions
            if (aggModule.equals("hourly"))
              dfWriter = dfWriter.option("replaceWhere", s"$dailyPartitionName='${dateVal._1}' and $hourlyPartitionName>='${dateVal._2}' and $hourlyPartitionName<='${dateVal._3}'")
            else
              dfWriter = dfWriter.option("replaceWhere", s"$dailyPartitionName='${dateVal._1}'")

            // assign partitions
            dfWriter = AggregationUtil.assignPartitions(dfWriter, dailyPartitionName, hourlyPartitionName)

            logInfo(s" === Writing aggregation output to $targetDir")

            // finally execute the writer
            dfWriter.save(targetDir)

            logInfo(s" === Aggregation completed for ${dailyPartitionName}=${dateVal._1} ${hourlyPartitionName}_start=${dateVal._2} ${hourlyPartitionName}_end=${dateVal._3}")
          })

        }
        case "multiStage" => {
          aggRangeList.foreach(dateVal => {
            logInfo(s" === Aggregating $dailyPartitionName=${dateVal._1} ${hourlyPartitionName}_start=${dateVal._2} ${hourlyPartitionName}_end=${dateVal._3}")
            var outDir = ""
            for (index <- aggOutDataPaths.indices) {
              var tempDf: DataFrame = null
              var writeTempDataEnable = if (index == aggOutDataPaths.length - 1) true else false
              //if (index != 0) {
              val path = s"${AggregationUtil.preparePath(aggOutDataPaths(index), storageAccountUrl)}_${dateVal._1}"
              val aggQueryPath = aggQueryPaths(index)
              val alias = if (index < aggQueryPaths.length - 1) aggQueryAliases(index + 1) else "defaultFinalTbl"

              if (index == 0)
                formattedQuery = AggregationUtil.prepareQuery(aggModule, aggQueryPath, dateVal, queryDatePartToken, queryHourPartStartToken, queryHourPartEndToken, replaceToken = true)
              else
                formattedQuery = AggregationUtil.prepareQuery(aggModule, aggQueryPath, dateVal, queryDatePartToken, queryHourPartStartToken, queryHourPartEndToken, replaceToken = false)

              logInfo(s" === Aggregation '$aggModule': formatted query to be executed: \n ${formattedQuery}")

              if (index == aggOutDataPaths.length - 1) // final location
                outDir = targetDir
              else // temp location
                outDir = s"${AggregationUtil.preparePath(aggOutDataPaths(index), storageAccountUrl)}_${dateVal._1}"


              logInfo(s" === Reading step$index data from storage account path $path")
              try {
                if(index < aggOutDataPaths.length-1) {
                  tempDf = spark.read.format(aggTargetDataFormat).load(path)
                  logInfo(s" === Step$index data is loaded in memory ")
                } else
                  tempDf = spark.sql(formattedQuery)
              } catch {
                case ex: AnalysisException =>
                  logWarning(s" === ERROR occurred while reading step$index data directory: ${ex.getMessage}")
                  logInfo(s" === Step$index temp directory might be empty. Executing step$index query...")
                  tempDf = spark.sql(formattedQuery)
                  writeTempDataEnable = true
              }

              if(index < aggOutDataPaths.length-1) { // no need to register in final stage
                logInfo(s" === Registering path '${path}' as '${alias}' temp table ")
                tempDf.createOrReplaceTempView(alias)
              }

              if (writeTempDataEnable) {
                logInfo(s" === Writing step$index output to $outDir")

                // create DF writer
                var dfWriter = tempDf.write
                  .format(aggTargetDataFormat)
                  .mode("overwrite")
                  .option("mergeSchema", "true")

                // add option to overwrite delta partitions
                if (aggModule.equals("hourly"))
                  dfWriter = dfWriter.option("replaceWhere", s"$dailyPartitionName='${dateVal._1}' and $hourlyPartitionName>='${dateVal._2}' and $hourlyPartitionName<='${dateVal._3}'")
                else
                  dfWriter = dfWriter.option("replaceWhere", s"$dailyPartitionName='${dateVal._1}'")

                // assign partitions
                dfWriter = AggregationUtil.assignPartitions(dfWriter, dailyPartitionName, hourlyPartitionName)

                logInfo(s" === Spark writer execution started for step$index")
                // finally execute the writer
               dfWriter.save(outDir)
              }
              //}
            }
            logInfo(s" === Aggregation completed for ${dailyPartitionName}=${dateVal._1} ${hourlyPartitionName}_start=${dateVal._2} ${hourlyPartitionName}_end=${dateVal._3}")

            if (aggDropTempDataEnable){
              aggRangeList.foreach(dateVal => {
                for (index <- aggOutDataPaths.indices) {
                  if (index != 0) {
                    val path = s"${AggregationUtil.preparePath(aggOutDataPaths(index), storageAccountUrl)}_${dateVal._1}"
                    logInfo(s" === Deleting temp directory $path")
                    dbutils.fs.rm(path, true)
                  }
                }
              })
            }

          })

        }
      }

    } catch {
      case e: Throwable => {
        val logStatus = "Failure"
        val logFailureMessage = ExceptionUtils.getStackTrace(e)
        logError(s" === Handled: Error occurred at spark job: ${logFailureMessage}")

        throw e
      }
    }
  }


}
