# Chengyi Zhang cz5818
# Rui Jia rj418
# yao garbled circuit evaluation v1. simple version based on smart
# naranker dulay, dept of computing, imperial college, october 2018

import util

OBLIVIOUS_TRANSFERS = True

if OBLIVIOUS_TRANSFERS: # __________________________________________________

  # alice generates c from G
  # bob generates x from (Z/qZ).
  def generate_random_int(primeGroup):  return primeGroup.rand_int()

  # bob sends h_b to alice
  # INPUT: x, c, b
  # OUTPUT: h_0
  def generate_h_b(x, c_from_G, b_chosen_by_bob, primeGroup):
    # x is generated from (Z/qZ) in main
    # bob generates a pair of public keys: h_b and h_1-b
    hs = [0,0]
    hb = primeGroup.gen_pow(x)
    hs[b_chosen_by_bob] = hb
    hs[1-b_chosen_by_bob] = primeGroup.mul(c_from_G, primeGroup.inv(hb))
    # send the h_b
    return hs[0]


  # alice sends c, e0, e1 to bob
  # INPUT: c, h_0, m_0, m_1
  # OUTPUT: c_1, e_0, e_1
  def send_parameters(c, h_0, m_0, m_1, primeGroup):
    # generate h1 by c/h0
    h_1 = primeGroup.mul(c, primeGroup.inv(h_0))
    # alice generates k from (Z/qZ)
    k = primeGroup.rand_int()
    # alice generate a public key by g^k
    c_1 = primeGroup.gen_pow(k)
    # Calculate e_0 and e_1
    e_0 = util.xor_bytes(m_0, util.ot_hash(primeGroup.pow(h_0, k), len(m_0)))
    e_1 = util.xor_bytes(m_1, util.ot_hash(primeGroup.pow(h_1, k), len(m_1)))
    #
    parameters_AliceToBob = []
    parameters_AliceToBob.append(c_1)
    parameters_AliceToBob.append(e_0)
    parameters_AliceToBob.append(e_1)

    return parameters_AliceToBob

  # INPUT: x, c_1, e_0, e_1, b_chosen_by_bob
  # OUTPUT: m_b
  def calculate_m_b(x, c_1, e_0, e_1, b_chosen_by_bob, primeGroup):
    # the same x with generate_h_b
    # calculate m_b and m_1-b
    m_b = util.xor_bytes(e_0, util.ot_hash(primeGroup.pow(c_1, x), len(e_0)))
    m_1_b = util.xor_bytes(e_1, util.ot_hash(primeGroup.pow(c_1, x), len(e_1)))

    if b_chosen_by_bob == 0:    return m_b
    if b_chosen_by_bob == 1:    return m_1_b
    else:
      print("ERROR: calculate m_b !")

# non oblivious transfers, not even a secure channel is used, for testing
else: # ____________________________________________________________________
  print("just for testing.")
  
#b = 1
#m_0 = b'j2xGmb7ab5_9k7AxxS6FPncIu6IMxl0sdOsBQZeIAAg=' + bytes([0])
#m_1 = b'xU9jVohTlsf7rNk1Yd7Qh8kRHJzRDXZph-i9VkE9gF8=' + bytes([1])

#c = generate_random_int()
#x = generate_random_int()
#print("c:{}, x:{}".format(c, x))

#h0 = generate_h_b(x, c, b)
#params = send_parameters(c, h0, m_0, m_1)
#result = calculate_m_b(x, c, params[1], params[2], b)
#print(result)