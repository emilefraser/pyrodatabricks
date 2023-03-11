// Databricks notebook source exported at Mon, 28 Mar 2016 15:56:31 UTC
// MAGIC %md ## [Streaming] SPARK-2629: New improved state management
// MAGIC * Introducing a DStream transformation for stateful stream processing
// MAGIC  * Does not scan every key
// MAGIC  * Easier to implement common use cases 
// MAGIC    * timeout of idle data
// MAGIC    * returning items other than state
// MAGIC * Supercedes updateStateByKey in functionality and performance.
// MAGIC * trackStateByKey (note, this name may change)

// COMMAND ----------

// Code Snippet
// Execute the full code at: https://github.com/apache/spark/blob/master/examples/src/main/scala/org/apache/spark/examples/streaming/StatefulNetworkWordCount.scala
StreamingExamples.setStreamingLogLevels()

val sparkConf = new SparkConf().setAppName("StatefulNetworkWordCount")

// Create the context with a 1 second batch size
val ssc = new StreamingContext(sparkConf, Seconds(1))
ssc.checkpoint(".")

// Initial RDD input to trackStateByKey
val initialRDD = ssc.sparkContext.parallelize(List(("hello", 1), ("world", 1)))

// Create a ReceiverInputDStream on target ip:port and count the
// words in input stream of \n delimited test (eg. generated by 'nc')
val lines = ssc.socketTextStream(args(0), args(1).toInt)
val words = lines.flatMap(_.split(" "))
val wordDstream = words.map(x => (x, 1))

// Update the cumulative count using updateStateByKey
// This will give a DStream made of state (which is the cumulative count of the words)
val trackStateFunc = (batchTime: Time, word: String, one: Option[Int], state: State[Int]) => {
  val sum = one.getOrElse(0) + state.getOption.getOrElse(0)
  val output = (word, sum)
  state.update(sum)
  Some(output)
}

val stateDstream = wordDstream.trackStateByKey(
  StateSpec.function(trackStateFunc).initialState(initialRDD))

// COMMAND ----------

