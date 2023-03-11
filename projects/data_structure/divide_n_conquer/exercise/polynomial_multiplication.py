from divide_n_conquer.exercise.tests import tests


def polynomial_multiplication(poly1, poly2):
    m = len(poly1)
    n = len(poly2)
    result = [0]*(m+n-1)
    for i in range(m):
        for j in range(n):
            result[i+j] += poly1[i] * poly2[j]
    return result

# function that print polynomial


def polynomial(poly):
    n = len(poly)
    for i in range(n): 
        print(poly[i], end="")
        if i != 0:
            print("x^", i, end="")
        if i != n - 1:
            print(" + ", end="")


# polynomial in array representation
if __name__ == "__main__":
    for poly in tests:
        print("First polynomial is:")
        polynomial(poly['input']['poly1'])
        print('\n')
        print("Second polynomial is: ")
        polynomial(poly['input']['poly2'])
        print('\n')
        poly_result = (polynomial_multiplication(**poly['input']))
        print(f"Product of polynomials is: {poly_result}")
        print("Polynomial coefficient result as below: ,")
        polynomial(poly_result)
        print("\n\nPolynomial result status: ", poly_result == poly['output'])

