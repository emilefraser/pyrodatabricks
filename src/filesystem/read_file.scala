package filesAndProcesses

import scala.io.Source

object ReadFile extends App{

  /*
    concise but leaves the file open
    sudo lsof -u shaun | './files/example.txt'

    use Thread.sleep afterwards to see this
  */

  val filename = "./files/example.txt"
  for (line <- Source.fromFile(filename).getLines()){
    println(line)
  }

  // return as a list and array
  // filename
  // getlines() separators are \r\n \r \n longest match
  val linesList = Source.fromFile(filename).getLines().toList
  linesList.foreach(print)
  val linesArray = Source.fromFile(filename).getLines().toArray
  linesArray.foreach(print)
  // combine into a string
  val linesString = Source.fromFile(filename).getLines().mkString(" ")
  print(linesString)

  /*
    properly closing the file
   */
  val bufferedSource = Source.fromFile(filename)
  for (line <- bufferedSource.getLines()){
    println(line)
  }
  bufferedSource.close()


}
