import matplotlib.pyplot as plt
import numpy as np
import basic_image_app
import basic_file_app
import px_shift_on_arrays
import single_image_processing


class StackProcessingWithShiftOnSequence:
    def __init__(self, path, image_list, minimum_position, method, rzp_spectrum_roi, back_roi):
        self.path = path
        self.image_list = image_list
        self.result_stack = []
        self.stack_shift_list = []
        self.rzp_spectrum_roi = rzp_spectrum_roi
        self.back_roi = back_roi
        self.temporary_image_array = []
        self.single_image_spectrum = []
        # first guess for minimum for shift evaluation (range-> in px-shift_on-array.py 15px fixed default)
        self.minimum_position = minimum_position
        # method: see below "xx" - nothing, "norm_single" norms stack members via maximum to first stack member
        self.method = method
        self.back_stats = []
        self.shift_stats = []

    def open_single_image(self, file_name):
        self.temporary_image_array = basic_image_app.read_image(self.path + '/' + file_name)
        return self.temporary_image_array

    def process_single_image(self, file_name, key_back):
        self.open_single_image(file_name)
        # calls script for single picture processing, choose option by key  for background subtraction
        # key = "back" : constant background subtraction on roi image
        # key = "refback" : reference on backroi between background and picture, scaled back ground subtraction
        single_picture_processing = single_image_processing.SingleImageOneRzpProcessing(self.temporary_image_array,
                                                                                        file_name, background_avg,
                                                                                        DataDirectory_dark,
                                                                                        self.rzp_spectrum_roi,
                                                                                        self.back_roi)
        if key_back == "back":
            self.single_image_spectrum = single_picture_processing.process_single_image_with_back()

        elif key_back == "refback":
            self.single_image_spectrum, scaling, mean_pic, mean_back = \
                single_picture_processing.process_single_image_with_referenced_back()
            self.back_stats.append(scaling)
        else:
            self.single_image_spectrum = single_picture_processing.process_single_image_without_back()
        return self.single_image_spectrum

    def process_stack(self, key_back):
        self.reference_image(key_back)
        # ToDo: test if image-list>1
        for x in self.image_list[1:]:
            print("iteration stack", x)
            # sum of lineouts with chosen back ground substraction method
            self.process_single_image(x, key_back)
            plt.figure(3)
            plt.plot(self.single_image_spectrum)
            plt.title("unshifted")
            self.result_array()
        # px-shift on members of stack to first stack member
        self.result_stack = self.shift_spectral_method()
        self.method()
        return self.avg_on_stack()

    def reference_image(self, key_back):
        file_name = self.image_list[0]
        print("reference file: ", file_name)
        self.process_single_image(file_name, key_back)
        self.result_array()

    def shift_spectral_method(self):
        evaluate_shift = px_shift_on_arrays.PixelShift(self.result_stack[0], self.minimum_position)
        for x in range(len(self.result_stack[1:])):
            self.result_stack[x] = evaluate_shift.evaluate_shift_for_input_array(self.result_stack[x])
            self.shift_stats.append(evaluate_shift.return_shift_value())
        return self.result_stack

    def method(self):
        # "norm_single for normalization of single images in stack"
        if self.method == "norm_single":
            # normalisierung der stack-member zu stack-member numero 1
            self.norm_single()
        else:
            print("no normalization on single image")

    def norm_single(self):
        # on particular spectral range
        reference_intensity = np.amax(self.result_stack[0][980:1100])
        for x in range(len(self.result_stack[1:])):
            ratio = np.amax(self.result_stack[x][980:1100]) / reference_intensity
            print("normalization single image", ratio)
            self.result_stack[x] = self.result_stack[x] * ratio
        return self.result_stack

    def avg_on_stack(self):
        avg_stack = np.mean(self.result_stack, axis=0)
        # plt.figure(5)
        # plt.plot(avg_stack, label = "avg on stack")
        # plt.legend()
        return avg_stack

    def result_array(self):
        self.result_stack.append(self.single_image_spectrum)
        return self.result_stack

    def plot_results(self):
        for x in range(len(self.result_stack)):
            plt.figure(2)
            plt.plot(self.result_stack[x], label=str(x))
            plt.show()

    # two stack lineout calculations (e.g. reference and data)
    def shift_for_two_stacks(self, result_array, reference_array):
        # only 1D arrays (e.g. avg )
        evaluate_shift = px_shift_on_arrays.PixelShift(result_array, self.minimum_position)
        result_array_min_position = evaluate_shift.return_reference()
        evaluate_shift_reference = px_shift_on_arrays.PixelShift(reference_array, self.minimum_position)
        reference_array_min_position = evaluate_shift_reference.return_reference()
        shift_between_stacks = reference_array_min_position - result_array_min_position
        print("shift between reference stack and data stack:", shift_between_stacks)
        self.shift_stats.append(shift_between_stacks)
        result_array = np.roll(result_array, shift_between_stacks)
        return result_array

    def normalize_two_lists(self, result_array, reference_array):
        max_result = np.amax(result_array)
        max_reference = np.amax(reference_array)
        ratio = max_result / max_reference
        print("normalization of data  to reference intensity of about: ", 1 / ratio)
        return result_array[:] / ratio

    def save_backstats(self, name):
        data = np.hstack(("background statistic referenced in back roi (mean value) scaling", self.shift_stats))
        np.savetxt(name + "backstats" + ".txt", self.back_stats, delimiter=' ',
                   header='string', comments='',
                   fmt='%s')

    def save_shift_stats(self, name):
        data = np.hstack(("shift statistic referenced to stack number one in px", self.shift_stats))
        np.savetxt(name + "shift_stats" + ".txt", data, delimiter=' ',
                   header='string', comments='',
                   fmt='%s')

    def nexafs_from_avg(self, data, reference, name):
        nexafs = -np.log(data / reference)
        plt.figure(6)
        plt.plot(nexafs, label="avg nexafs")
        plt.title("Nexafs" + name)
        # plt.ylim(-0.02, 0.02)
        # plt.xlim(600, 2000)
        plt.legend()
        self.save_nexafs(name, nexafs)
        return nexafs

    def save_nexafs(self, name, nexafs):
        plt.figure(6)
        print(name, "name of picture")
        plt.savefig(name + "Nexafs" + ".png", bbox_inches="tight", dpi=500)
        np.savetxt(name + "Nexafs" + ".txt", nexafs, delimiter=' ',
                   header='string', comments='',
                   fmt='%s')

    def prepare_header(self, description1, result_list):
        # insert header line and change index

        header_names = (['stack spectrum '])
        add_info = str(self.back_roi) + "backroi"
        add_info2 = str(self.rzp_spectrum_roi) + "dataroi"
        parameter_info = (
            ['description:' + description1])
        return np.hstack((parameter_info, add_info, add_info2, header_names, result_list))

    def save_data(self, description1, result_list):
        print("xxxxxxxxxxxxxxxxxxxxxxxx")
        result = self.prepare_header(description1, result_list)
        print('...saving:', result)
        np.savetxt(description1 + ".txt", result, delimiter=' ',
                   header='string', comments='',
                   fmt='%s')


def naming_back_key():
    if key == "refback":
        return "RB"
    elif key == "back":
        return "B"
    else:
        return ""


def naming_method():
    if method == "norm_single":
        return "N"
    else:
        return ""


data_directory = "data/m115"
data_name = data_directory[-4:]
DataDirectory_dark = 'data/straylight500ms'
dark_avg_calculation = basic_image_app.ImageStackMeanValue(DataDirectory_dark)
background_avg = dark_avg_calculation.average_stack()

data_list1 = basic_image_app.get_file_list(data_directory)
reference_list, data_list = basic_file_app.search_file_list(data_list1, "LOW")

# choose "xx" for "noback", "back" for unscaled backsubtraction, "refback" for referenced back substraction
key = "refback"
# choose "nix" for nix and "norm_single" for single image normalization (to 1. picture of stack)
method = "xx"

name1 = "20220228" + data_name + "Pump" + naming_back_key() + naming_method()
name2 = "20220228" + data_name + "noPump" + naming_back_key() + naming_method()

# data roi where the spectrum is sitting, [x1, y1, x2, y2]
data_roi = ([1152, 585, 1730, 640])

# backroi for referenced back ground subtraction [x1, y1, x2, y2]
back_roi = ([0, 0, 430, 312])
# first guess minimum in spectra for px-shift correction
# Note!! this is counting from data_roi start = 0
minimum_reference_x = 237  # 379

# batch process data
batch_process_data = StackProcessingWithShiftOnSequence(data_directory, data_list, minimum_reference_x, method,
                                                        data_roi, back_roi)
my_data_avg = batch_process_data.process_stack(key)
batch_process_data.save_data(name1, my_data_avg)
batch_process_data.save_backstats(name1)
batch_process_data.save_shift_stats(name1)

# batch process reference
batch_process_reference = StackProcessingWithShiftOnSequence(data_directory, reference_list, minimum_reference_x,
                                                             method, data_roi, back_roi)
my_reference_avg = batch_process_reference.process_stack(key)
batch_process_reference.save_data(name2, my_reference_avg)
batch_process_reference.save_backstats(name2)
batch_process_reference.save_shift_stats(name2)

# use last class for operations on two input list:
my_data_avg = batch_process_reference.shift_for_two_stacks(my_data_avg, my_reference_avg)
# my_data_avg = batch_process_reference.normalize_two_lists(my_data_avg, my_reference_avg)
# the nexafs function creates nexafs, plots and saves plot and data if you don't comment it out

batch_process_reference.nexafs_from_avg(my_data_avg, my_reference_avg, name1)

plt.show()
