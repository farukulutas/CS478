import math

def find_inclusive_triangle(points):
    """
    Find a triangle that contains all the points
    This triangle should be big enough that when it's vertexes are removed from the triangulation, the remaning triangulation is complete.
    O(n) time and O(1) space
    """
    # Find minimum and maximum x and y coordinates
    min_x = points[0][0]
    max_x = points[0][0]
    min_y = points[0][1]
    max_y = points[0][1]
    
    for point in points:
        if point[0] < min_x:
            min_x = point[0]
        if point[0] > max_x:
            max_x = point[0]
        if point[1] < min_y:
            min_y = point[1]
        if point[1] > max_y:
            max_y = point[1]

    margin = (max_x - min_x + max_y - min_y + 1) * 1000

    return [min_x - margin, min_y - margin], [max_x + max_y - min_y + margin, min_y], [min_x, max_y + max_x - min_x + margin]

def point_in_triangle(pt, tri):
    """
    O(1) time and O(1) space
    Reference: https://stackoverflow.com/a/20949123/7279624
    """
    a = 1/(-tri[1][1]*tri[2][0]+tri[0][1]*(-tri[1][0]+tri[2][0]) +
           tri[0][0]*(tri[1][1]-tri[2][1])+tri[1][0]*tri[2][1])
    s = a*(tri[2][0]*tri[0][1]-tri[0][0]*tri[2][1]+(tri[2][1]-tri[0][1])*pt[0] +
           (tri[0][0]-tri[2][0])*pt[1])
    if s < 0:
        return False
    else:
        t = a*(tri[0][0]*tri[1][1]-tri[1][0]*tri[0][1]+(tri[0][1]-tri[1][1])*pt[0] +
               (tri[1][0]-tri[0][0])*pt[1])
    return ((t > 0) and (1-s-t > 0))

def find_containing_triangle(point, triangles):
    """
    Find the triangle that contains the point
    O(n) time and O(n) space
    """
    for triangle in triangles:
        if point_in_triangle(point, triangle):
            return triangle
    return None

def get_angle(a, b, c):
    """
    Calculate the angle between three points
    This is not vectoral and is always between 0 and 180 degrees
    O(1) time and O(1) space
    Reference: https://manivannan-ai.medium.com/find-the-angle-between-three-points-from-2d-using-python-348c513e2cd
    """
    ang = math.degrees(math.atan2(
        c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    ang = -ang if ang < 0 else ang
    return 360 - ang if ang > 180 else ang

def legalize_edge(againts_point, container_triangle, triangles):
    if (container_triangle[0] == againts_point):
        commonV1 = container_triangle[1]
        commonV2 = container_triangle[2]
    elif (container_triangle[1] == againts_point):
        commonV1 = container_triangle[0]
        commonV2 = container_triangle[2]
    else:
        commonV1 = container_triangle[0]
        commonV2 = container_triangle[1]

    for triangle in triangles:
        if (commonV1 in triangle and commonV2 in triangle and againts_point not in triangle):

            if(triangle[0] != commonV1 and triangle[0] != commonV2):
                last_vertex = triangle[0]
            elif(triangle[1] != commonV1 and triangle[1] != commonV2):
                last_vertex = triangle[1]
            else:
                last_vertex = triangle[2]

            angle1 = get_angle(commonV1, againts_point, commonV2)
            angle2 = get_angle(commonV1, last_vertex, commonV2)

            if (angle1 + angle2 > 180):
                triangles.remove(triangle)
                triangles.remove(container_triangle)

                new_triangle_1 = [commonV1, againts_point, last_vertex]
                new_triangle_2 = [commonV2, againts_point, last_vertex]

                triangles.append(new_triangle_1)
                triangles.append(new_triangle_2)
                legalize_edge(againts_point, new_triangle_1, triangles)
                legalize_edge(againts_point, new_triangle_2, triangles)

            break

def add_point(point, triangles):
    """
    Incrementally addes one new point to the triangulation
    # TODO: If the new point is on an edge
    """
    # Find which triangle contains the point
    containing_triangle = find_containing_triangle(point, triangles)

    # Remove the containing triangle from the list of triangles
    triangles.remove(containing_triangle)

    # Form 3 new triangles
    triangle1 = [containing_triangle[0], containing_triangle[1], point]
    triangle2 = [containing_triangle[1], containing_triangle[2], point]
    triangle3 = [containing_triangle[2], containing_triangle[0], point]

    # Add 3 new triangles to the list of triangles
    triangles.append(triangle1)
    triangles.append(triangle2)
    triangles.append(triangle3)

    legalize_edge(point, triangle1, triangles)
    legalize_edge(point, triangle2, triangles)
    legalize_edge(point, triangle3, triangles)

def randomized_incremental_delaunay(pointSet):
    # Find the triangle that contains all the points.
    a, b, c = find_inclusive_triangle(pointSet)

    triangles = [[a, b, c]]

    # For each point in the point set, add point to the triangulation.
    for point in pointSet:
        add_point(point, triangles)

    # Remove all triangles that have a common vertex with the inclusive triangle.
    return [triangle for triangle in triangles if not (a in triangle or b in triangle or c in triangle)]