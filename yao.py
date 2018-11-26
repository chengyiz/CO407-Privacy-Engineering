# Chengyi Zhang cz5818
# Rui Jia rj418
# yao garbled circuit evaluation v1. simple version based on smart
# naranker dulay, dept of computing, imperial college, october 2018
import random
import json
import crypto

class Wire:
    def __init__(self, index):
        self.index = index # id
        self.keys = [crypto.generate_key(), crypto.generate_key()] # two keys
        self.p = random.randint(0,1) # generate randomly
        self.ext_value = None # not evaluated yet
        
    def set_value(self, value, xor):
        # use xor'ed value for in and out is more convenient
        self.ext_value = (value ^ self.p) if xor==True else value 
        
    def clean(self):
        # remove info that Bob has no access to
        self.keys = [None, None]
        self.p = None
        self.ext_value = None
        
    def set_key(self, key):
        # set the real key looked up by Bob
        self.real_key = key
        
    def __str__(self):
        if self.ext_value!=None:
            return "index: {}, p: {}, ext_value: {}".format(\
                self.index, self.p, self.ext_value)
        return "index: {}, p: {}".format(self.index, self.p)
        
        
        
class Gate:
    
    # At least one input for the gate
    def __init__(self, ID, inwire_1, outwire, gate_type, inwire_2=None):
        self.ID = ID
        self.inwire_1 = inwire_1
        self.gate = gate_type
        if gate_type == 'NOT':
            assert inwire_2==None, "NOT gate cannot have two input wires"
        self.inwire_2 = inwire_2
        self.outwire = outwire
        
        result = {}
        # generate the truth table
        # for any real input values, encrypt the output key and xor'ed value
        # then assign the encrypted value to the corresponding xor'ed input
        if gate_type == 'NOT':
            for a in [0,1]:
                first = a ^ self.inwire_1.p
                value = (1-a) ^ self.outwire.p
                key = self.outwire.keys[1-a]
                result[str(first)] = \
                    crypto.encrypt(key, value, self.inwire_1.keys[a])
        else:
            for a in [0, 1]:
                for b in [0, 1]: 
                    first = a ^ self.inwire_1.p
                    second = b ^ self.inwire_2.p
                    if gate_type == 'AND':
                        o_ab = a & b
                    elif gate_type == 'OR':
                        o_ab = a | b
                    elif gate_type == 'XOR':
                        o_ab = a ^ b
                    elif gate_type == 'NAND':
                        o_ab = not (a & b)
                    elif gate_type == 'NOR':
                        o_ab = not (a | b)
                    elif gate_type == 'XNOR':
                        o_ab = not (a ^ b)
                    key = self.outwire.keys[o_ab]
                    value = o_ab ^ self.outwire.p
                    result[str(first)+str(second)] = \
                        crypto.encrypt(key, value, self.inwire_1.keys[a], \
                                       self.inwire_2.keys[b])
        self.table =  result
        
    # Look up table, decrypt and get correct key and xor'ed value of output wire 
    def set_out(self):
        key = str(self.inwire_1.ext_value) + str(self.inwire_2.ext_value) \
            if self.gate != 'NOT' else str(self.inwire_1.ext_value) 
        unknown = self.table[key]
        wire1 = self.inwire_1
        key_idx = wire1.ext_value ^ wire1.p
        if self.gate == 'NOT':
            (key, value) = crypto.decrypt(unknown, wire1.keys[key_idx])
        else:
            wire2 = self.inwire_2
            key_idx_1 = wire2.ext_value ^ wire2.p
            (key, value) = crypto.decrypt(unknown, \
                                   wire1.keys[key_idx], wire2.keys[key_idx_1])
        self.outwire.set_value(value, False)
        
    # Similar to the one above, only does not need the p-bits and original keys
    def set_out_secure(self):
        key = str(self.inwire_1.ext_value) + str(self.inwire_2.ext_value) \
            if self.gate != 'NOT' else str(self.inwire_1.ext_value)  
        unknown = self.table[key]
        if self.gate == 'NOT':
            (key, value) = crypto.decrypt(unknown, self.inwire_1.real_key)
        else:
            (key, value) = crypto.decrypt(unknown, self.inwire_1.real_key, \
                                          self.inwire_2.real_key)
        self.outwire.set_value(value, False)
        self.outwire.set_key(key)
                
    def __str__(self):
        if self.gate == 'NOT':
            result = "type: {}, wires: {}, table: {}".format(\
                self.gate,[self.inwire_1.index, self.outwire.index], self.table)
        else:
            result = "type: {}, wires: {}, table: {}".format(\
                self.gate, [self.inwire_1.index, self.inwire_2.index, \
                            self.outwire.index], self.table)            
        return "ID: " + str(self.ID) + ", " + result

class Circuit:
    def __init__(self, json_circuit):
        self.gen_circuit(json_circuit)

    def gen_circuit(self, circuit):
        self.alice = circuit['alice'] if 'alice' in circuit else []
        self.bob = circuit['bob'] if 'bob' in circuit else []
        wire_ids = find_wires(circuit)
        wires = []
        for i in range(max(wire_ids)):
            wires.append(Wire(i+1))
        self.wires = wires
        
        gates = []
        for i, gate in enumerate(circuit['gates']):
            if gate['type'] == 'NOT':
                gates.append(Gate(gate['id'], inwire_1=wires[gate['in'][0]-1], \
                                  outwire=wires[gate['id']-1], \
                                  gate_type=gate['type']))
            else:
                gates.append(Gate(gate['id'], wires[gate['in'][0]-1], \
                                  wires[gate['id']-1], gate['type'], \
                                  wires[gate['in'][1]-1]))
        
        self.gates = gates
        outs = []
        for idx in circuit['out']:
            outs.append(self.wires[idx-1])
        self.outs = outs
            
    def evaluate(self, alice_input, bob_input=[]):
        if self.alice:          
            for i in range(len(self.alice)):
                self.wires[self.alice[i]-1].set_value(alice_input[i], False)
        if self.bob:

            assert bob_input!=[], "Need input from Bob"
            for i in range(len(self.bob)):
                self.wires[self.bob[i]-1].set_value(bob_input[i], False)
                    
        for gate in self.gates:
            gate.set_out()
        
        result = []
        for out in self.outs:
            result.append(out.ext_value ^ out.p)
        print("Alice[1,2] = {}, Bob[1,2] = {}, Output = {}".format(alice_input, bob_input, result))
        return result    
    
    def evaluate_secure(self, alice_input, alice_keys, bob_input=[], bob_keys=[]):
        if self.alice:          
            for i in range(len(self.alice)):
                self.wires[self.alice[i]-1].set_value(alice_input[i], False)
                self.wires[self.alice[i]-1].set_key(alice_keys[i])
                
        if self.bob:
            assert bob_input!=[], "Need input from Bob"
            for i in range(len(self.bob)):
                self.wires[self.bob[i]-1].set_value(bob_input[i], False)
                self.wires[self.bob[i]-1].set_key(bob_keys[i])
              
        for gate in self.gates:
            gate.set_out_secure()
        
        result = []
        for out in self.outs:
            result.append(out.ext_value)
        return result            
    
    def clean(self):
        for wire in self.wires:
            wire.clean()
    
def find_wires(circuit_dict):
    wires = []
    for key in circuit_dict:
        if key == 'gates':
            for gate in circuit_dict['gates']:
                wires.append(gate['id'])
                wires.extend(gate['in'])
        elif key == 'out':
            wires.extend(circuit_dict['out'])
        elif key == 'name':
            pass
        else:
            wires.extend(circuit_dict[key])
    return wires
    
#gen_circuit("./json/f.bool.json", 8)