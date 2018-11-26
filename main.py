
# yao garbled circuit evaluation v1. simple version based on smart
# naranker dulay, dept of computing, imperial college, october 2018

import json	# load
import sys	# argv

import ot	# alice, bob
import util	# ClientSocket, log, ServerSocket
import yao	# Circuit
import time
import copy
import random

# Alice is the circuit generator (client) __________________________________

def alice(filename):
    socket = util.ClientSocket()

    with open(filename) as json_file:
        json_circuits = json.load(json_file)

    for json_circuit in json_circuits['circuits']:
        circuit = yao.Circuit(json_circuit)
    
    for wire in circuit.wires:
        print(wire)
        
    alice = [random.randint(0,1) for i in range(len(circuit.alice))]
    bob = [random.randint(0,1) for i in range(len(circuit.bob))]

    wires_alice = [circuit.wires[idx-1] for idx in circuit.alice]
    wires_bob = [circuit.wires[idx-1] for idx in circuit.bob]
    keys_alice = [wires_alice[i].keys[alice[i]] for i in range(len(alice))]
    keys_bob = [wires_bob[i].keys[bob[i]] for i in range(len(circuit.bob))]
    
    print("Alice =[1,2] = {}, Bob[1,2] = {}".format(alice, bob))
    
    bob = [bob[i]^wires_bob[i].p for i in range(len(circuit.bob))]
    alice = [alice[i]^wires_alice[i].p for i in range(len(circuit.alice))]
    p = [out.p for out in circuit.outs]
    
    copy_ = copy.deepcopy(circuit)
    #copy_.clean()
    
    d = {'circuit': copy_, \
        'keys_a': keys_alice, \
        'keys_b': keys_bob, \
        'p_out': p, \
        'alice': alice,\
        'bob': bob}        
    act = socket.send_wait(d)
    exp = circuit.evaluate(alice, bob)
    
    

  

# Bob is the circuit evaluator (server) ____________________________________

def bob():
    socket = util.ServerSocket()
    util.log(f'Bob: Listening ...')
    while True:
        dic = socket.receive()
        circuit = dic['circuit']
        keys_alice = dic['keys_a']
        keys_bob = dic['keys_b']
        p_out = dic['p_out']
        alice = dic['alice']
        bob = dic['bob']
        #bob = [random.randint(0,1) for i in range(len(circuit.bob))]
        #bob = [bob[i] ^ p_in[i] for i in range(len(p_in))]
        
        result = circuit.evaluate_secure(alice_input=alice, \
                                         alice_keys=keys_alice, bob_input=bob, \
                                         bob_keys=keys_bob)
        result = [result[i] ^ p_out[i] for i in range(len(p_out))]
        print("Output = {}".format(result))
        time.sleep(1)
        socket.send(result)
    

# local test of circuit generation and evaluation, no transfers_____________

#def local_test(filename):
  #with open(filename) as json_file:
    #json_circuits = json.load(json_file)

  #for json_circuit in json_circuits['circuits'][0:1]:
    #print("------------"+json_circuit['name'] +"----------")
    #circuit = yao.Circuit(json_circuit)
    #circuit.evaluate([1,0],[1,0])

    #for a in [0,1]:
      #for b in [0,1]:
        #for c in [0,1]:
          #for d in [0,1]:
              #circuit.evaluate([a,b], [c,d])
# main _____________________________________________________________________

def to_json(tables, keys, p):
    d = {'tables': tables, \
         'keys': keys, \
         'p': p}
    return d
    


def main():
    behaviour = sys.argv[1]
    if   behaviour == 'alice': alice(filename=sys.argv[2])
    elif behaviour == 'bob':   bob()
    elif behaviour == 'local': local_test(filename=sys.argv[2])

if __name__ == '__main__':
    main()

# __________________________________________________________________________


