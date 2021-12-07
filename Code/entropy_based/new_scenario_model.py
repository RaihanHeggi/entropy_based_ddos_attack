import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sn
import itertools
import operator
import statistics
import collections
import math
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from scipy.stats import entropy
from sklearn.preprocessing import MinMaxScaler
from sympy import *


class entropy_model:
    def __init__(self, windows_size, mean_count):
        self.cut_value = windows_size
        self.mean_count = mean_count
        self.list_entropy_luar = list()
        self.list_entropy_dalam = list()
        self.hasil = list()
        self.current_count = 0

    ########################################## NEW CODE ################################################
    # Calculate Entropy Value and Cut on Windows Size

    # nilai pada log bisa diganti menjadi basis 2 atau 10 dikarenakan rumusan menghitung shannon entropy
    def entropy_calculate_2(self, s):
        x_value = [x for x, n_x in collections.Counter(s).items()]
        probabilities = [n_x / len(s) for x, n_x in collections.Counter(s).items()]
        e_x = [-p_x * math.log(p_x + 0.1, 2) for p_x in probabilities]
        n_e = [h / math.log(len(s), 10) for h in e_x]
        entropy_df = dict(zip(x_value, e_x))
        normalize_entropy = dict(zip(x_value, n_e))
        return entropy_df, normalize_entropy

    def search_threshold(self, x):
        # get max value for threshold
        all_values = x.values()
        return np.mean(list(all_values))

    def create_toList(self, list_data, filter_value):
        list_hasil = list()
        for x in list_data:
            list_hasil.append(x[filter_value])
        return list_hasil

    def new_get_entropy_prediction(self, df):
        counter = 0
        list_output = list()
        list_luar = list()
        df_columns_len = len(list(df.columns))
        for x, y in df.iterrows():
            self.list_entropy_dalam.append(y.values)
            if counter == self.cut_value:
                for i in range(df_columns_len):
                    list_output = self.create_toList(self.list_entropy_dalam, i)
                    entropy_value, normalized_entropy = self.entropy_calculate_2(
                        list_output
                    )
                    mean_value = self.search_threshold(entropy_value)
                    list_luar.append(
                        [entropy_value, mean_value, list_output, normalized_entropy]
                    )
                self.list_entropy_luar.append(list_luar)
                self.list_entropy_dalam = []
                list_luar = []
                counter = 0
            counter += 1

        # input Last Value Group Value
        for i in range(df_columns_len):
            list_output = self.create_toList(self.list_entropy_dalam, i)
            entropy_value, normalized_entropy = self.entropy_calculate_2(list_output)
            mean_value = self.search_threshold(entropy_value)
            list_luar.append(
                [entropy_value, mean_value, list_output, normalized_entropy]
            )
        self.list_entropy_luar.append(list_luar)
        self.list_entropy_dalam = []
        return

    # patokan menggunakan SRCIP namun sistem sudah dinamis sisa dipikirkan bagaimana bila ada lebih dari satu fitur yang dimasukann
    def new_label(self, list_entropy, listdata, status, iterasi):
        # use status[iterasi].get(x) if threshold using dict
        # use status[iterasi] if threshold using list
        counter_data = 0
        loop_data = len(list_entropy)
        for x in listdata:
            if (list_entropy.get(x) == None) or (status[iterasi].get(x) == None):
                continue
            elif list_entropy.get(x) < status[iterasi].get(x):
                self.hasil.append(1)
            else:
                self.hasil.append(0)
        return

    def normalized_entropy(self, normalize_threshold, list_threshold):
        # use status[iterasi].get(x) if threshold using dict
        # use status[iterasi] if threshold using list
        dict_key = list()
        list_hasil = list()
        for x in normalize_threshold:
            dict_key = x.keys()
            for i in dict_key:
                # masih menggunakan satu SRCIP dulu
                for j in range(len(list_threshold) - 1):
                    if x.get(i) < list_threshold[j].get(i):
                        list_hasil.append([i, True])
                    else:
                        list_hasil.append([i, False])
        return list_hasil

    def check_maximum_entropy(self, threshold):
        dictionary_hasil = dict()
        maximum = list()
        value_max = list()
        for x in threshold:
            nilai_max = max(x, key=x.get)
            maximum.append(nilai_max)  # Just use 'min' instead of 'max' for minimum.
            value_max.append(x[nilai_max])
        dictionary_hasil = dict(zip(maximum, value_max))
        return list(dictionary_hasil.values())

    def calculate_limit(self, list_entropy, list_data, max_value):
        x_value = [x for x, n_x in collections.Counter(list_data).items()]
        n_x_value = [n_x for x, n_x in collections.Counter(list_data).items()]
        count_value = dict(zip(x_value, n_x_value))
        for x in x_value:
            if count_value.get(x) != None:
                z = symbols("x")
                limit_value = limit(
                    (1 / count_value.get(x)) * list_entropy.get(x), z, oo,
                )
                if limit_value <= max_value:
                    print("Intrusi Terjadi")
                else:
                    print("Jaringan Normal")
            else:
                continue
        return

    def loop_hasil(self, listdata, list_threshold):
        counter_data = 0
        threshold_list = list_threshold
        data_count = 0
        # list_mean = list()
        list_normal_entropy = list()
        list_windows_entropy = list()
        list_entropy_only = list()
        iterasi = 1
        for x in listdata:
            data_count = len(x)
            for j in x:
                # Note saat ini cuma melihat SRCIP saja
                if iterasi >= data_count:
                    iterasi = 1
                    break
                else:
                    self.new_label(j[0], j[2], threshold_list, iterasi - 1)
                    # list_mean.append(j[1])
                    list_normal_entropy.append(j[3])
                    list_windows_entropy.append([j[0], j[2]])
                    list_entropy_only.append(j[0])
                    iterasi += 1

            if counter_data > self.mean_count:
                check_normalized_value = self.normalized_entropy(
                    list_normal_entropy, threshold_list
                )
                maximum_value = self.check_maximum_entropy(list_entropy_only)

                # buka komentar ketika sudah ingin implementasi dengan sistem deteksi
                for x in check_normalized_value:
                    if x[1]:
                        # pengecekan lebih lanjut
                        for x in list_windows_entropy:
                            for i in range(len(maximum_value)):
                                self.calculate_limit(x[0], x[1], maximum_value[i])
                    else:
                        print("Jaringan Normal")
                # list_mean = []
                list_normal_entropy = []
                list_windows_entropy = []
                list_entropy_only = []
                counter_data = 0
            counter_data += 1
        return self.hasil

    def check_entropy_all(self, df):
        df_columns = list(df.columns)
        list_hasil = list()
        max_entropy = list()
        for x in df_columns:
            list_hasil = df[x].tolist()
            entropy_value = self.entropy_calculate_2(list_hasil)
            max_entropy.append(entropy_value)
        return max_entropy

    def check_maximum_entropy(self, threshold):
        dictionary_hasil = dict()
        maximum = list()
        value_max = list()
        for x in threshold:
            nilai_max = max(x, key=x.get)
            maximum.append(nilai_max)  # Just use 'min' instead of 'max' for minimum.
            value_max.append(x[nilai_max])
        dictionary_hasil = dict(zip(maximum, value_max))
        return list(dictionary_hasil.values())

    def check_average_entropy(self, threshold):
        list_avg = list()
        for x in threshold:
            list_avg.append(statistics.mean(x.values()))
        return list_avg

    # Getter
    def get_list_luar(self):
        return self.list_entropy_luar

    def calculate_all_entropy(self, df):
        entropy_list = list()
        for x, y in df.iterrows():
            entropy_value = self.entropy_calculate(y.values)
            entropy_list.append(entropy_value)
        return entropy_list

    def get_prediction_result(self, threshold):
        list_nilai_mean = self.get_mean_prediction()
        self.create_prediction_result(list_nilai_mean, threshold)
        return self.hasil

    def check_entropy_value(self, df):
        for x, y in df.iterrows():
            print(self.entropy_calculate(y.values))
            print(self.entropy_calculate(y.values))
            break


def normalization_dataset(df):
    scaler = MinMaxScaler()
    df = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)
    return df


def check_df(df):
    print(df.head(5))
    return


def main():
    dataset_path = "semi_processed_train.csv"

    # Load Dataset Value to Dataframe
    df = pd.read_csv(dataset_path, sep=",")
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    # getting sample of current dataframe
    # df = df.head(10000)

    ######################## NEW SCENARIO ###################################

    # splitting data
    x = df[["srcIP", "dstIP"]]
    y = df["label"]

    # creating model with windows size and mean_count
    model = entropy_model(10, 5)
    threshold_value, normalize_threshold = model.check_entropy_all(x)

    # Skenario menggunakan max_threshold jika menggunakan ini, maka perlu mengganti metode pada fungsi new_label dan normalized_entropy
    # max_threshold = model.check_maximum_entropy(threshold_value)
    # avg_threshold = model.check_average_entropy(threshold_value)

    model.new_get_entropy_prediction(x)
    list_luar = model.get_list_luar()

    predict_result = model.loop_hasil(list_luar, threshold_value)
    # predict_result = model.loop_hasil(list_luar, max_threshold)
    # predict_result = model.loop_hasil(list_luar, avg_threshold)

    print(confusion_matrix(y, predict_result))
    print(classification_report(y, predict_result))
    print(
        "Accuracy:", accuracy_score(y, predict_result) * 100,
    )


if __name__ == "__main__":
    main()
