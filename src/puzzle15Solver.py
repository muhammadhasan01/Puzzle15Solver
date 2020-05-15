# Muhammad Hasan - 13518012
# Program : Puzzle15 - Solver
from heapq import heappop, heappush
import time

def print_matrix(matrix):
  for i in range(len(matrix)):
    print(matrix[i], end = ' ');
    if (i % 4 == 3):
      print("")
  print("")

def nilai_kurang(matrix):
  kurang = [0 for i in range(16)]
  for i in range(len(matrix)):
    hitungInversi = 0
    for j in range(i + 1, len(matrix)):
      if (matrix[j] < matrix[i]):
        hitungInversi += 1
    kurang[matrix[i] - 1] = hitungInversi
  
  return kurang

def index_ubin_kosong(matrix):
  for i in range(len(matrix)):
    if (matrix[i] == 16):
      return i

def ubah_matrix_to_alphabet(matrix):
  ret = ""
  alphabet = "abcdefghijklmnopqrstuvwxyz"
  for element in matrix:
    ret += alphabet[element]
  return ret

def nilai_ongkos_g(matrix):
  ret = 0
  for i in range(len(matrix)):
    if (i + 1 != matrix[i]):
      ret += 1
  return ret

def up_matrix(matrix, idx):
  ret_matrix = matrix.copy()
  if ((idx // 4) > 0):
    ret_matrix[idx], ret_matrix[idx - 4] = ret_matrix[idx - 4], ret_matrix[idx]
    return ret_matrix
  else:
    return -1

def down_matrix(matrix, idx):
  ret_matrix = matrix.copy()
  if ((idx // 4) < 3):
    ret_matrix[idx + 4], ret_matrix[idx] = ret_matrix[idx], ret_matrix[idx + 4]
    return ret_matrix
  else:
    return -1

def left_matrix(matrix, idx):
  ret_matrix = matrix.copy()
  if (idx % 4 > 0):
    ret_matrix[idx - 1], ret_matrix[idx] = ret_matrix[idx], ret_matrix[idx - 1]
    return ret_matrix
  else:
    return -1

def right_matrix(matrix, idx):
  ret_matrix = matrix.copy()
  if (idx % 4 < 3):
    ret_matrix[idx], ret_matrix[idx + 1] = ret_matrix[idx + 1], ret_matrix[idx]
    return ret_matrix
  else:
    return -1

matrix_awal = []
for i in range(4):
  inp = list(map(int, input().strip().split(' ')));
  matrix_awal += inp

start_time = time.time()

print("matrix posisi awal:")
print_matrix(matrix_awal)

kurang = nilai_kurang(matrix_awal)
jumlah_kurang_x = 0

print("Didapat nilai kurang untuk setiap ubin-i adalah sebagai berikut:")
for i in range(16):
    print("Nilai kurang ke-" + str(i + 1) + " = " + str(kurang[i]))
    jumlah_kurang_x += kurang[i]
print("")

index_kosong = index_ubin_kosong(matrix_awal)
if (index_kosong % 8 < 4):
  if (index_kosong % 2 == 1):
    jumlah_kurang_x += 1
elif (index_kosong % 2 == 0):
  jumlah_kurang_x += 1

print("Nilai dari sum_{i=1}^{16} kurang(i) + X adalah =", jumlah_kurang_x)
if (jumlah_kurang_x % 2 == 1):
  print("Karena nilai tersebut ganjil kita tidak akan dapat menyelesaikan persoalan.")
  exit()

map_matrix = {}
map_node_to_matrix = {}
depth_node = {}
cost_node = {}
parent_node = {}

matrix_hash = ubah_matrix_to_alphabet(matrix_awal)
cur_node = 1

map_matrix[matrix_hash] = 1
map_node_to_matrix[1] = matrix_awal
depth_node[cur_node] = 0
cost_node[cur_node] = 0
parent_node[cur_node] = cur_node

prioQueue = [(cost_node[cur_node], cur_node)]
found_solution = False

while (prioQueue) and (not found_solution):
  cost, node = heappop(prioQueue)

  matrix_node = map_node_to_matrix[node]
  index_kosong = index_ubin_kosong(matrix_node)

  matrix_ekspansi = []
  matrix_ekspansi.append(up_matrix(matrix_node, index_kosong))
  matrix_ekspansi.append(right_matrix(matrix_node, index_kosong))
  matrix_ekspansi.append(down_matrix(matrix_node, index_kosong))
  matrix_ekspansi.append(left_matrix(matrix_node, index_kosong))

  for matrix in matrix_ekspansi:
    if (matrix == -1):
      continue
    
    matrix_hash = ubah_matrix_to_alphabet(matrix)
    if (matrix_hash in map_matrix):
      continue

    cur_node += 1
    
    fungsi_g = nilai_ongkos_g(matrix)

    map_matrix[matrix_hash] = 1
    map_node_to_matrix[cur_node] = matrix
    depth_node[cur_node] = depth_node[node] + 1
    cost_node[cur_node] = depth_node[cur_node] + fungsi_g
    parent_node[cur_node] = node

    if (fungsi_g == 0):
      found_solution = True
      break

    heappush(prioQueue, (cost_node[cur_node], cur_node))


jumlah_node = cur_node
solusi_node = []

while True:
  solusi_node.append(cur_node)
  if (cur_node == 1):
    break
  cur_node = parent_node[cur_node]

solusi_node = solusi_node[::-1]

print("Karena nilai tersebut genap kita bisa memperoleh solusi!")
print("Solusinya adalah sebagai berikut:")
for i in range(len(solusi_node)):
  print("Langkah ke-" + str(i) + ":")
  print_matrix(map_node_to_matrix[solusi_node[i]])

print("Waktu eksekusi :", (time.time() - start_time) * 1000, "ms")
print("Jumlah node yang dibangkitkan adalah :", jumlah_node)


