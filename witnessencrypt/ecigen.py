from random import *

# Generates exact cover instance for target length n with t subsets
# Returns (s, w) where s is a t-length list of subsets and w is a l length list of witness indices of s
def generate(n, l, t):
    assert t >= n
    assert 1 <= l <= n
    target = list(range(1,n+1))
    witness = []
    # Randomly create a witness set of appropriate length
    for _ in range(l):
        next_element = sample(target, 1)[0]
        target.remove(next_element)
        witness.append([next_element])

    # Randomly partition remaining target set between partitions
    while target:
        next_element = sample(target, 1)[0]
        target.remove(next_element)
        next_partition = randrange(l)
        witness[next_partition].append(next_element)
    witness = [sorted(w) for w in witness]

    # Randomly generate other subsets
    subsets = []
    rem = t - len(witness)
    for _ in range(rem):
        subset = set()
        length = randint(1, n)
        for _ in range(length):
            subset.add(randint(1, n))
        subsets.append(sorted(subset))

    # Shuffle witnesses into subsets
    witness_indices = []
    for w in witness:
        index = randint(0, len(subsets))
        subsets.insert(index, w)
        # If this is inserted before any other witness element then those elements move up
        witness_indices = [i + 1 if i >= index else i for i in witness_indices]
        witness_indices.append(index)

    return (subsets, sorted(witness_indices))

if __name__=='__main__':
    import itertools
    import sys

    # run this code to test the exact cover instance generation. Ex: `python ecigen.py 10 5 20`

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
