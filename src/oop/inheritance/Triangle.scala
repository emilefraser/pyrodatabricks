package com.sibytes.inheritance

class Triangle(
                 override val dim1: Double,
                 dim2: Double
               )
  extends Figure(dim1, dim2) {

  override val sides = 3 // has to be immutable otherwise overriding it not allowed
  override def area(): Double = {
    println("Inside Area for Triangle")
    dim1 * dim2 / 2
  }

}
