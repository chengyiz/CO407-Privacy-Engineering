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
                            exp = (a&c) | (b^d)
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
                            #self.assertEqual(act, exp, str(a)+str(b))    
                    
                    

if __name__ == '__main__':
    unittest.main(exit=False)