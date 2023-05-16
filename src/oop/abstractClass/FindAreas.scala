package com.sibytes.abstractClass

object FindAreas {
  def main(args: Array[String]): Unit = {
    //val figure:Figure = new Figure(10,10)
    val rectangle: Rectangle = new Rectangle(9, 5)
    val triangle:Triangle = new Triangle(10, 8)

    //reference has the type of the superclass
    val figures = Array[Figure](rectangle, triangle)

    figures.map(f => (println(s"Area is ${f.area()}")))

  }
}
