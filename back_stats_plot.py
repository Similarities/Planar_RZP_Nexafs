import matplotlib.pyplot as plt
import numpy as np

import basic_file_app






no_back = basic_file_app.load_1d_array("20220310_results/referenced_Backcorrection/202200310_125all800mspumpBRBackTest.txt", 0,1)

x = np.linspace(0,len(no_back),len(no_back) )
print(len(no_back))
print(no_back)
plt.scatter(x, no_back, label=  "125II + 125 HIGH", marker= "+")
no_back = basic_file_app.load_1d_array("20220310_results/referenced_Backcorrection/202200310_125all800msnoPumpBRBackTest.txt", 0,1)
x = np.linspace(0,len(no_back),len(no_back) )
print(len(no_back))
print(no_back)
plt.scatter(x, no_back, label ="125II + 125 LOW",  marker= ".")

plt.ylabel("scaling factor (mean.back/mean.data)")
plt.xlabel("shot_number of stack")

plt.title("20220310_ background stats ")

plt.legend()

#plt.yscale(log)

plt.savefig("20220310_backstats_125all "+ ".png", bbox_inches="tight", dpi=500)
plt.show()
