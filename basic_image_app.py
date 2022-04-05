import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image


def read_image(file):
    bg = Image.open(file)  # Listen und Arrays und so
    bg = np.array(bg)
    return bg.astype(float)


def get_file_list(path_picture):
    tif_files = []
    counter = 0
    for file in os.listdir(path_picture):
        print(file)
        try:
            if file.endswith(".tiff"):
                tif_files.append(str(file))
                counter = counter + 1
            else:
                print("only other files found")
        except Exception as e:
            raise e
    return tif_files


def convert_32_bit(picture):
    return np.float32(picture)


def search_file_list(list, search_word):
    list_key_word = []
    list_rest = []
    for counter, value in enumerate(list):
        if value.find(search_word) != -1:
            list_key_word.append(value)
        else:
            list_rest.append(value)
    return list_key_word, list_rest



class ImageStackMeanValue:

    def __init__(self, file_path):
        self.file_path = file_path
        self.list = get_file_list(self.file_path)
        self.result = np.zeros([2052, 2048])
        self.file_list = self.list
        self.others_list = []
        self.other_result= np.zeros([2052,2048])

    def selection_file_list(self, keyword):
        self.file_list = []
        for counter, value in enumerate(self.list):
            if value.find(keyword) != -1:
                self.file_list.append(value)
            else:
                self.others_list.append(value)

        return self.file_list, self.others_list

    def average_stack(self):
        for x in self.file_list:
            x = str(self.file_path + '/' + x)
            picture_x = read_image(x)
            #picture_x = convert_32_bit(picture_x)
            self.result = self.result + picture_x

        self.result = self.result / (len(self.file_list))
        return self.result




class ImageSumOverStack:

    def __init__(self, file_list, file_path):
        self.file_list = file_list
        self.file_path = file_path
        self.result = np.zeros([2052, 2048])

    def sum_stack(self):
        for x in self.file_list:
            x = str(self.file_path + '/' + x)
            picture_x = read_image(x)
            picture_x = convert_32_bit(picture_x)
            self.result = self.result + picture_x

        return self.result, len(self.file_list)


class SingleImageOpen:
    def __init__(self, file_name, file_path):
        self.file_name = file_name
        self.file_path = file_path

    def return_single_image(self):
        picture = read_image(str(self.file_path + '/' + self.file_name))
        return convert_32_bit(picture)



