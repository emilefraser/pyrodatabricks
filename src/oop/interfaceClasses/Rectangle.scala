package com.sibytes.interfaceClasses

class Rectangle(
                 var dim1: Double,
                 var dim2: Double
               )
  extends Figure {


  override def area(): Double = {
    println("Inside Area for Rectangle")
    dim1 * dim2
  }

}
