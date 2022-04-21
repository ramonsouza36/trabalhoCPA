# Problema do arranjo minimo 
# usando simulated annealing
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

def simulated_annealing(nodes, rnd, max_iter, 
  start_temperature, alpha):
  # solve using simulated annealing
  curr_temperature = start_temperature
  err = error(nodes)
  iteration = 0
  interval = (int)(max_iter / 10)
  while iteration < max_iter and err > 0.0:
    adj_route = adjacent(nodes, rnd)
    adj_err = error(adj_route)

    if adj_err < err:  # better route so accept
      nodes = adj_route; err = adj_err
    else:          # adjacent is worse
      accept_p = \
        np.exp((err - adj_err) / curr_temperature)
      p = rnd.random()
      if p < accept_p:  # accept anyway
        nodes = adj_route; err = adj_err 
      # else don't accept

    if iteration % interval == 0:
      print("iter = %6d" % \
      (iteration, err, curr_temperature))

    if curr_temperature < 0.00001:
      curr_temperature = 0.00001
    else:
      curr_temperature *= alpha
    iteration += 1

  return nodes       

def main():
  filename = 'nos4.mtx'
  header = "100 100"
  #filename = 'Trefethen_200.mtx'
  #header = "200 200"
  #filename = 'Trefethen_500.mtx'
  #header = "500 500"
  #filename = 'sherman1.mtx'
  #header = "1000 1000"
  #filename = 'olm2000.mtx'
  #header = "2000 2000"    
  conteudo = open(filename,'r')
  nodes = []
  cont = 0
  for linha in conteudo.readlines():
    if "%" not in linha:
        if header not in linha:   
          teste = linha.split(' ')
          x = int(teste[0])
          y = int(teste[1])
          if x > y:
                cont+= x-y
          else: 
            cont+=y-x 
          nodes.append(x)
          nodes.append(y)
  rnd = np.random.RandomState(4) 
  max_iter = 300000
  start_temperature = 10000.0
  alpha = 0.95
  #alpha = 0.99

  print("\nSettings: ")
  print("max_iter = %d " % max_iter)
  print("start_temperature = %0.1f " \
    % start_temperature)
  print("alpha = %0.2f " % alpha) 
  print("Soma inicial: ",cont)
  soln = simulated_annealing(nodes, rnd, max_iter, 
    start_temperature, alpha)
  print("Finished solve() ")

  dist = total_dist(soln)
  print("\nMelhor soma encontrada = %0.1f " % dist)
  
if __name__ == "__main__":
  main()