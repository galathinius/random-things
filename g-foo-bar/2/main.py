import numpy as np

def make_matrix(n):
  matrix = np.zeros((n, n))

  for i in range(n-1):
    matrix[i][i] = 1
    matrix[i][i + 1] = 1

  matrix[-1][0] = 1
  matrix[-1][-1] = -2

  return matrix

def get_b(pegs):
  b = np.zeros((len(pegs), 1))
  # print b

  for i in range(len(pegs)-1):
    b[i][0] = pegs[i + 1] - pegs[i]

  return b

def are_they_real(res):
  for peg in res:
    if peg[0] < 1:
      return False
  return True

def solution(pegs):
  matrix = make_matrix(len(pegs))
  inverse = np.linalg.inv(matrix)
  b = get_b(pegs)
  result = np.matmul(inverse, b)

  if not are_they_real(result):
    return [-1, -1]

  needed = result[0][0]
  needed *= 3
  needed = int(needed + 0.5)

#   print needed

  if not needed % 3:
    needed /= 3
    return [int(needed), 1]
    

  return [int(needed), 3]
