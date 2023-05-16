package com.sibytes.interfaceClasses

class Triangle(
                 var dim1: Double,
                 var dim2: Double
               )
  extends Figure {

  override def area(): Double = {
    println("Inside Area for Triangle")
    dim1 * dim2 / 2
  }

}
