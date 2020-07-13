import re
a = "zenfone6"
b = re.findall(r'[A-Za-z]+|\d+', a)
print(b)
k = (" ".join(b))
print(k,1)