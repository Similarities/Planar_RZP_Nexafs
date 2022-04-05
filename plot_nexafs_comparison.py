import matplotlib.pyplot as plt
import numpy as np
import px_shift_on_arrays
import basic_file_app

minimum_position = 765

def shift_for_two_stacks( result_array, reference_array):
    # only 1D arrays (e.g. avg )
    evaluate_shift = px_shift_on_arrays.PixelShift(result_array, minimum_position)
    result_array_min_position = evaluate_shift.return_reference()
    evaluate_shift_reference = px_shift_on_arrays.PixelShift(reference_array, minimum_position)
    reference_array_min_position = evaluate_shift_reference.return_reference()
    shift_between_stacks = reference_array_min_position - result_array_min_position
    print("shift between reference stack and data stack:", shift_between_stacks)
    result_array = np.roll(result_array, shift_between_stacks)
    return result_array
# "0" = -125



no_back = basic_file_app.load_1d_array("20220302_referenced_back_correction/20220302_m117pumpBR.txt", 0,1)
no_pumped = basic_file_app.load_1d_array("20220302_referenced_back_correction/20220302_m117noPumpBR.txt", 0,1)
no_back = shift_for_two_stacks(no_back, no_pumped)
#plt.plot(np.log(no_back[:]/no_pumped[:]), label = "117, -16mm, -53ps")
#plt.plot(no_back, label = "pump")
#plt.plot(no_pumped, label ="no pump")

no_back = basic_file_app.load_1d_array("20220302_referenced_back_correction/20220302_m117_IIpumpBR.txt", 0,1)

no_pumped =basic_file_app.load_1d_array("20220302_referenced_back_correction/20220302_m117_IInoPumpBR.txt", 0,1)
no_back = shift_for_two_stacks(no_back, no_pumped)
#plt.plot(-np.log(no_back[:]/no_pumped[:]), label = "117 II, -16mm, -53ps")



no_back = basic_file_app.load_1d_array("20220302_referenced_back_correction/20220302_m117_IIIpumpBR.txt", 0,1)
no_pumped =basic_file_app.load_1d_array("20220302_referenced_back_correction/20220302_m117_IIInoPumpBR.txt", 0,1)
no_back = shift_for_two_stacks(no_back, no_pumped)
plt.plot(np.log(no_back[:])-np.log(no_pumped[:]), label = "117 III, -16mm, -53ps")
#plt.plot(no_back, label = "pump")
#plt.plot(no_pumped, label ="no pump")
print(no_pumped[765], no_back[765])




plt.legend()
plt.title("20220302_ ODDB ")
plt.vlines(ymin = -0.1, ymax= 0.2, x = 765)
plt.xlim(600, 800)

#plt.yscale(log)

plt.savefig("20220302B_ODD_"+ ".png", bbox_inches="tight", dpi=500)
plt.show()
