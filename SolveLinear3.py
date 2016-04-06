def solve_linear_3(coefficients_list, right_hand_list):
    """
    This function uses Crammer's method to solve a 3X3 linear equations system
    """

    det2 = lambda a,b,c,d: a*d - b*c
    det3 = lambda A: A[0][0]*det2(A[1][1], A[1][2], A[2][1], A[2][2]) -\
    A[0][1]*det2(A[1][0], A[1][2], A[2][0], A[2][2]) +\
    A[0][2]*det2(A[1][0], A[1][1], A[2][0], A[2][1])

    detA = det3(coefficients_list)

    if detA == 0:
        print("There are points marked on the edges or vertices of existing\
            triangles. Please mark the points again.")
        exit(1)

    #Crammer's method
    a = [0,0,0]
    for i in range(3):
        A_ = [list(row) for row in coefficients_list]
        A_[0][i] = right_hand_list[0]
        A_[1][i] = right_hand_list[1]
        A_[2][i] = right_hand_list[2]
        a[i] = det3(A_) / detA

    return tuple(a)