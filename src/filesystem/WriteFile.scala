package filesAndProcesses
import java.nio.file.{Paths, Files}
import java.io._


object WriteFile extends App{

  /*
    PrintWriter & FileWriter
    the difference => https://www.coderanch.com/t/418148/certification/Information-PrintWriter-FileWriter

   */
  val input = "Hello File"
  val pwFilename = "./files/printWriter.txt"

  // print writer - doesn't throw IOExceptions
  Files.deleteIfExists(Paths.get(pwFilename))
  val pw = new PrintWriter(new File(pwFilename))
  pw.write(input)
  pw.close()

  // FileWriter - does throw IOExceptions
  val fwFilename = "./files/fileWriter.txt"
  Files.deleteIfExists(Paths.get(fwFilename))
  val file = new File(fwFilename)
  val bw = new BufferedWriter(new FileWriter(file))
  bw.write(input)
  bw.close()

}
