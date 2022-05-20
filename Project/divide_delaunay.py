from delaunay_helpers import is_in_circumcircle, point_on_right, point_on_left, left_test


class Edge:
    """
    Edge data structure that simplifies the algorithm
    """

    def __init__(self, from_, to):
        self.from_ = from_  # Origin
        self.to = to  # Destination

        self.sym = None  # Same edge, backwards
        self.nextCCW = self  # While traversing edge ring, next counter-clockwise edge
        self.nextCW = self  # While traversing edge ring, previous clockwise edge

        self.deleted = False  # Deleted flag


def div_and_conq_delaunay(points):
    """
    Use this function to compute the Delaunay triangulation of a set of points.
    Triangulate the points using the divide and conquer delaunay triangulation algorithm.
    """

    # Validate the input size
    if len(points) < 2:
        return

    # Sort points by x coordinate, y is a tiebreaker
    points.sort(key=lambda point: (point[0], point[1]))

    # Remove duplicates.
    i = 0
    while i < len(points) - 1:
        if points[i] == points[i + 1]:
            del points[i]
        else:
            i += 1

    # Triangulate
    edges = []
    div_and_conq_triangulate(points, edges)

    # Remove edges that are not part of the triangulation
    edges = [e for e in edges if e.deleted is False]

    return edges


def div_and_conq_triangulate(S, edges):
    """
    Computes the Delaunay triangulation of a point set S and returns two edges, le and re,
    which are the counterclockwise convex hull edge out of the leftmost vertex and the clockwise
    convex hull edge out of the rightmost vertex, respectively.
    """

    # Base case: 2 points
    if len(S) == 2:
        edge = create_edge(S[0], S[1], edges)
        return edge, edge.sym

    # Base case: 3 points
    elif len(S) == 3:
        # Create edge S[0]-S[1] and edge S[1]-S[2]
        edge1 = create_edge(S[0], S[1], edges)
        edge2 = create_edge(S[1], S[2], edges)
        update_next_prev(edge1.sym, edge2)

        # Create edge S[2]-S[0]
        det = left_test(S[2], [edge1.from_, edge1.to])

        # Right
        if det < 0:
            connect(edge2, edge1, edges)
            return edge1, edge2.sym
        # Left
        elif det > 0:
            edge3 = connect(edge2, edge1, edges)
            return edge3.sym, edge3
        # Points are linear
        else:
            return edge1, edge2.sym

    # Recurively triangulate the left and right halves
    else:
        m = len(S) // 2
        ldo, ldi = div_and_conq_triangulate(S[:m], edges)
        rdi, rdo = div_and_conq_triangulate(S[m:], edges)
        ldo_r, rdo_r = merge(ldo, ldi, rdi, rdo, edges)

        return ldo_r, rdo_r


def merge(ldo, ldi, rdi, rdo, edges):
    """
    Takes 2 halves of the triangulation and merges them into a single triangulation.
    While doing so it uses previosly calculated values of these halves.
    Reference: https://github.com/alexbaryzhikov/triangulation
    """
    # Find the upper base of the halves
    while True:
        if point_on_right(rdi.from_, [ldi.from_, ldi.to]):
            # Advance to the next edge on the convex hull of L.
            ldi = ldi.sym.nextCCW
        elif point_on_left(ldi.from_, [rdi.from_, rdi.to]):
            # Advance to the next edge on the convex hull of R.
            rdi = rdi.sym.nextCW
        else:
            break

    # Connect the upper base of L and R
    base = connect(ldi.sym, rdi, edges)

    # Adjust ldo and rdo
    if ldi.from_[0] == ldo.from_[0] and ldi.from_[1] == ldo.from_[1]:
        ldo = base
    if rdi.from_[0] == rdo.from_[0] and rdi.from_[1] == rdo.from_[1]:
        rdo = base.sym

    # Merge two halves
    while True:
        # Locate the first R and L points to be encountered by the diving bubble.
        rcand, lcand = base.sym.nextCCW, base.nextCW

        # If both lcand and rcand are invalid, then base is the lower common tangent.
        v_rcand, v_lcand = point_on_right(
            rcand.to, [base.from_, base.to]), point_on_right(lcand.to, [base.from_, base.to])
        if not (v_rcand or v_lcand):
            break

        # Delete R edges out of base.to that fail the circle test.
        if v_rcand:
            while point_on_right(rcand.nextCCW.to, [base.from_, base.to]) and is_in_circumcircle(base.to, base.from_, rcand.to, rcand.nextCCW.to):
                t = rcand.nextCCW
                mark_edge_deleted(rcand)
                rcand = t

        # Symmetrically, delete L edges.
        if v_lcand:
            while point_on_right(lcand.nextCW.to, [base.from_, base.to]) and is_in_circumcircle(base.to, base.from_, lcand.to, lcand.nextCW.to):
                t = lcand.nextCW
                mark_edge_deleted(lcand)
                lcand = t

        # The next cross edge is to be connected to either lcand.to or rcand.to.
        # If both are valid, then choose the appropriate one using the in_circle test.
        if not v_rcand or (v_lcand and is_in_circumcircle(rcand.to, rcand.from_, lcand.from_, lcand.to)):
            # Add cross edge base from rcand.to to base.to.
            base = connect(lcand, base.sym, edges)
        else:
            # Add cross edge base from base.from_ to lcand.to
            base = connect(base.sym, rcand.sym, edges)

    return ldo, rdo


def create_edge(from_, to, edges):
    """
    Creates an edge, add it to edges, and return it.
    """

    edge = Edge(from_, to)
    edge_sym = Edge(to, from_)

    edge.sym = edge_sym
    edge_sym.sym = edge

    edges.append(edge)
    return edge


def update_next_prev(e1, e2):
    """
    Either combines e1 and e2 into a single edge, or seperates them.
    Which one is determined by the orientation of e1 and e2.
    """

    if e1 == e2:
        return

    e1.nextCCW.nextCW = e2
    e2.nextCCW.nextCW = e1

    # Swap a.nextCCW and b.nextCCW
    e1.nextCCW, e2.nextCCW = e2.nextCCW, e1.nextCCW


def connect(a, b, edges):
    """
    Connecting destination of a with the origin of b with an edge
    O(1) time and O(1) space
    """
    e = create_edge(a.to, b.from_, edges)

    # Maintain the nextCCW and nextCW values
    update_next_prev(e, a.sym.nextCW)
    update_next_prev(e.sym, b)

    return e


def mark_edge_deleted(e):
    """
    Delete edge from the edge list
    O(1) time and O(1) space
    """

    # Update the e.nextCCW' and e.nextCW's values
    update_next_prev(e, e.nextCW)
    update_next_prev(e.sym, e.sym.nextCW)

    # Mark the edge to be deleted
    e.deleted = True
    e.sym.deleted = True