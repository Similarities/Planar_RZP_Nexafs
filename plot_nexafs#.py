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

no_back = basic_file_app.load_1d_array("20220228_no_back_correction/20220228_m115pump.txt", 0,1)
no_pumped =basic_file_app.load_1d_array("20220228_no_back_correction/20220228_m115noPump.txt", 0,1)
no_back = shift_for_two_stacks(no_back, no_pumped)
plt.plot(-np.log(no_back[:]/no_pumped[:]), label = "115, -20mm")

no_back = basic_file_app.load_1d_array("20220228_no_back_correction/20220228_m120pump.txt", 0,1)
no_pumped =basic_file_app.load_1d_array("20220228_no_back_correction/20220228_m120noPump.txt", 0,1)
no_back = shift_for_two_stacks(no_back, no_pumped)
plt.plot(-np.log(no_back[:]/no_pumped[:]), label = "120, -10mm")


no_back = basic_file_app.load_1d_array("20220228_no_back_correction/20220228_m130pump.txt", 0,1)
no_pumped =basic_file_app.load_1d_array("20220228_no_back_correction/20220228_m130noPump.txt", 0,1)
no_back = shift_for_two_stacks(no_back, no_pumped)
#plt.plot(-np.log(no_back[:]/no_pumped[:]), label = "130, 10mm")





plt.legend()
plt.title("20220228_ ODD ")
plt.ylabel("-log(pump/ref)")
plt.xlabel("px")
plt.xlim(400,900)
plt.ylim(-0.01, 0.01)
plt.vlines(ymin= -0.1, ymax=0.1, x=765)
#plt.yscale("log")

#plt.yscale(log)

plt.savefig("20220228_ODD_120_115"+ ".png", bbox_inches="tight", dpi=500)
plt.show()
