import numpy as np

disp_file = open('dispersiyon_cozumu.txt', "r")

data = np.loadtxt(disp_file)

a = data[0]
b = data[1]
c = data[2]
d = data[3]

print(a,b,c,d)

