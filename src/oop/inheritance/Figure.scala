package com.sibytes.inheritance

class Figure(val dim1: Double, var dim2: Double)
{
  val sides = 4 //can't be mutable if it's going to be overridden
  def area() = {
    println("Area for figure is undefined.")
    0d
  }
}
