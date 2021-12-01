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
        return entropy(dist, base=2.0)

    # Fungsi Cek Nilai Monoton Turun
    def monotone_decreasing(self, list_value):
        pairs = zip(list_value, list_value[:0])
        return all(itertools.starmap(operator.ge, pairs))

    def labelling_data(self, x, threshold):
        for j in x:
            for i in range(len(j)):
                # for i in j:
                if j[i] > threshold:
                    self.hasil.append(1)
                else:
                    self.hasil.append(0)

    # threshold  updated by windows size max mean (local mean not dataframe mean)
    def labelling_data_dynamic(self, list_nilai, list_mean):
        threshold = 0
        for j in list_nilai:
            threshold = max(j)
            for i in range(len(j)):
                # for i in j:
                if j[i] > threshold:
                    self.hasil.append(1)
                else:
                    self.hasil.append(0)

    def create_prediction_result_individual(self, list_data, threshold):
        for x in list_data:
            self.labelling_data(x[0], threshold)

    def get_entropy_prediction_individual(self, df, threshold):
        count = 0
        windows_size = self.cut_value
        list_entropy = list()
        for x, y in df.iterrows():
            entropy_values = self.entropy_calculate(y.values)
            if entropy_values > threshold:
                self.hasil.append(1)
            else:
                self.hasil.append(0)
        return self.hasil

    # Calculate Mean

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
                # threshold = max(list_nilai[list_mean.index(max(list_mean))])
                if check_monoton_turun:
                    # print("Intrusi Terjadi")
                    self.labelling_data(list_nilai, threshold)
                    # self.labelling_data_dynamic(list_nilai, list_mean)
                else:
                    self.labelling_data(list_nilai, threshold)
                    # self.labelling_data_dynamic(list_nilai, list_mean)
                count_data = 0
                list_nilai = []
                list_mean = []
            count_data += 1
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
        return

    def old_entropy_value_count(self):
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
        pass

    # Getter Value

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

    ########################################## NEW CODE ################################################
    # Calculate Entropy Value and Cut on Windows Size

    # nilai pada log bisa diganti menjadi basis 2 atau 10 dikarenakan rumusan menghitung shannon entropy
    def entropy_calculate_2(self, s):
        x_value = [x for x, n_x in collections.Counter(s).items()]
        probabilities = [n_x / len(s) for x, n_x in collections.Counter(s).items()]
        e_x = [-p_x * math.log(p_x, 2) for p_x in probabilities]
        entropy_df = dict(zip(x_value, e_x))
        return entropy_df

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
                    entropy_value = self.entropy_calculate_2(list_output)
                    mean_value = self.search_threshold(entropy_value)
                    list_luar.append([entropy_value, mean_value, list_output])
                self.list_entropy_luar.append(list_luar)
                self.list_entropy_dalam = []
                list_luar = []
                counter = 0
            counter += 1

        # input Last Value Group Value
        for i in range(df_columns_len):
            list_output = self.create_toList(self.list_entropy_dalam, i)
            entropy_value = self.entropy_calculate_2(list_output)
            mean_value = self.search_threshold(entropy_value)
            list_luar.append([entropy_value, mean_value, list_output])
        self.list_entropy_luar.append(list_luar)
        self.list_entropy_dalam = []
        return

    # patokan menggunakan SRCIP namun sistem sudah dinamis sisa dipikirkan bagaimana bila ada lebih dari satu fitur yang dimasukann
    def new_label(self, list_entropy, listdata, status, iterasi):
        # use status[iterasi].get(x) if threshold using dict
        counter_data = 0
        loop_data = len(list_entropy)
        for x in listdata:
            if (list_entropy.get(x) == None) or (status[iterasi] == None):
                continue
            elif list_entropy.get(x) < status[iterasi]:
                self.hasil.append(1)
            else:
                self.hasil.append(0)
        return

    def loop_hasil(self, listdata, list_threshold):
        threshold_list = list_threshold
        counter_data = 0
        data_count = 0
        list_mean = list()
        iterasi = 1
        for x in listdata:
            data_count = len(x)
            if counter_data > self.mean_count:
                check_monotone_value = self.monotone_decreasing(list_mean)
                # buka komentar ketika sudah ingin implementasi dengan sistem deteksi
                # if check_monotone_value:
                #     print("Instrusi Terjadi")
                # else:
                #     print("Jaringan Normal")
                list_mean = []
                counter_data = 0

            for j in x:
                # Note saat ini cuma melihat SRCIP saja
                if iterasi >= data_count:
                    iterasi = 1
                    break
                else:
                    self.new_label(j[0], j[2], threshold_list, iterasi - 1)
                    list_mean.append(j[1])
                    iterasi += 1
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
    threshold_value = model.check_entropy_all(x)

    # Skenario menggunakan max_threshold
    max_threshold = model.check_maximum_entropy(threshold_value)

    model.new_get_entropy_prediction(x)
    list_luar = model.get_list_luar()

    predict_result = model.loop_hasil(list_luar, max_threshold)

    print(confusion_matrix(y, predict_result))
    print(classification_report(y, predict_result))
    print(
        "Accuracy:", accuracy_score(y, predict_result) * 100,
    )

    ######################## OLD SCENARIO ###################################
    # splitting data (bisa dipilih menggunakan yang mana)
    # x = df[df.columns[:17]]
    # x = df[["pktcount", "bytecount", "Protocol"]]
    # y = df["label"]

    # normalize data for same range
    # x = normalization_dataset(x)

    # windows size dan count size bisa diganti saat membangun model
    # model = entropy_model(18, 10)
    # df_entropy = model.calculate_all_entropy(x)

    # threshold bisa diganti dengan nilai terbesar/nilai mean/nilai yang didefinisikan sendiri
    # 2.782777146007937
    # threshold = np.mean(df_entropy)

    # model.check_entropy_value(x)

    # Mean Testing Model

    # model.get_entropy_prediction(x)
    # predict_result = model.get_prediction_result(threshold)

    # print("Mean Version")
    # print(confusion_matrix(y, predict_result))
    # print(classification_report(y, predict_result))
    # print(
    #     "Accuracy:", accuracy_score(y, predict_result) * 100)

    # Individual Comparising to Threshold Testing Value (Perlu di evaluasi karena metode kurang pas)

    # dapat diganti count size dan windows sizenya
    # model_2 = entropy_model(10, 10)

    # threshold bisa diganti dengan nilai terbesar/nilai mean/nilai yang didefinisikan sendiri
    # threshold_2 = max(df_entropy)

    # predict_result_individual = model_2.get_entropy_prediction_individual(
    #     x, threshold_2
    # )

    # print("Individual Version")
    # print(confusion_matrix(y, predict_result_individual))
    # print(
    #     classification_report(
    #         y, predict_result_individual, labels=np.unique(predict_result_individual)
    #     )
    # )
    # print("Accuracy:", accuracy_score(y, predict_result_individual) * 100)


if __name__ == "__main__":
    main()
