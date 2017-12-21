from trivial_ges import TrivialGES
import sys

# Testing
l = int(sys.argv[1])
n = int(sys.argv[2])

print("Instantiating with lambda = ", l, " n = ", n)
x = TrivialGES(l, n)

print("n: ", x.get_n())
print("lambda: ", x.get_lambda())

e = x.sample()
print("Sample 1:", e)
f = print("Sample 2: ", x.sample())
f = print("Sample 3: ", x.sample())
f = print("Sample 4: ", x.sample())

e = x.encode(1, e)
print("Encoding first sample at level 1", e)
f = x.copy_encoding(e)
print("Copying encoding: ", f)
x.rerandomize(2, e)
print("Rerandomizing first encoding at level 2: ", e)
print("Checking copy has not changed: ", f)

print("Multiplying both and returning new: ", x.multiply(e, f))
print("Checking encodings haven't changed: ")
print("\t", e)
print("\t", f)
print("Multiplying both and storing in new: ", x.multiply(e, f, e))
print("Checking only first encoding changes: ")
print("\t", e)
print("\t", f)

print("Length of key from first:", len(x.extract(e)))
print("Length of key from second:", len(x.extract(f)))
print("First two keys are equal:", str(x.extract(e)) == str(x.extract(f)))
print("First encoding key and key of copy are equal:",
        str(x.extract(e)) == str(x.extract(x.copy_encoding(e))))

