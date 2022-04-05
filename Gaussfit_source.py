import matplotlib.pyplot as plt
import numpy as np
import basic_image_app
from lmfit.models import GaussianModel
import math


class SourceSize:

    def __init__(self, file, width_area):
        self.image = file
        self.index_y, self.index_x_axis = self.evaluate_index_of_maximum_in_picture()
        self.width_area = width_area
        self.center_of_intensity() #- more accurate method for line out on roi positioning.
        self.x_axis_vertical, self.line_out_vertical = self.vertical_line_out()
        self.x_axis_horizontal, self.line_out_horizontal = self.horizontal_line_out()
        self.line_out_horizontal = self.zero_offset(self.line_out_horizontal)
        self.line_out_vertical = self.zero_offset(self.line_out_vertical)
        self.sigma_temp = 0
        self.amplitude_temp = 0
        self.center_temp = 0
        self.result = np.empty([1, 4])

    def evaluate_index_of_maximum_in_picture(self):
        self.index_y, self.index_x_axis = np.where(self.image >= np.amax(self.image))
        # sometimes np.where has more than one coordinate:
        self.index_y = self.index_y[0]
        self.index_x_axis = self.index_x_axis[0]
        print(np.amax(self.image), 'max', self.index_y, self.index_x_axis)
        return self.index_y, self.index_x_axis

    def center_lineout_on_image(self):
        plt.figure(12)
        plt.imshow(self.image[int(self.index_y - self.width_area / 2): int(self.index_y + self.width_area / 2),
                   int(self.index_x_axis - self.width_area / 2): int(self.index_x_axis + self.width_area / 2)])

    def center_of_intensity(self):
        print('before', self.index_y, self.index_x_axis)
        y_up = int(self.index_y - self.width_area / 2)
        y_down = int(y_up + self.width_area)
        x_left = int(self.index_x_axis - self.width_area / 2)
        x_right = int(x_left + self.width_area)
        sum_of_y_line = np.sum(self.image[y_up: y_down, x_left:x_right], axis=1)
        sum_of_x_line = np.sum(self.image[y_up: y_down, x_left:x_right], axis=0)
        plt.legend()
        self.index_y = int(np.where(sum_of_y_line[:] >= np.amax(sum_of_y_line))[0] - self.width_area / 2 + self.index_y)
        self.index_x_axis = int(
            np.where(sum_of_x_line[:] >= np.amax(sum_of_x_line))[0] - self.width_area / 2 + self.index_x_axis)
        print('after:', self.index_y, self.index_x_axis)
        return self.index_y, self.index_x_axis

    def plot_results(self):
        plt.figure(1)
        plt.imshow(self.image)
        #plt.scatter(self.index_x_axis, self.index_y)
        #plt.vlines(x=self.index_x_axis, ymin=0, ymax=len(self.image), color="y")
        plt.figure(2)
        plt.plot(self.x_axis_vertical, self.line_out_vertical, color="b")
        plt.figure(1)
        #plt.hlines(y=self.index_y, xmin=0, xmax=len(self.line_out_horizontal))
        plt.figure(3)
        plt.plot(self.x_axis_horizontal, self.line_out_horizontal, color="r")

    def vertical_line_out(self):
        # seems to be horizontal  [x values for y]
        self.line_out_vertical = self.image[:, self.index_x_axis]
        self.x_axis_vertical = np.arange(0, len(self.line_out_vertical))
        return self.x_axis_vertical, self.line_out_vertical

    def horizontal_line_out(self):
        self.line_out_horizontal = np.reshape(self.image[self.index_y, :], np.size(self.image[self.index_y, :]))
        self.x_axis_horizontal = np.arange(0, len(self.line_out_horizontal))
        return self.x_axis_horizontal, self.line_out_horizontal

    def evaluate_horizontal_and_vertical(self):
        self.fit_gaussian(self.x_axis_horizontal, self.line_out_horizontal, 3)
        self.result[0, 0] = self.sigma_temp
        self.result[0, 2] = self.center_temp
        self.fit_gaussian(self.x_axis_vertical, self.line_out_vertical, 2)
        self.result[0, 1] = self.sigma_temp
        self.result[0, 3] = self.center_temp
        return self.result


    def fit_gaussian(self, array_x, array_y,figurenumber):
        #print("fitting guassian")
        mod = GaussianModel()
        pars = mod.guess(array_y, x=array_x)
        out = mod.fit(array_y, pars, x=array_x)
        self.sigma_temp = out.params['sigma'].value
        self.amplitude_temp = out.params['amplitude'].value
        self.center_temp = out.params['center'].value
        return self.sigma_temp, self.amplitude_temp, self.center_temp

    def zero_offset(self, array):
        offset = np.mean(array[0:1])
        return array[:] - offset

    def plot_fit_function(self, array_x, figure_number):
        # IMPORTANT sigma  corresponds to w(0) beamwaist = half beam aperture
        yy = np.zeros([len(array_x), 1])
        for counter, value in enumerate(array_x):
            a = (self.amplitude_temp / (self.sigma_temp * ((2 * math.pi) ** 0.5)))
            b = -(array_x[counter] - self.center_temp) ** 2
            c = 2 * self.sigma_temp ** 2
            yy[counter] = (a * math.exp(b / c))

        plt.figure(figure_number)
        plt.plot(array_x, yy)
        if figure_number == 2:
            plt.plot(self.x_axis_vertical, self.line_out_vertical)
        else:
            plt.plot(self.x_axis_horizontal, self.line_out_horizontal)