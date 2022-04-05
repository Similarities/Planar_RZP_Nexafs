import matplotlib.pyplot as plt
import numpy as np

import basic_file_app






no_back = basic_file_app.load_1d_array("20220310_results/referenced_Backcorrection/202200310_130pumpBRShift.txt", 0,1)

x = np.linspace(0,len(no_back),len(no_back) )
print(len(no_back))
print(no_back)
plt.scatter(x, no_back, label=  "130 BR HIGH", marker= "+")
no_back = basic_file_app.load_1d_array("20220310_results/back_correct/202200310_130pumpBShift.txt", 0,1)
x = np.linspace(0,len(no_back),len(no_back) )
print(len(no_back))
print(no_back)
plt.scatter(x, no_back, label ="130 B HIGH",  marker= ".")
no_back = basic_file_app.load_1d_array("20220310_results/no_back_correction/202200310_130pumpShift.txt", 0,1)
x = np.linspace(0,len(no_back),len(no_back) )
print(len(no_back))
print(no_back)
plt.scatter(x, no_back, label ="130 no back HIGH",  marker= ".")


plt.ylabel("in between stack members shift")
plt.xlabel("shot_number of stack")

plt.title("20220310_ shift stats back methods ")

plt.legend()

#plt.yscale(log)

plt.savefig("20220310_backmethods_130 "+ ".png", bbox_inches="tight", dpi=500)
plt.show()
