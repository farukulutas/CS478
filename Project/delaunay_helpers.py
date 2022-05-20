def is_in_circumcircle(a, b, c, d):
    """
    Calculate the determinant of the 3x3 matrix [a-d, b-d, c-d]
    """
    ax = a[0]-d[0]
    ay = a[1]-d[1]
    bx = b[0]-d[0]
    by = b[1]-d[1]
    cx = c[0]-d[0]
    cy = c[1]-d[1]

    a_dist = ax**2 + ay**2
    b_dist = bx**2 + by**2
    c_dist = cx**2 + cy**2

    det1 = ax*by*c_dist + ay*b_dist*cx + a_dist*bx*cy
    det2 = a_dist*by*cx + ax*b_dist*cy + ay*bx*c_dist
    return det1 - det2 < 0


def left_test(point, edge):
    """
    Left test for a point relative to an edge.
    """
    det1 = (edge[0][0]-point[0]) * (edge[1][1]-point[1])
    det2 = (edge[0][1]-point[1]) * (edge[1][0]-point[0])
    return det2 - det1


def point_on_right(point, edge):
    return left_test(point, edge) < 0


def point_on_left(point, edge):
    return left_test(point, edge) > 0
