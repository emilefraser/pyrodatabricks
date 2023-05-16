package filesAndProcesses

import java.io.{File, FileOutputStream, PrintWriter}

object AppendFilePrintWriter extends App {

  def using[A <: {def close(): Unit}, B](resource: A)(f: A => B): B = {
    try {
      f(resource)
    } finally {
      resource.close()
    }
  }

  val input = "Hello Append File"
  val lineSep = "\n"
  val filename = "./files/append.txt"
  val f = new File(filename)
  val out =
    if (f.exists() && !f.isDirectory) {
      val outStream = new FileOutputStream(f, true)
      new PrintWriter(outStream, true)
    }
    else {
      new PrintWriter(filename)
    }

  out.append(s"$lineSep$input")
  out.close

}
