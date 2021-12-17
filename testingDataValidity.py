import os

dirs = os.listdir('Data/')

dirs.sort()

for d in dirs:
    files = os.listdir('Data/' + d)

    print(d, ' : ', len(files))



sums = os.listdir('summary/')

sums.sort()

print(sums)
print(len(sums))