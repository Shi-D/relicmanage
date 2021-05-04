from math import sqrt
from numpy import concatenate
from matplotlib import pyplot
from pandas import read_csv
from pandas import DataFrame
from pandas import concat
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import matplotlib.pyplot as plt
import pandas as pd
import csv
import numpy as np


def data_load(data_path):
    with open(data_path, 'r') as f:
        reader = csv.reader(f)
        data = pd.DataFrame(reader)
        return data
    return None



DATA_NUM = 330
DIVISION_LINE = 280
TIME_STAMP = 10

EPOCHS = 10
BATCH_SIZE = 20

data_path = 'museum.csv'
data = data_load(data_path)
data = data[[1, 2, 3, 4]]
# 划分训练集和验证集
data_train = data[0: DIVISION_LINE+TIME_STAMP]
data_valid = data[DIVISION_LINE-TIME_STAMP: DATA_NUM]

# plt.plot(data_train[1])
# plt.show()

data_train = data_train.values
data_valid = data_valid.values
print('data_train', data_train)
print('data_valid', data_valid)

# 训练集
x_train, y_train = [], []
for i in range(TIME_STAMP, len(data_train)):
    x_train.append(data_train[i - TIME_STAMP: i])
    y_train.append(data_train[i, 1])

x_train = np.array(x_train)
y_train = np.array(y_train)
print(x_train.shape)
print(y_train.shape)

# 验证集
x_valid, y_valid = [], []
print(data_valid.shape)
for i in range(TIME_STAMP, len(data_valid)):
    x_valid.append(data_valid[i - TIME_STAMP: i])
    y_valid.append(data_valid[i, 1])

x_valid = np.array(x_valid)
y_valid = np.array(y_valid)
print(x_valid.shape)
print(y_valid.shape)


model = Sequential()
model.add(LSTM(units=100, return_sequences=True, input_shape=(x_train.shape[1], x_train.shape[2])))
model.add(LSTM(units=50))
model.add(Dense(1))
model.compile(loss='mae', optimizer='adam')
history = model.fit(x_train, y_train, epochs=EPOCHS, batch_size=BATCH_SIZE, verbose=1, shuffle=False)


number = model.predict(x_valid)


# print(y_valid)
# print(closing_price)
rms = np.sqrt(np.mean(np.power((y_valid - number), 2)))
print(rms)
print(number.shape)
print(y_valid.shape)


plt.figure(figsize=(16, 8))
dict_data = {
    'Predictions': number.reshape(1, -1)[0],
    'Close': y_valid[0]
}
data_pd = pd.DataFrame(dict_data)


plt.plot(data_pd[['Close', 'Predictions']])
plt.show()