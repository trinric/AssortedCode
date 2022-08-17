import math
import random

# Generates a voronoi diagram by finding its respective delaunay triangulation.

def circumcenter(p1, p2, p3):
    # A clever way to find the cirumcenter without finding perp bisectors.
    ax = p1[0]
    ay = p1[1]
    bx = p2[0]
    by = p2[1]
    cx = p3[0]
    cy = p3[1]
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    ux = ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx * cx + cy * cy) * (ay - by)) / d
    uy = ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) + (cx * cx + cy * cy) * (bx - ax)) / d
    return (ux, uy)

def distance(p, q):
    return math.sqrt(sum((px-qx) ** 2.0 for px, qx in zip(p, q)))

def find_invalid(point, triangles):
    """ Determines if a point falls within any of the existing triangles"""
    invalid = []
    polygonhole = []
    for t in triangles:
        cc = circumcenter(t[0], t[1], t[2])
        d = distance(t[0], cc)
        if distance(point, cc) < d:
            invalid.append(t)
            polygonhole.append([t[0], t[1]])
            polygonhole.append([t[1], t[2]])
            polygonhole.append([t[2], t[0]])

    return invalid, polygonhole 

def remove_duplicate_edges(edges):
    for e in edges:
        if e[0][0] > e[1][0]:
            e[0], e[1] = e[1], e[0]
    edges = sorted(edges, key = lambda e: e[0][0])
    # i = 0
    # prev = edges[0]
    # while True:
    #     i = i + 1
    #     if i >= len(edges) - 1:
    #         break
    #     new = edges[i]
    #     if same_edge(prev, new):
    #         edges.remove(prev)
    #     prev = new
    new = []
    for e in edges:
        if edges.count(e) == 1:
            new.append(e)
    return new


def fill_polygon_hole(polygonhole, triangles, point):
    for edge in polygonhole:
        triangle = [edge[0], edge[1], point]
        triangles.append(triangle)
    return triangles
    

def same_edge(e1, e2):
    if e1[0] == e2[0] and e1[1] == e2[1]:
        return True
    elif e1[0] == e2[1] and e1[1] == e2[0]:
        return True
    else:
        return False



def generate_delaunay():
    # Genenerate points
    maxX = 900
    maxY = 900
    n = 30
    points = []
    for i in range(n):
        points.append([random.randrange(0, maxX), random.randrange(0, maxY)])
    # make starting triangle outside whole thing
    triangles = []
    starting_triangle = [(0,0), (0, 2 * maxY), (2 * maxX, 0)]
    triangles.append(starting_triangle)
    #keep adding points
    for p in points:
        invalid, polygonhole = find_invalid(p, triangles)
        polygonhole = remove_duplicate_edges(polygonhole)
        for t in invalid:
            triangles.remove(t)
        fill_polygon_hole(polygonhole, triangles, p)

    return triangles


def test():
    starting_triangle = [[0, 0], [0, 20], [20, 0]]
    triangles = [starting_triangle]
    p1 = [5, 3]
    inv, ph = find_invalid(p1, triangles)
    for t in inv:
        triangles.remove(t)
    new = fill_polygon_hole(ph, triangles, p1)
    print(triangles)
    # - to here works fine
    print("----------------------")
    p2 = [5, 6]
    inv, ph = find_invalid(p2, triangles)
    print(ph)
    ph = remove_duplicate_edges(ph)
    print(ph)
    for t in inv:
        triangles.remove(t)
    new = fill_polygon_hole(ph, triangles, p2)


#test() 