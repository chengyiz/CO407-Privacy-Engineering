# Chengyi Zhang cz5818
# Rui Jia rj418
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

def alice(json_circuit, circuit, alice, bob=[]):
    socket = util.ClientSocket()
    
    # create and send the prime group to Bob
    primeGroup = util.prime_group
    socket.send_wait(primeGroup)
    
    output = "  Alice{} = ".format(circuit.alice)
    for val in alice:
        output = output + str(val) + ' '
    output = output +" Bob{} = ".format(circuit.bob)
    for val in bob:
        output = output + str(val) + ' '
    output = output + "  Outputs{} = ".format(json_circuit['out'])
    #print(output)
    
    # Alice's input wires and corresponding keys
    wires_alice = [circuit.wires[idx-1] for idx in circuit.alice]
    keys_alice = [wires_alice[i].keys[alice[i]] for i in range(len(alice))]
    
    # xor the input values
    alice = [alice[i]^wires_alice[i].p for i in range(len(circuit.alice))]
    # p-bits of output wires
    p = [out.p for out in circuit.outs]
    
    # Copy the circuit and remove secret info
    copy_ = copy.deepcopy(circuit)
    copy_.clean()
    
    # Send necessary to Bob, note that despite we create values of Bob here, 
    # this knowledge is not used by Alice in OT or garbled circuit evaluation
    # 
    dic = {'circuit': copy_, \
        'keys_a': keys_alice, \
        'p_out': p, \
        'alice': alice, \
        'bob': bob}        
    socket.send_wait(dic)
    
    c = ot.generate_random_int(primeGroup)
        
    # Find Bob's input wires, then use OT to transfer correct info to Bob with
    # Alice knowing any info
    wires_bob = [circuit.wires[idx-1] for idx in circuit.bob]
    for wire_bob in wires_bob:
        # step1: send c to bob and waiting for h_0
        h_0 = socket.send_wait(c)
      
        # step3: receive h_0 from bob
        #           send c_1, e_0, e_1 to bob
        m_0 = wire_bob.keys[0] + bytes([0^wire_bob.p])
        m_1 = wire_bob.keys[1] + bytes([1^wire_bob.p])
        ot_status = socket.send_wait(ot.send_parameters\
                                     (c, h_0, m_0, m_1, primeGroup))
    res = socket.send_wait("start evaluate")
    #time.sleep(0.01)
    for val in res:
        output = output + str(val) + ' '
    print(output)
                

# Bob is the circuit evaluator (server) ____________________________________

def bob():
    socket = util.ServerSocket()
    util.log(f'Bob: Listening ...')
    while True:
        primeGroup = socket.receive()
        socket.send("pG received")
        dic = socket.receive()
        socket.send("circuit received")
        #time.sleep(0.1)
        circuit = dic['circuit']
        keys_alice = dic['keys_a']
        p_out = dic['p_out']
        alice = dic['alice']
        # Input values of Bob here, use this in OT and GC evaluation
        bob = dic['bob']
        #bob = [random.randint(0,1) for i in range(len(circuit.bob))]
        #print("bob={}".format(bob))
        keys_bob = []
        
        
        for i in range(len(circuit.bob)):
            # step2: bob receives c from alice
            #          generates x from (Z/qZ)
            #            chooses one public key from alice
            #             and waiting for c_1, e_0, e_1
            c = socket.receive()
            x = ot.generate_random_int(primeGroup)
            h_0 = ot.generate_h_b(x, c, bob[i], primeGroup)
        
            param = socket.send_wait(h_0)
        
            # step4: bob receives c_1, e_0, e_1 from alice
            #          calculate m_b
            m_b = ot.calculate_m_b(x, param[0], param[1], param[2], bob[i], \
                                   primeGroup) 
            bob[i] = m_b[-1]
            keys_bob.append(m_b[:-1])
            socket.send("continue")
        
        socket.receive()
        result = circuit.evaluate_secure(alice_input=alice, \
                                         alice_keys=keys_alice, bob_input=bob, \
                                         bob_keys=keys_bob)
        result = [result[i] ^ p_out[i] for i in range(len(p_out))]
        print("Output = {}".format(result))
        #time.sleep(0.01)
        socket.send(result)
    

# local test of circuit generation and evaluation, no transfers_____________

def local_test(filename):
    with open(filename) as json_file:
        json_circuits = json.load(json_file)
      
    for json_circuit in json_circuits['circuits'][0:1]:
        print("------------"+json_circuit['name'] +"----------")
        circuit = yao.Circuit(json_circuit)
        circuit.evaluate([1,0],[1,0])
      
        for a in [0,1]:
            for b in [0,1]:
                for c in [0,1]:
                    for d in [0,1]:
                        circuit.evaluate([a,b], [c,d])
# main _____________________________________________________________________

def to_json(tables, keys, p):
    d = {'tables': tables, \
         'keys': keys, \
         'p': p}
    return d
    


def main():
    behaviour = sys.argv[1]
    if   behaviour == 'alice': 
        print("")
        filename = sys.argv[2]
        with open(filename) as json_file:
            json_circuits = json.load(json_file)
    
        for json_circuit in json_circuits['circuits']:
            circuit = yao.Circuit(json_circuit)
            # Create the truth-table
            print("======= "+json_circuit['name']+" =======")
            for i in range(2**len(json_circuit['alice'])):
                if 'bob' in json_circuit:
                    for j in range(2**len(json_circuit['bob'])):
                        alice(json_circuit, circuit, \
                              util.bits(i, len(json_circuit['alice'])),\
                                    bob=util.bits(j, len(json_circuit['bob'])))
                else:
                    alice(json_circuit, circuit, \
                          util.bits(i, len(json_circuit['alice'])))
            print("")
        #alice(filename=sys.argv[2])
    elif behaviour == 'bob':   bob()
    elif behaviour == 'local': local_test(filename=sys.argv[2])

if __name__ == '__main__':
    main()

# __________________________________________________________________________


