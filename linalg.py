"""
Linear algebra functions duplicated from https://github.com/dwpaley/orient.
A small and undocumented selection of matrix operations working on lists (and
nested lists) of ints and floats.
"""
from math import sqrt

def norm(vec):
  return sqrt(sum([x**2 for x in vec]))

def dot(a, b):
  return sum([x*y for x, y in zip(a,b)])

def cross(a, b):
  return [a[1]*b[2] - a[2]*b[1],
          a[2]*b[0] - a[0]*b[2],
          a[0]*b[1] - a[1]*b[0]]

def inv33(mat):
  # cofactor matrix elements
  c00 = + mat[1][1]*mat[2][2] - mat[2][1]*mat[1][2]
  c01 = - mat[1][0]*mat[2][2] + mat[1][2]*mat[2][0]
  c02 = + mat[1][0]*mat[2][1] - mat[2][0]*mat[1][1]
  c10 = - mat[0][1]*mat[2][2] + mat[2][1]*mat[0][2]
  c11 = + mat[0][0]*mat[2][2] - mat[2][0]*mat[0][2]
  c12 = - mat[0][0]*mat[2][1] + mat[2][0]*mat[0][1]
  c20 = + mat[0][1]*mat[1][2] - mat[1][1]*mat[0][2]
  c21 = - mat[0][0]*mat[1][2] + mat[1][0]*mat[0][2]
  c22 = + mat[0][0]*mat[1][1] - mat[1][0]*mat[0][1]

  # cofactor matrix and its transpose
  c = [[c00, c01, c02],
       [c10, c11, c12],
       [c20, c21, c22]]
  c_t = map(list, zip(*c))

  det = c00*mat[0][0] + c01*mat[0][1] + c02*mat[0][2]

  inv = [[el/det for el in row] for row in c_t]

  return inv

def mat_vec_3_product(m, v):
  r0 = sum([x*y for x, y in zip(m[0], v)])
  r1 = sum([x*y for x, y in zip(m[1], v)])
  r2 = sum([x*y for x, y in zip(m[2], v)])
  return [r0, r1, r2]

def centroid(vecs):
  '''vecs is a list of lists'''
  result = []
  for i in range(len(vecs[0])):
    elements = [v[i] for v in vecs]
    mean = sum(elements) / len(elements)
    result.append(mean)
  return result

def vec_sum(v1, v2):
  result = []
  for i in range(len(v1)):
    result.append(v1[i] + v2[i])
  return result



