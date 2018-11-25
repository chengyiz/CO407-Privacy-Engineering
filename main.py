
# yao garbled circuit evaluation v1. simple version based on smart
# naranker dulay, dept of computing, imperial college, october 2018

import json	# load
import sys	# argv

import ot	# alice, bob
import util	# ClientSocket, log, ServerSocket
import yao	# Circuit

# Alice is the circuit generator (client) __________________________________

#def alice(filename):
  #socket = util.ClientSocket()

  #with open(filename) as json_file:
    #json_circuits = json.load(json_file)

  #for json_circuit in json_circuits['circuits']:
    # << removed >>

# Bob is the circuit evaluator (server) ____________________________________

#def bob():
  #socket = util.ServerSocket()
  #util.log(f'Bob: Listening ...')
  #while True:
    # << removed >>

# local test of circuit generation and evaluation, no transfers_____________

def local_test(filename):
  with open(filename) as json_file:
    json_circuits = json.load(json_file)

  for json_circuit in json_circuits['circuits']:
    print("------------"+json_circuit['name'] +"----------")
    circuit = yao.Circuit(json_circuit)
    #circuit.evaluate([1,0],[1,0])

    for a in [0,1]:
      for b in [0,1]:
        for c in [0,1]:
          for d in [0,1]:
              circuit.evaluate([a,b], [c,d])
# main _____________________________________________________________________

def main():
  behaviour = sys.argv[1]
  if   behaviour == 'alice': alice(filename=sys.argv[2])
  elif behaviour == 'bob':   bob()
  elif behaviour == 'local': local_test(filename=sys.argv[2])

if __name__ == '__main__':
  main()

# __________________________________________________________________________


