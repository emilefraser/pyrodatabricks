package filesAndProcesses


object Control {

  def using[A<: {def close(): Unit}, B](resource: A)(f:A=>B):B =
    try {
      f(resource)
    } finally {
      resource.close()
    }
}
import Control._



 object LoanPattern extends App {
   val filename = "./files/example.txt"

   using(io.Source.fromFile(filename)) {source => {
     source.getLines().foreach(println)
   }}
 }