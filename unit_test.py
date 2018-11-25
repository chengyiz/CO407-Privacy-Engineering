import unittest
import json
import yao

class TestGarbledCircuit(unittest.TestCase):

    def test_smart(self):
        with open("./json/f.smart.json") as json_file:
            json_circuits = json.load(json_file)
    
        for json_circuit in json_circuits['circuits']:
            print("------------SMART----------")
            
            #circuit.evaluate([1,0],[1,0])
    
            for a in [0,1]:
                for b in [0,1]:
                    for c in [0,1]:
                        for d in [0,1]:
                            exp = [(a&c) | (b^d)]
                            circuit = yao.Circuit(json_circuit)                    
                            act = circuit.evaluate([a,b], [c,d])
                            self.assertEqual(act, exp, str(a)+str(b)+str(c)+str(d))
                            
                            
    def test_bool(self):
        with open("./json/f.bool.json") as json_file:
            json_circuits = json.load(json_file)
        
        for json_circuit in json_circuits['circuits']:
            print("------------BOOL----------")
            
            name = json_circuit['name']
            for a in [0,1]:
                for b in [0,1]:
                    if "AND" == name.split()[0]:
                        exp = a & b
                    elif "OR" == name.split()[0]:
                        exp = a | b
                    elif "NOT" == name.split()[0]:
                        exp = not a
                    elif "XOR" == name.split()[0]:
                        exp = a ^ b
                    elif "NOR" == name.split()[0]:
                        exp = not (a | b)
                    elif "NAND" == name.split()[0]:
                        exp = not (a & b)
                    elif "XNOR" == name.split()[0]:
                        exp = not (a ^ b)
                    elif "implies" in name:
                        exp = (not a) | b
                    elif "AA'" in name:
                        exp = a & (not a)
                    elif "A+A'" in name:
                        exp = a | (not a)
                    else:
                        break
                    exp = [exp]
                    circuit = yao.Circuit(json_circuit) 
                    act = circuit.evaluate([a], [b])
                    self.assertEqual(act, exp, str(a)+str(b))
                    
    def test_max(self):
        with open("./json/f.max.json") as json_file:
            json_circuits = json.load(json_file)
        
        for json_circuit in json_circuits['circuits']:
            print("-----------MAX-----------")
            
            name = json_circuit['name']
            for a in [0,1]:
                for b in [0,1]:
                    for c in [0,1]:
                        for d in [0,1]:
                            circuit = yao.Circuit(json_circuit) 
                            act = circuit.evaluate([a,b], [c,d])
                            exp = max([a,b],[c,d])
                            self.assertEqual(act, exp, str(a)+str(b)+str(c)+str(d))
                            
    
    def test_nand(self):
        with open("./json/f.nand.json") as json_file:
            json_circuits = json.load(json_file)
        
        for json_circuit in json_circuits['circuits']:
            print("-----------MAX-----------")
            
            name = json_circuit['name']
            for a in [0,1]:
                for b in [0,1]:
                    if "AND" == name.split()[0]:
                        print("-----AND-----")
                        exp = a & b
                    elif "OR" == name.split()[0]:
                        print("-----OR-----")
                        exp = a | b
                    elif "NOT" == name.split()[0]:
                        print("-----NOT-----")
                        exp = not a
                    elif "XOR" == name.split()[0]:
                        print("-----XOR-----")
                        exp = a ^ b
                    elif "NOR" == name.split()[0]:
                        print("-----NOR-----")
                        exp = not (a | b)
                    elif "NAND" == name.split()[0]:
                        exp = not (a & b)
                    elif "XNOR" == name.split()[0]:
                        print("-----XNOR-----")
                        exp = not (a ^ b)
                    else:
                        break                    
                    circuit = yao.Circuit(json_circuit) 
                    act = circuit.evaluate([a], [b])
                    exp = [exp]
                    self.assertEqual(act, exp, str(a)+str(b))       
                    
    def test_min(self):
        with open("./json/f.min.json") as json_file:
            json_circuits = json.load(json_file)
        
        for json_circuit in json_circuits['circuits']:
            print("-----------MIN-----------")
            
            name = json_circuit['name']
            for a in [0,1]:
                for b in [0,1]:
                    for c in [0,1]:
                        for d in [0,1]:
                            circuit = yao.Circuit(json_circuit) 
                            act = circuit.evaluate([a,b], [c,d])
                            exp = min([a,b],[c,d])
                            print("exp={}".format(exp))
                            self.assertEqual(act, exp, str(a)+str(b)+str(c)+str(d)) 
                            
    def test_add_1(self):
        with open("./json/f.add.json") as json_file:
            json_circuits = json.load(json_file)
        
        for json_circuit in json_circuits['circuits'][0:1]:
            print("-----------ADD 1BIT-----------")
            
            name = json_circuit['name']
            for a in [0,1]:
                for b in [0,1]:
                    for c in [0,1]:
                        circuit = yao.Circuit(json_circuit) 
                        act = circuit.evaluate([a,b], [c])
                        exp = [a^(b^c), (b&c) | (a&(b^c))]
                        print("exp={}".format(exp))
                        self.assertEqual(act, exp, str(a)+str(b)+str(c))       
                    
    def test_add_2(self):
        with open("./json/f.add.json") as json_file:
            json_circuits = json.load(json_file)
        
        for json_circuit in json_circuits['circuits'][1:]:
            print("-----------ADD 2BIT-----------")
            
            name = json_circuit['name']
            for c in range(2):
                for a in range(4):
                    for b in range(4):
                        a_bits = bits(a,2)
                        b_bits = bits(b,2)
                        a_bits.reverse()
                        b_bits.reverse()
                        a_input = [c]+a_bits
                        b_input = b_bits
                        circuit = yao.Circuit(json_circuit) 
                        act = circuit.evaluate(a_input, b_input)
                        exp = bits(a+b+c,3)
                        exp.reverse()
                        print("a={},b={},c={},exp={}".format(a,b,c,exp))
                        self.assertEqual(act, exp, str(a)+str(b)) 
                        
    def test_cmp(self):
        with open("./json/f.cmp.json") as json_file:
            json_circuits = json.load(json_file)
        
        for json_circuit in json_circuits['circuits']:
            print("-----------ADD 2BIT-----------")
            
            name = json_circuit['name']
            for a in range(2):
                for b in range(2):
                    a_bits = bits(a,2)
                    b_bits = bits(b,2)
                    circuit = yao.Circuit(json_circuit) 
                    act = circuit.evaluate(a_bits, b_bits)
                    if a==b:
                        exp = bits(0,2)
                    elif a>b:
                        exp = bits(1,2)
                    elif a<b:
                        exp = bits(3,2)
                    print("a={},b={},exp={}".format(a,b,exp))
                    self.assertEqual(act, exp, str(a)+str(b))      



def bits(num, width):			# convert number into a list of bits
    # example: bits(num=6, width=5) will return [0, 0, 1, 1, 0]
    # use [int(k) for k in format(num, 'b').zfill(width)] for older Pythons
    return [int(k) for k in f'{num:0{width}b}']


if __name__ == '__main__':
    unittest.main(exit=False)