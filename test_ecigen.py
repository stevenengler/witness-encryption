from ecigen import generate
import itertools
import sys

# Testing
n = int(sys.argv[1])
l = int(sys.argv[2])
t = int(sys.argv[3])
subsets, witness = generate(n, l, t)
# Check that we have the right number of subsets
assert(len(subsets) == t)

# Check witness is the right length
assert(len(witness) == l)

witness_subsets = [subsets[i] for i in witness]

# Check that we have exactly n elements across all witness subsets
assert(sum([len(i) for i in witness_subsets]) == n)
# Check that their union is the {1, 2, ..., n}
assert(set(itertools.chain.from_iterable(witness_subsets)) == set(range(1, n+1)))

print(subsets)
print(witness)
