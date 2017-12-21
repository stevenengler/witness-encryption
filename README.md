# Witness Encryption Implementation
An (insecure) implementation of witness encryption in Python. The library uses a c++ graded multilinear map library.

The witness encryption implementation follows the design from the paper ["Witness Encryption and its Applications"](https://eprint.iacr.org/2013/258.pdf) by Garg et al.

The multilinear map code used is from the forked repository [new-multilinear-maps](https://github.com/stevenengler/new-multilinear-maps), which is described by the paper ["New Multilinear Maps over the Integers"](https://eprint.iacr.org/2015/162.pdf).

Developed by [Steven](https://github.com/stevenengler) and [Alex](https://github.com/alex-norton) for a course project.

## Set-up

To run the code, install [Docker](https://www.docker.com/) and build the Dockerfile. After building the image and running the container, you can access it by running `docker run -it <image-id> /bin/bash`.

## Example

```pycon
>>> from witnessencrypt.graded_witness_encryption import encrypt, decrypt
>>> from witnessencrypt.mmap_ges import MMapGES
>>> from witnessencrypt.ecigen import generate
>>> 
>>> lmbda = 50
>>> n = 10
>>> rho = 52
>>> etap = 420
>>> 
>>> exact_cover_collection, witness = generate(n, 5, 15)
>>> exact_cover_collection = [[y-1 for y in x] for x in exact_cover_collection]
>>> print(exact_cover_collection)
[[1, 3, 4, 6, 9], [1, 2, 4, 6, 8], [2, 5, 6, 7, 9], [5, 6, 7, 8], [1, 6, 7, 9], [2], [1, 2, 4, 7, 8], [6], [3, 5], [9], [5], [0], [0, 2, 3, 6, 8], [1, 2, 3, 8, 9], [0]]
>>> print(witness)
[6, 7, 8, 9, 14]
>>> 
>>> pp = MMapGES(lmbda, n, n, rho, etap)
(eta = 2487)
>>> 
>>> (key, ciphertext) = encrypt(pp, exact_cover_collection)
>>> key_recovered = decrypt(pp, ciphertext, witness)
>>> 
>>> print(key)
00000011100101000000010000110111001011100110011110
>>> print(key_recovered)
00000011100101000000010000110111001011100110011110
```
