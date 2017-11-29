import test_swig
import ecigen

#
# FIX KEY LENGTH sometimes 201
#
__lmda = 200
__n = 6
#
__n_mlm = 10
__kappa_mlm = __n
__rho_mlm = 52
__etap_mlm = 420
#
__arguments = (__lmda, __kappa_mlm, __n_mlm, __rho_mlm, __etap_mlm)
#
####__T = [[0,2,4], [0,1], [3,5], [2], [1]]
#__l = len(__T)
#
####__W = [0, 2, 4]


__T, __W = ecigen.generate(__n, __n*3)

print(__T)
print(__W)


#
def format_key_string(key, bit_length):
    sign_bit = (key[0] == '-')
    if sign_bit:
        key = key[1:]
    #
    key = str(int(sign_bit))+key
    return key.zfill(bit_length)
#
print('----------------------')
#
def encrypt(lmda, n, T, arguments=None):
    pp = test_swig.public_parameters_generate(*arguments)
    pp.generate()
    #
    a = []
    #
    for i in range(n):
        samp = test_swig.encoding()
        samp.samp(pp, 0)
        a.append(samp)
    #
    C = []
    #
    for i in range(len(T)):
        #
        a_prime = []
        #
        for j in range(n):
            samp = test_swig.encoding()
            samp.set_to(a[j])
            samp = pp.enc(samp, 1)
            samp.rerand()
            a_prime.append(samp)
        #
        product = test_swig.encoding()
        product.set_to(a_prime[T[i][0]])
        for j in range(1, len(T[i])):
            product.mult_in_place(a_prime[T[i][j]])
        #
        encoded = pp.enc(product, len(T[i]))
        C.append(encoded)
    #
    product = test_swig.encoding()
    product.set_to(a[0])
    #
    for i in range(1, n):
        product.mult_in_place(a[i])
    #
    encoding = pp.enc(product, n)
    K = pp.ext_as_str(encoding, 0)
    print(len(K))
    #K = format_key_string(pp.get_value_of_mpz(K), lmda)
    K = format_key_string(K, lmda)
    #
    return (K, pp, C)
#
(__K, __pp, __C) = encrypt(__lmda, __n, __T, __arguments)
#
print('----------------------')
#
print('K (first 15 bits): {0}'.format(__K[0:15]))
print('K length: {0}'.format(len(__K)))
#
def decrypt(lmda, n, C, pp, W):
    B = test_swig.encoding()
    B.set_to(C[W[0]])
    #
    for i in range(1, len(W)):
        B.mult_in_place(C[W[i]])
    #
    K_recovered = pp.ext_as_str(B, 0)
    #K_recovered = format_key_string(pp.get_value_of_mpz(K_recovered), lmda)
    K_recovered = format_key_string(K_recovered, lmda)
    #
    return K_recovered
#
__K_recovered = decrypt(__lmda, __n, __C, __pp, __W)
#
print('----------------------')
#
print('K_recovered (first 15 bits): {0}'.format(__K_recovered[0:15]))
print('K_recovered length: {0}'.format(len(__K_recovered)))
#
print('----------------------')
#
print('Keys are the same?: {0}'.format(__K_recovered == __K))
#
print('----------------------')
print()

results = []
for i in range(5, 100):
    __T, __W = ecigen.generate(i, i*3)
    
    __arguments = (__lmda, i, __n_mlm, __rho_mlm, __etap_mlm)
    
    (__K, __pp, __C) = encrypt(__lmda, i, __T, __arguments)
    __K_recovered = decrypt(__lmda, i, __C, __pp, __W)
    print('Keys are the same?: {0}'.format(__K_recovered == __K))
    results.append(__K_recovered == __K)

print(results)
print(all(results))



