import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sn
import itertools
import operator
import statistics
import collections
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from scipy.stats import entropy


class entropy_model:
    def __init__(self, windows_size, mean_count):
        self.cut_value = windows_size
        self.mean_count = mean_count
        self.list_entropy_luar = list()
        self.list_entropy_dalam = list()
        self.hasil = list()
        self.current_count = 0

    # Fungsi Check Nilai Entropi
    def entropy_calculate(self, labels):
        # value, counts = np.unique(labels, return_counts=True)

        # Shannon Entropy
        bases = collections.Counter([tmp_base for tmp_base in labels])
        dist = [x / sum(bases) for x in bases]
        return entropy(dist, base=2)

    # Fungsi Cek Nilai Monoton Turun
    def monotone_decreasing(self, list_value):
        pairs = zip(list_value, list_value[:0])
        return all(itertools.starmap(operator.ge, pairs))

    def labelling_data(self, x, threshold):
        for j in x:
            for i in j:
                if i > threshold:
                    self.hasil.append(1)
                else:
                    self.hasil.append(0)

    def get_mean_prediction(self):
        list_hasil_deteksi = list()
        for x in self.list_entropy_luar:
            list_hasil_deteksi.append([x, np.mean(x)])
        return list_hasil_deteksi

    def create_prediction_result(self, list_data, threshold):
        count_data = 0
        list_nilai = list()
        list_mean = list()
        for x in list_data:
            list_nilai.append(x[0])
            list_mean.append(x[1])
            if count_data == self.mean_count:
                check_monoton_turun = self.monotone_decreasing(list_mean)
                if check_monoton_turun:
                    # print("Intrusi Terjadi")
                    self.labelling_data(list_nilai, threshold)
                else:
                    self.labelling_data(list_nilai, threshold)
                count_data = 0
                list_nilai = []
                list_mean = []
            count_data += 1

        # Nilai Sisa Masukin
        self.labelling_data(list_nilai, threshold)
        return

    def get_entropy_prediction(self, df):
        stop_iteration = True
        counter = 0
        for x, y in df.iterrows():
            entropy_values = self.entropy_calculate(y.values)
            self.list_entropy_dalam.append(entropy_values)
            if counter == self.cut_value:
                self.list_entropy_luar.append(self.list_entropy_dalam)
                self.list_entropy_dalam = []
                counter = 0
            counter += 1

        # input last data
        self.list_entropy_luar.append(self.list_entropy_dalam)

        # old methods need revision but newer one more readable
        # while counter < df.shape[0]:
        #     df_test = df.iloc[
        #         self.current_count : (self.current_count + self.cut_value)
        #     ]
        #     if count_data == self.mean_count:
        #         check_mean_turun = self.monotone_decreasing()
        #         self.list_entropy_luar.append(self.list_entropy_dalam)
        #         # self.list_entropy_luar = []
        #         count_data = 0
        #         counter += 1
        #     else:
        #         entropy_value = self.entropy_calculate(df_test.values)
        #         self.list_entropy_dalam.append(entropy_value)
        #         self.list_entropy_dalam = []
        #         count_data += 1
        #         self.current_count += self.cut_value

        return

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


def main():
    dataset_path = "semi_processed_train.csv"

    # Load Dataset Value to Dataframe
    df = pd.read_csv(dataset_path, sep=",")
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    # getting sample of current dataframe
    # df = df.head(10000)

    # splitting data
    x = df[df.columns[:5]]
    y = df["label"]

    model = entropy_model(10, 10)
    df_entropy = model.calculate_all_entropy(x)
    threshold = np.mean(df_entropy)

    # 2.782777146007937

    model.get_entropy_prediction(x)
    predict_result = model.get_prediction_result(threshold)

    print(confusion_matrix(y, predict_result))
    print(classification_report(y, predict_result))
    print("Accuracy:", accuracy_score(y, predict_result) * 100)


if __name__ == "__main__":
    main()
