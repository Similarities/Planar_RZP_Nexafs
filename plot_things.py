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





no_back = basic_file_app.load_1d_array("20220228_no_back_correction/20220228_m120pump.txt", 0,1)
no_pumped =basic_file_app.load_1d_array("20220228_no_back_correction/20220228_m120noPump.txt", 0,1)
no_back = shift_for_two_stacks(no_back, no_pumped)

plt.plot(no_back, label = "120 pump")
plt.plot(no_pumped, label = "120 ref")
plt.legend()
#plt.vlines(ymin= -0.1, ymax=0.1, x=765)
plt.title("20220228_120 ")
plt.xlim(600, 800)

#plt.ylim(-0.01, 0.01)


plt.xlabel("px")
plt.ylabel("-log(ref/pumped)")




#plt.yscale(log)

plt.savefig("20220228_m120_avg"+ ".png", bbox_inches="tight", dpi=500)
plt.show()
