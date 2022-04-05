import numpy as np
import matplotlib.pyplot as plt


# reference point list: method evaluates minimum in +/- range, the px-position (in x) of minimum is needed
# umgeschrieben mit np.roll auf 1d arrays
# array_reference - 1d reference spectrum
# reference point: initial guess minimum
class PixelShift:
    def __init__(self, array_reference, reference_point):

        self.array_reference = array_reference
        self.reference_points = reference_point
        self.array_in = np.empty([])
        self.binned_reference = np.empty([])
        self.position_reference = int
        self.prepare_reference()
        self.shift = 0

    def prepare_reference(self):
        self.position_reference = self.minimum_analysis(self.array_reference)
        print(self.position_reference, 'minimum reference')
        return self.position_reference

    def return_reference(self):
        return self.position_reference

    def evaluate_shift_for_input_array(self, spectrum):
        #spectrum ist 1d spectrum -> for stacks: muss man dat hier in loop packen
        self.array_in = spectrum
        # self.test_plot(self.array_reference, 1, "reference")
        min_position = self.minimum_analysis(self.array_in)
        self.shift = self.shift_to_reference(min_position)
        # print(min_position, '#### minimum### ')
        corrected_array = self.correct_for_shift(spectrum)
        # self.test_plot(corrected_array, 2, "px-shifted")
        return corrected_array

    def shift_to_reference(self, minimum_position):
        return self.position_reference - minimum_position

    def return_shift_value(self):
        return self.shift

    def correct_for_shift(self,  array):
        self.return_shift_value()
        print("shift to reference is:", self.shift)
        if self.shift == 0:
            corrected_array = array

        elif self.shift < 0 & self.shift > -15:
            corrected_array = np.roll(array, self.shift)

        elif self.shift > 0 & self.shift < 15:
            corrected_array = np.roll(array, self.shift)
        return corrected_array

    def minimum_analysis(self, array):
        left = self.reference_points - 15
        right = self.reference_points + 15
        sub_array = array[left:right]
        minimum = np.amin(sub_array)
        # print(minimum)
        # print([idx for idx, val in enumerate(sub_array) if val == minimum] )
        shift_1 = [idx for idx, val in enumerate(sub_array) if val == minimum][0] + left
        return shift_1

    def maximum_analysis(self, array):
        left = self.reference_points - 15
        right = self.reference_points + 15
        sub_array = array[left:right]
        maximum = np.amax(sub_array)
        print([idx for idx, val in enumerate(sub_array) if val == maximum])
        shift_1 = [idx for idx, val in enumerate(sub_array) if val == maximum][0] + left
        return shift_1

    def test_plot(self, array, figure_number, name):
        plt.figure(figure_number)
        plt.plot(array, label=name)
        plt.title("px - shift -test plot")
        # plt.ylim(0, np.amax(array))
        # plt.xlim(self.reference_points[0] -20, self.reference_points[0] + 20)
        # plt.legend()
