# Witness Encryption Implementation
An (insecure) implementation of witness encryption in Python. The library uses a c++ graded multilinear map library.

The witness encryption implementation follows the design from the paper ["Witness Encryption and its Applications"](https://eprint.iacr.org/2013/258.pdf) by Garg et al.

The multilinear map code used is from the forked repository [new-multilinear-maps](https://github.com/stevenengler/new-multilinear-maps), which is described by the paper ["New Multilinear Maps over the Integers"](https://eprint.iacr.org/2015/162.pdf).

Developed by [Steven](https://github.com/stevenengler) and [Alex](https://github.com/alex-norton) for a course project.

## Set-up

To run the code, install [Docker](https://www.docker.com/) and build the Dockerfile. After building the image and running the container, you can access it by running `docker run -it <image-id> /bin/bash`.
