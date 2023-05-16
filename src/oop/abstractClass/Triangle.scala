package com.sibytes.abstractClass

class Triangle(
                 dim1: Double,
                 dim2: Double
               )
  extends Figure(dim1, dim2) {

  override def area(): Double = {
    println("Inside Area for Triangle")
    dim1 * dim2 / 2
  }

}
