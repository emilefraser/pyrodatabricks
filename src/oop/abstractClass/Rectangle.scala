package com.sibytes.abstractClass

class Rectangle(
                 dim1: Double,
                 dim2: Double
               )
  extends Figure(dim1, dim2) {

  override def area(): Double = {
    println("Inside Area for Rectangle")
    dim1 * dim2
  }

}
