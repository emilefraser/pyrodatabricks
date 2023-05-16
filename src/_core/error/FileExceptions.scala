package filesAndProcesses

import Control._
import scala.io.Source
import java.io.{FileNotFoundException, IOException}

object FileExceptions extends App{

  val filename = "./files/example.txt"

  /*
    The traditional way - not preferred in scala
  */
  println("\n--- TRADITIONAL ---")
  try {
    val buff = Source.fromFile(filename)
    for (line <- buff.getLines) {
      println(line)
    }
  } catch {
    case e: FileNotFoundException => println("Couldn't find that file.")
    case e: IOException => println("IOException Occurred")
  } finally {
    // horrible since we can't reference
    // buff here to close it!
    // Options with using is much better.
  }


  /*
    returns Some(List[String]) on success
    and None if something goes wrong.
   */
  def readTextFile(filename: String) : Option[List[String]] = {
    try {

      val lines = using(Source.fromFile(filename)) {
        source =>
          (for (l <- source.getLines) yield l).toList
      }
      Some(lines)

    } catch {
      case e: Exception => None
    }
  }

  println("\n--- FOREACH ---")
  val result = readTextFile(filename)
  result.foreach { strings =>
    strings.foreach(println)
  }

  println("\n--- MATCH ---")
  readTextFile(filename) match {
    case Some(lines) => lines.foreach(println)
    case None => println(s"couldn't read file $filename")
  }


}
