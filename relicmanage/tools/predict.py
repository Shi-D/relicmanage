import torch as t
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import torch.nn.functional as F
import csv
import pandas as pd
from DNN import *


def data_load(data_path):
    with open(data_path, 'r') as f:
        reader = csv.reader(f)
        data = pd.DataFrame(reader)
        return data
    return None

net = t.load('DNNnet.pkl')

output = []
with open('output.txt', 'r') as f:
    for i in range(330):
        data = f.readline()
        output.append(int(float(data)))

print('output', output)


x_predict = [[330, 0, 0, 0], [331, 1, 0, 0], [332, 1, 0, 0], [333, 0, 0, 0], [334, 0, 1, 0]]
predict = net(t.tensor(x_predict))
predict = predict.detach().numpy()
print('predict0', predict)
predict = [int(i[0]) for i in predict]
print('predict', predict)
with open('predict.txt', 'w') as f:
    for i in predict:
        f.write(str(i)+'\n')

data_path = 'museum.csv'
data = data_load(data_path)
y_train = data[[2]]
y_train = y_train.values
y_train = y_train[1:]
y = []
for i in y_train:
    y.append(int(i[0]))
print('y', y)

x = [i for i in range(330)]
print('x', x)

plot_x = [i for i in range(330, 335)]
plt.plot(x, output, color='#C25E6E', label='fit')
plt.plot(x, y, color='#B4E3DA', label='true')
plt.scatter(plot_x, predict, color='#7779A8', label='predict')
for (i, px) in enumerate(plot_x):
    plt.text(px, predict[i], predict[i], ha='center', va='bottom', fontsize=10)


plt.legend()
plt.show()

