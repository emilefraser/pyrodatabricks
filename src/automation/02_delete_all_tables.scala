import spark.implicits._
import spark.sql

spark.conf.set("spark.databricks.delta.retentionDurationCheck.enabled", false)

val databases = spark.catalog.listDatabases()

for (database <- databases.collect()) {
  spark.catalogue.setCurrentDatabase(database)
  val tables = spark.catalog.listTables()

  for (table <- tables.collect()) {
    if (!table.name.startsWith("daily_") && !table.name.startsWith("average_")) {
      println(s"Dropping ${database.name}.${table.name}")
      try {
        sql(s"DELETE FROM ${table.name}")
      } catch {
        case e: Exception =>
          println(s">>> Not a Delta table: skipping DELETE operation")
      }
      try {
        sql(s"VACUUM ${table.name} RETAIN 0 HOURS")
      } catch {
        case e: Exception =>
          println(s">>> Could not be vacuumed")
      }
      try {
        sql(s"DROP TABLE ${table.name}")
      } catch {
        case e: Exception =>
          println(s">>> Could not be deleted")
      }
    }
  }
}

spark.catalog.clearCache()
println("Done")