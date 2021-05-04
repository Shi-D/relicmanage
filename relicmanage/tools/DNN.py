import torch as t
# import matplotlib.pyplot as plt
import torch.nn.functional as F
import csv
import pandas as pd
import numpy as np


def data_load(data_path):
    with open(data_path, 'r') as f:
        reader = csv.reader(f)
        data = pd.DataFrame(reader)
        return data
    return None


class Net(t.nn.Module):
    def __init__(self, n_feature, n_hidden1, n_hidden2, n_hidden3, n_output):
        super(Net, self).__init__()  # 继承 __init__ 功能
        # 定义每层用什么样的形式
        self.layer1 = t.nn.Linear(n_feature, n_hidden1)  # 隐藏层线性输出
        self.layer2 = t.nn.Linear(n_hidden1, n_hidden2)  # 隐藏层线性输出
        self.layer3 = t.nn.Linear(n_hidden2, n_hidden3)  # 隐藏层线性输出
        self.predict = t.nn.Linear(n_hidden3, n_output)  # 输d出层线性输出

    def forward(self, x):  # 这同时也是 Module 中的 forward 功能
        x = x.float()
        # 正向传播输入值, 神经网络分析出输出值
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        x = F.relu(self.layer3(x))
        # 最后一层输出不需要relu
        x = self.predict(x)
        return x


LEARNING_RATE = 0.1
EPOCHS = 1000
DATA_NUM = 330



data_path = 'museum.csv'
data = data_load(data_path)
x_train = data[[0, 3, 4, 5]]
x_train = x_train.values
y_train = data[[2]]
y_train = y_train.values

x_train = x_train[1:]
y_train = y_train[1:]

x_train = x_train.astype(float)  # numpy强制类型转换
y_train = y_train.astype(float)  # numpy强制类型转换
x_train = t.tensor(x_train)
y_train = t.tensor(y_train)


net = Net(n_feature=4, n_hidden1=8, n_hidden2=16, n_hidden3=4, n_output=1)
print(net)

optimizer = t.optim.Adam(net.parameters(), lr=LEARNING_RATE)  # 传入 net 的所有参数, 学习率
loss_func = t.nn.MSELoss()  # 预测值和真实值的误差计算公式 (均方差)


for i in range(EPOCHS):
    inputs = t.autograd.Variable(x_train)
    target = t.autograd.Variable(y_train)
    target = target.float()

    output = net(inputs)  # 喂给 net 训练数据 x, 输出预测值

    output = output.float()

    loss = loss_func(output, target)  # 计算两者的误差

    if i % 50 == 0:
        print('loss', loss)
    loss = loss.float()

    optimizer.zero_grad()  # 清空上一步的残余更新参数值
    loss.backward()  # 误差反向传播, 计算参数更新值
    optimizer.step()  # 将参数更新值施加到 net 的 parameters 上


t.save(net, 'DNNnet2.pkl')



