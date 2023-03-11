package cloud.spark.agg

import org.apache.spark.internal.Logging
import org.apache.spark.sql.{DataFrame, DataFrameWriter, Row}
import org.apache.spark.sql.functions.{col, max, min}
import java.text.SimpleDateFormat
import java.util.{Calendar, TimeZone}
import scala.io.Source
object AggregationUtil extends Logging {

  /**
   * Retrieves the max available date and hour from the input dataframe
   *
   * @param inputDf dataframe to query
   * @param datePartName date partition name
   * @param hourPartName hour partition name
   * @return a tuple of (max_date,max_hour)
   */
  def getDataMaxDtHr(inputDf: DataFrame, datePartName: String, hourPartName: String): (String, String) = {
    if(datePartName.isEmpty || hourPartName.isEmpty) {
      logError(s" === getDataMaxDtHr: input datePart='$datePartName' or hourPart='$hourPartName' is empty")
      sys.exit(1)
    }
    var max_date_part = ""
    var max_hour_part = ""

    val maxHrDf = inputDf.groupBy(col(datePartName)).agg(max(col(hourPartName))).orderBy(col(datePartName).desc).limit(1)

    maxHrDf.collect().foreach( row => {
      max_date_part = row.getString(0)
      max_hour_part = row.getString(1)
    })

    (max_date_part,max_hour_part)
  }

  /**
   * Retrieves the max available date and hour from the input dataframe
   *
   * @param inputDf dataframe to query
   * @param datePartName date partition name
   * @param hourPartName hour partition name
   * @return a tuple of (max_date,max_hour)
   */
  def getDataMinDtHr(inputDf: DataFrame, datePartName: String, hourPartName: String): (String, String) = {
    if(datePartName.isEmpty || hourPartName.isEmpty) {
      logError(s" === getDataMinDtHr: input datePart='$datePartName' or hourPart='$hourPartName' is empty")
      sys.exit(1)
    }
    var min_date_part = ""
    var min_hour_part = ""

    val maxHrDf = inputDf.groupBy(col(datePartName)).agg(min(col(hourPartName))).orderBy(col(datePartName).asc).limit(1)

    maxHrDf.collect().foreach( row => {
      min_date_part = row.getString(0)
      min_hour_part = row.getString(1)
    })

    (min_date_part,min_hour_part)
  }

  /**
   * Retrieves the max available date from the input dataframe
   *
   * @param inputDf dataframe to query
   * @param datePart date partition name
   * @return a tuple of (minDatePart,maxDatePart)
   */
  def getDataMinMaxDate(inputDf: DataFrame, datePart: String): (String,String) = {
    if(datePart.isEmpty) {
      logError(s" === getDataMinMaxDt: input datePart='$datePart' is empty")
      sys.exit(1)
    }
    var minDatePart = ""
    var maxDatePart = ""

    val maxHrDf = inputDf.agg(min(col(datePart)),max(col(datePart)))

    maxHrDf.collect().foreach( row => {
      minDatePart = row.getString(0)
      maxDatePart = row.getString(1)
    })

    (minDatePart,maxDatePart)
  }

  /**
   * Converts integer hour into string hour in 'hh' format
   * @param hourPart hour value in integer
   * @return string representation of the hour in 'hh' format
   */
  def formatHourPart(hourPart: Integer): String = {
    if (hourPart.toString.length < 2)
       "0"+hourPart.toString
    else hourPart.toString
  }

  /**
   * Performs data manipulations
   * @param date date in string format
   * @param days number of days to add
   * @param dateFormat format of the input date
   * @return manipulated date in the specified dateFormat
   */
  def dateAdd(date: String, days: Int, dateFormat: String) : String = {
    val currTime = Calendar.getInstance()
    currTime.setTime(new SimpleDateFormat(dateFormat).parse(date))
    currTime.add(Calendar.DATE, days)

    new SimpleDateFormat(dateFormat).format(currTime.getTime())
  }

  /**
   * Performs hour manipulation
   * @param date date-hour in string format
   * @param hours number of hours to add
   * @param dateFormat format of the input date-hour
   * @return date-hour in the specified dateFormat
   */
  def hourAdd(date: String, hours: Int, dateFormat: String) : String = {
    val currTime = Calendar.getInstance()
    currTime.setTime(new SimpleDateFormat(dateFormat).parse(date))
    currTime.add(Calendar.HOUR_OF_DAY, hours)

    new SimpleDateFormat(dateFormat).format(currTime.getTime())
  }

  /**
   * Prepares the hourly aggregation boundary per date
   *
   * @param lastAggDt last aggregation data
   * @param lastAggHr last aggregation hour
   * @param latestAggDt latest aggregation date
   * @param latestAggHr latest aggregation hour
   * @param catchupLimit number of days to restrict the aggregation boundary
   * @return list of tuple(aggDate,aggHourStart,aggHourEnd)
   */
  def prepareHrlyAggBoundary(lastAggDt:String, lastAggHr:String, latestAggDt:String, latestAggHr:String,
                             catchupLimit: Integer, isFirstTimeExecution: Boolean ): List[(String,String,String)] = {
    var aggList : List[(String,String,String)] = List()
    if (lastAggDt.equals(latestAggDt)){
      if(latestAggHr > lastAggHr)
        if(isFirstTimeExecution)
          aggList:+=((lastAggDt,formatHourPart(lastAggHr.toInt),latestAggHr))
        else
          aggList:+=((lastAggDt,formatHourPart(lastAggHr.toInt+1),latestAggHr))
      else
        logInfo(" === prepareHrlyAggBoundary: the aggregation is up to date. Skipping current execution...")
    } else if (lastAggDt < latestAggDt){
      var initDate = lastAggDt
      var startHr = lastAggHr
      var endHr = latestAggHr
      var dayCnt = 0
      while(initDate <= latestAggDt && dayCnt < catchupLimit  ) {
        if (initDate.equals(latestAggDt))
          endHr = latestAggHr
        else
          endHr = "23"
        if (startHr < "23" || isFirstTimeExecution )
          if ((startHr == "00" && dayCnt > 0) || isFirstTimeExecution)
            aggList:+= ((initDate,formatHourPart(startHr.toInt),endHr))
          else
            aggList:+= ((initDate,formatHourPart(startHr.toInt+1),endHr))

        initDate = dateAdd(initDate,1,"yyyy-MM-dd")
        startHr = "00"
        dayCnt += 1
      }
    } else {
      logError(s" === prepareHrlyAggBoundary: the latestAggDt:$latestAggDt is smaller than lastAggDt:$lastAggDt")
      System.exit(1)
    }

    aggList
  }

  /**
   *  Prepares the daily aggregation boundary
   * @param lastDlyAggDt last date of daily aggregation
   * @param latestHrlyAggDt latest date of hourly aggregation
   * @param catchupLimit number of days to restrict the aggregation boundary
   * @return list of aggregation dates
   */
  def prepareDlyAggBoundary(lastDlyAggDt:String, latestHrlyAggDt:String, catchupLimit: Integer): List[(String,String,String)] = {
    var aggList : List[(String,String,String)] = List()
    if (lastDlyAggDt.equals(latestHrlyAggDt)){
      logWarning(" === prepareDlyAggBoundary: the aggregation is up to date. Skipping current execution...")
    } else if (lastDlyAggDt < latestHrlyAggDt){
      var initDate = dateAdd(lastDlyAggDt,1,"yyyy-MM-dd")
      var iterations = 0
      while(initDate <= latestHrlyAggDt && iterations < catchupLimit ) {
        aggList:+= ((initDate,"NA","NA"))
        initDate = dateAdd(initDate,1,"yyyy-MM-dd")
        iterations += 1
      }
    } else {
      logError(s" === prepareDlyAggBoundary: the latestHrlyAggDt:$latestHrlyAggDt is smaller than lastDlyAggDt:$lastDlyAggDt")
      System.exit(1)
    }

    aggList
  }

  /**
   *  Convert the epoch time to specified timezone TimeStamp
   *
   *  @param epoch timestamp as string
   *  @param timezone timezone as string
   *  @return date as timestamp
   */
  def fromUtcTimestamp(epoch :String, timezone: String):String = {
    var epochFomatted = 0L
    val dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSS")
    try {
      if ( epoch.length > 13 )
        epochFomatted = epoch.toLong/1000
      else if ( epoch.length < 13 )
        epochFomatted = epoch.toLong * 1000
      else
        epochFomatted = epoch.toLong

      if ( ! timezone.isEmpty ) {
        dateFormat.setTimeZone(TimeZone.getTimeZone(timezone))
        return dateFormat.format(epochFomatted)
      } else {
        dateFormat.setTimeZone(TimeZone.getTimeZone("UTC"))
        return dateFormat.format(epochFomatted)
      }
    } catch {
      case e: Exception => {print(s"Exception oxccurred in fromUtcTimestamp: $e" + e.printStackTrace()) }
        return epoch
    }
  }

  /**
   * Prepares the absolute path from the input path URI
   * @param path path prefix with URI
   * @param storageAccountUrl storage account URL
   * @return the absolute file system path
   */
  def preparePath(path: String, storageAccountUrl: String) : String = {
    var output: String = ""
    val tokens = path.split(":")

    if (tokens.length != 2) {
      logError(s" === Invalid path supplied. Make sure there is only one colon(:) in the path ${path}")
      sys.exit(1)
    }

    tokens(0) match {
      case "adls" => output = storageAccountUrl + tokens(1)
      case "dbfs" => output = path
      case _ => {
        logError(s" === Unsupported file system URI '${tokens(0)}'. Only 'adls' and 'dbfs' file systems are supported")
        sys.exit(1)
      }
    }

    logInfo(s" === The input path ${path} is transformed into ${output} ")

    output
  }


  /**
   *  Validates the passed parameters
   * @param aggEnrichmentEnable
   * @param enrichmentDataPaths
   * @param enrichmentDataAliases
   * @param enrichmentDataFormats
   * @param aggProcessingType
   * @param aggModule
   * @param aggMode
   * @param aggDataPaths
   * @param aggTableAliases
   * @param aggQueryPaths
   * @return true if the validation is passed
   */
  def validateParams(aggEnrichmentEnable:Boolean, enrichmentDataPaths: Array[String], enrichmentDataAliases: Array[String],
                     enrichmentDataFormats: Array[String], aggProcessingType: String, aggModule: String, aggMode: String,
                     aggDataPaths: Array[String], aggTableAliases: Array[String], aggQueryPaths: Array[String]): Boolean = {
    var response = true
    if(aggEnrichmentEnable && (enrichmentDataPaths.length != enrichmentDataAliases.length || enrichmentDataAliases.length != enrichmentDataFormats.length
      || enrichmentDataPaths.length !=  enrichmentDataFormats.length)) {
      logError(s" === The count of elements for 'enrichmentDataPaths' and 'enrichmentDataFormats' and 'enrichmentDataAliases' don't match ")
      response = false
    }
    if (!aggProcessingType.equals("singleStage") && !aggProcessingType.equals("multiStage")) {
      logError(s" === Unsupported processing type '${aggProcessingType}'. Allowed values - singleStage,multiStage " )
      response = false
    }
    if (aggProcessingType.equals("singleStage") && aggDataPaths.length != 1) {
      logError(s" === The aggDataPaths.length must be 1 for 'singleStage' aggProcessingType" )
      response = false
    }
    if (aggProcessingType.equals("multiStage") && aggDataPaths.length <= 1) {
      logError(s" === The aggDataPaths.length must be greater than 1 for 'multiStage' aggProcessingType" )
      response = false
    }
    if (aggDataPaths.length != aggTableAliases.length || aggTableAliases.length != aggQueryPaths.length ||
      aggDataPaths.length != aggQueryPaths.length) {
      logError(s" === The element count for aggDataPaths, aggTableAliases, and aggDataPaths must match" )
      response = false
    }
    if (!aggModule.equals("hourly") && !aggModule.equals("daily")) {
      logError(s" === Unsupported aggModule '${aggModule}'. Allowed values - hourly,daily " )
      response = false
    }
    if (!aggMode.equals("delta") && !aggMode.equals("adhoc")) {
      logError(s" === Unsupported aggMode '${aggMode}'. Allowed values -  delta, adhoc " )
      response = false
    }

    response
  }

  /**
   *  Assigns partitions to the input DataFrameWriter
   * @param dfWriter DataFrameWriter to be updated
   * @param dailyPartitionName partitions column 1
   * @param hourlyPartitionName partition column 2
   * @return DataFrameWriter with partitions added
   */
  def assignPartitions(dfWriter: DataFrameWriter[Row], dailyPartitionName: String, hourlyPartitionName: String): DataFrameWriter[Row] = {
    // assign partition columns
    var updatedDfWriter = dfWriter
    if(!dailyPartitionName.isEmpty && !hourlyPartitionName.isEmpty) {
      updatedDfWriter = dfWriter.partitionBy(dailyPartitionName,hourlyPartitionName)
      logInfo(s" === The partition columns are - ${dailyPartitionName}, ${hourlyPartitionName}")
    } else
      if (!dailyPartitionName.isEmpty) {
        updatedDfWriter = dfWriter.partitionBy(dailyPartitionName)
        logInfo(s" === The partition column is - ${dailyPartitionName}")
      } else
        if (!hourlyPartitionName.isEmpty) {
          updatedDfWriter = dfWriter.partitionBy(hourlyPartitionName)
          logInfo(s" === The partition column is - ${hourlyPartitionName}")
        } else
          logWarning(s" === No partition column is defined")

    updatedDfWriter
  }

  /**
   * Loads query from the specified file and replaces date, hour boundary with expected value
   * @param filePath file containing the query
   * @param data a tuple of (datePart,hourPartStart,hourPartEnd)
   * @param dateToken date token to replace with actual value
   * @param hrlyStartToken hour start token to replace with actual value
   * @param hrlyEndToken hour end token to replace with actual value
   * @param replaceToken set to true if tokens should be replaced
   * @return formatted wel-lformed query ready for execution
   */
  def prepareQuery(module: String, filePath: String, data: (String,String,String), dateToken: String, hrlyStartToken: String, hrlyEndToken: String,
                       replaceToken: Boolean): String = {
    val querySource = Source.fromFile(filePath)
    val queryString = try querySource.mkString finally querySource.close()
    var formattedQuery = ""
    if(replaceToken && module.equals("hourly")) {
      if (!queryString.contains(dateToken) || !queryString.contains(hrlyStartToken) || !queryString.contains(hrlyEndToken)) {
        logError(s" === prepareQuery: Supplied date/hour tokens not available in agg query. Verify tokens - '${dateToken}'," +
          s"' ${hrlyStartToken}','${hrlyEndToken}'")
        sys.exit(1)
      }
      formattedQuery = queryString.replace(dateToken, data._1)
      formattedQuery = formattedQuery.replace(hrlyStartToken, data._2)
      formattedQuery = formattedQuery.replace(hrlyEndToken, data._3)
    } else if (replaceToken && module.equals("daily")) {
      if (!queryString.contains(dateToken)) {
        logError(s" === prepareQuery: Supplied date token not available in agg query. Verify token - '${dateToken}'")
        sys.exit(1)
      }
      formattedQuery = queryString.replace(dateToken, data._1)
    } else
      formattedQuery = queryString

    formattedQuery
  }
}
