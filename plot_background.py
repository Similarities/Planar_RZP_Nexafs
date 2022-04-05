import matplotlib.pyplot as plt
import numpy as np

import basic_file_app




no_back = basic_file_app.load_1d_array("202200310_125pumpedBack.txt", 0,1)
no_pumped =basic_file_app.load_1d_array("202200310_125noPumpBack.txt", 0,1)


plt.plot(-np.log(no_back[:]/no_pumped[:]), label = "125")
no_back = basic_file_app.load_1d_array("202200310_125IIIpumpedBack.txt", 0,1)
no_pumped =basic_file_app.load_1d_array("202200310_125IInoPumpBack.txt", 0,1)
no_back = shift_for_two_stacks(no_back, no_pumped)


no_back = basic_file_app.load_1d_array("202200310_125IIIpumpedBack.txt", 0,1)
no_pumped =basic_file_app.load_1d_array("202200310_125IIInoPumpBack.txt", 0,1)
no_back = shift_for_two_stacks(no_back, no_pumped)


no_back = basic_file_app.load_1d_array("202200310_130pumpedBack.txt", 0,1)
no_pumped =basic_file_app.load_1d_array("202200310_130noPumpBack.txt", 0,1)
no_back = shift_for_two_stacks(no_back, no_pumped)
plt.plot(-np.log(no_back[:]/no_pumped[:]), label = "130")

no_back = basic_file_app.load_1d_array("202200310_120pumpedBack.txt", 0,1)
no_pumped =basic_file_app.load_1d_array("202200310_120noPumpBack.txt", 0,1)
no_back = shift_for_two_stacks(no_back, no_pumped)
plt.plot(-np.log(no_back[:]/no_pumped[:]), label = "120")



plt.legend()
plt.title("20220310_ ODD Back ")
plt.xlim(400, 1400)

#plt.yscale(log)

plt.savefig("20220310BackODDpxshifted"+ ".png", bbox_inches="tight", dpi=500)
plt.show()
