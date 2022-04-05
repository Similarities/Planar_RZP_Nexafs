import matplotlib.pyplot as plt
import numpy as np






class SingleImageOneRzpProcessing:
    # this processes single pictures
    # note upper and lower and are changed in order and separated, as the middle part is cut out
    # picture = image-array, background_array = image array !!! beide gleiche größe haben müssen
    # !!! rois hier setzen, 1. für Spektalen ROI, 2. Background Roi (nur zur normierung von Background und Picture)
    def __init__(self, picture, picture_name, background_array, background_name, roi_list_spectrum, roi_list_back):
        self.filename = picture_name
        self.picture = picture
        self.background = background_array
        self.background_name = background_name
        # roi [x1, y1,x2, y2]
        self.roi = roi_list_spectrum  # lower
        # x1, y1, x2, y2 needs to be given for the picture
        self.back_roi = roi_list_back
        self.spectrum_measurement = []
        self.back_ground_roi = self.background[self.back_roi[1]:self.back_roi[3], self.back_roi[0]:self.back_roi[2]]
        self.raw_picture = self.roi_measurement()
        self.scaling = 1


    def roi_measurement(self):
        # faster method remember: we have 32bit images
        raw_picture = self.picture[self.roi[1]:self.roi[3], self.roi[0]:self.roi[2]]
        return raw_picture

    def test_background_roi(self):
        plt.figure(7)
        plt.imshow(self.picture)
        plt.vlines(ymin=0, ymax=2048, x=self.back_roi[0], color="r")
        plt.vlines(ymin=0, ymax=2048, x=self.back_roi[2], color="w")
        plt.hlines(xmin=0, xmax=2048, y=self.back_roi[1])
        plt.hlines(xmin=0, xmax=2048, y=self.back_roi[3])
        plt.show()

    def reference_scaling(self):
        # opens tif is flipped vertical, array_image[y:y1, x:x1] (warum auch immer....)
        subarray_picture = self.picture[self.back_roi[1]:self.back_roi[3], self.back_roi[0]:self.back_roi[2]]
        # optional sum statt mean, median -
        mean_background_picture_x = np.mean(subarray_picture, axis=0)
        subarray_picture = []
        back_mean = np.mean(self.back_ground_roi, axis=0)
        #ToDo: test if background remains constant over loop of this class (merken der Variable)
        mean_pic = np.mean(mean_background_picture_x)
        mean_back = np.mean(back_mean)
        self.scaling = np.round(mean_pic/mean_back,4)
        print("normalization for background", self.scaling)

        self.back_ground_roi = []
        plt.figure(98)
        plt.plot(mean_background_picture_x[:], color="c", alpha=0.3)
        plt.plot(back_mean[:]*self.scaling, color = "r", alpha = 0.1)
        plt.title("background comparison")

        return self.scaling, np.mean(mean_background_picture_x), np.mean(back_mean)


    def background_on_roi(self):
        self.background = self.background[self.roi[1]:self.roi[3], self.roi[0]:self.roi[2]]
        self.raw_picture[:, :] = self.raw_picture[:, :] - self.background[:, :]*self.scaling
        self.background = []
        return self.raw_picture


    def figure_raw(self, picture_array):
        plt.figure(8)
        plt.imshow(picture_array)
        plt.colorbar()
        plt.show()

    def plot_arrays_1_d(self, array, name, figure_number):
        plt.figure(figure_number)
        plt.plot(array, label=name)
        plt.legend()
        plt.show()


    def process_single_image_with_referenced_back(self):
        self.scaling, mean_pic, back_mean = self.reference_scaling()

        self.process_single_image_with_back()
        return self.spectrum_measurement, self.scaling, mean_pic, back_mean


    def process_single_image_without_back(self):
        self.picture = []
        self.sum_spectra()
        self.raw_picture =[]
        return self.spectrum_measurement

    def process_single_image_with_back(self):
        self.background_on_roi()
        self.sum_spectra()
        self.raw_picture = []
        return self.spectrum_measurement

    def sum_spectra(self):
        self.spectrum_measurement = np.sum(self.raw_picture, axis=0)
        return self.spectrum_measurement

    def get_spectrum_measurement(self):
        return self.spectrum_measurement