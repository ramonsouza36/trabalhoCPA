# tsp_annealing.py
# traveling salesman problem 
# using classical simulated annealing
# Python 3.7.6 (Anaconda3 2020.02)
from scipy.io import mmread
import numpy as np

def total_dist(route):
  d = 0.0  # total distance between cities
  n = len(route)
  for i in range(n-1):
    if route[i] < route[i+1]:
      d += (route[i+1] - route[i])
    else:
      d += (route[i] - route[i+1])
  return d

def error(route):
  n = len(route)
  d = total_dist(route)
  min_dist = n-1
  return d - min_dist

def adjacent(route, rnd):
  n = len(route)
  result = np.copy(route)
  i = rnd.randint(n); j = rnd.randint(n)
  tmp = result[i]
  result[i] = result[j]; result[j] = tmp
  return result

def solve(n_cities, rnd, max_iter, 
  start_temperature, alpha):
  # solve using simulated annealing
  curr_temperature = start_temperature
  soln = np.arange(n_cities, dtype=np.int64)
  rnd.shuffle(soln)
  #retirar após pronto
  print("Initial guess: ")
  print(soln)

  err = error(soln)
  iteration = 0
  interval = (int)(max_iter / 10)
  while iteration < max_iter and err > 0.0:
    adj_route = adjacent(soln, rnd)
    adj_err = error(adj_route)

    if adj_err < err:  # better route so accept
      soln = adj_route; err = adj_err
    else:          # adjacent is worse
      accept_p = \
        np.exp((err - adj_err) / curr_temperature)
      p = rnd.random()
      if p < accept_p:  # accept anyway
        soln = adj_route; err = adj_err 
      # else don't accept

    if iteration % interval == 0:
      print("iter = %6d | curr error = %7.2f | \
      temperature = %10.4f " % \
      (iteration, err, curr_temperature))

    if curr_temperature < 0.00001:
      curr_temperature = 0.00001
    else:
      curr_temperature *= alpha
    iteration += 1

  return soln       

def main():
  print("\nBegin TSP simulated annealing demo ")
  #conteudo = mmread('Trefethen_200.mtx')
  conteudo = open('Trefethen_200.mtx','r')
  #print(list(conteudo))
  nodes = []
  for linha in conteudo.readlines():
    if "%" not in linha: 
        teste = linha.split(' ')
        x = int(teste[0])
        y = int(teste[1])
        nodes.append(x)
        nodes.append(y)
  print(nodes)
  num_cities = 200
  print("\nSetting num_cities = %d " % num_cities)
  rnd = np.random.RandomState(4) 
  max_iter = 2500
  start_temperature = 10000.0
  alpha = 0.99

  print("\nSettings: ")
  print("max_iter = %d " % max_iter)
  print("start_temperature = %0.1f " \
    % start_temperature)
  print("alpha = %0.2f " % alpha)
  cont = 0 
  for i in nodes:
        if nodes[i] < nodes[i+1]:
          cont+= (nodes[i+1] - nodes[i])
        else:
          cont+= (nodes[i] - nodes[i+1])
  print("Soma inicial: ",cont)
  print("\nStarting solve() ")
  soln = solve(num_cities, rnd, max_iter, 
    start_temperature, alpha)
  print("Finished solve() ")

  print("\nBest solution found: ")
  print(soln)
  dist = total_dist(soln)
  print("\nTotal distance = %0.1f " % dist)

  print("\nEnd demo ")

if __name__ == "__main__":
  main()