from math import exp
from random import normalvariate

import numpy as np
from numpy import shape, zeros, ones, multiply

import torch
import torch.nn
import torch.utils.data as Data
import matplotlib.pyplot as plt
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

def preprocessData(data):
    feature=np.array(data.iloc[:,:-1])   #取特征
    label=data.iloc[:,-1].map(lambda x: 1 if x==1 else -1) #取标签并转化为 +1，-1
    #将数组按行进行归一化
    zmax, zmin = feature.max(axis=0), feature.min(axis=0)
    feature = (feature - zmin) / (zmax - zmin)
    label=np.array(label)

    return feature,label
#定义激活函数
def sigmoid(inx):
    # return 1. / (1. + exp(-max(min(inx, 15.), -15.)))
    return 1.0 / (1 + exp(-inx))

def SGD_FM(dataMatrix, classLabels, k, iter):
    '''
    :param dataMatrix:  特征矩阵
    :param classLabels: 类别矩阵
    :param k:           辅助向量的大小
    :param iter:        迭代次数
    :return:
    '''
    # dataMatrix用的是mat, classLabels是列表
    m, n = shape(dataMatrix)   #矩阵的行列数，即样本数和特征数
    print(m, n)
    alpha = 0.01
    # 初始化参数
    # w = random.randn(n, 1)#其中n是特征的个数
    w = zeros((n, 1))      #一阶特征的系数
    w_0 = 0.00
    v = normalvariate(0, 0.2) * ones((n, k))   #即生成辅助向量，用来训练二阶交叉特征的系数

    for it in range(iter):
        for x in range(m):  # 随机优化，每次只使用一个样本
            # 二阶项的计算
            inter_1 = dataMatrix[x] * v
            inter_2 = multiply(dataMatrix[x], dataMatrix[x]) * multiply(v, v)  #二阶交叉项的计算
            interaction = sum(multiply(inter_1, inter_1) - inter_2) / 2.       #二阶交叉项计算完成

            p = w_0 + dataMatrix[x] * w + interaction  # 计算预测的输出，即FM的全部项之和

            loss = 1-sigmoid(classLabels[x] * p[0, 0])    #计算损失

            w_0 = w_0 +alpha * loss * classLabels[x]

            for i in range(n):
                if dataMatrix[x, i] != 0:
                    w[i, 0] = w[i, 0] +alpha * loss * classLabels[x] * dataMatrix[x, i]
                    for j in range(k):
                        v[i, j] = v[i, j]+ alpha * loss * classLabels[x] * (
                        dataMatrix[x, i] * inter_1[0, j] - v[i, j] * dataMatrix[x, i] * dataMatrix[x, i])
        print("第{}次迭代后的损失为{}".format(it, loss))

    return w_0, w, v

def getAccuracy(dataMatrix, classLabels, w_0, w, v):
    m, n = shape(dataMatrix)
    allItem = 0
    error = 0
    result = []
    for x in range(m):   #计算每一个样本的误差
        allItem += 1
        inter_1 = dataMatrix[x] * v
        inter_2 = multiply(dataMatrix[x], dataMatrix[x]) * multiply(v, v)
        interaction = sum(multiply(inter_1, inter_1) - inter_2) / 2.
        p = w_0 + dataMatrix[x] * w + interaction  # 计算预测的输出

        pre = sigmoid(p[0, 0])
        print(p)

        result.append(pre)

        if pre < 0.5 and classLabels[x] == 1.0:
            error += 1
        elif pre >= 0.5 and classLabels[x] == -1.0:
            error += 1
        else:
            continue
    plt.plot(p, pre, color="r", linestyle="-", linewidth=1)
    plt.show()
    return float(error) / allItem

# 搭建神经网络
class Net(torch.nn.Module):

    def __init__(self, n_input, n_hidden, n_output):
        super(Net, self).__init__()  # 继承init的功能
        self.hidden_layer = torch.nn.Linear(n_input, n_hidden)
        self.output_layer = torch.nn.Linear(n_hidden, n_output)

    def forward(self, input):
        x = torch.relu(self.hidden_layer(input))
        output = self.output_layer(x)
        return output
# 超参数
LR = 0.01
batch_size = 10
epoches = 3
torch.manual_seed(15)

# 准备数据
x = torch.unsqueeze(torch.linspace(-1, 1, 1000), dim=1)
y = x.pow(2)

plt.scatter(x.numpy(), y.numpy())
plt.show()

dataset = Data.TensorDataset(x, y)
loader = Data.DataLoader(
    dataset=dataset,
    batch_size=batch_size,
    shuffle=True,
    num_workers=2)


def train():
    net_SGD = Net(1, 20, 1)
    net_Momentum = Net(1, 20, 1)
    net_RMSprop = Net(1, 20, 1)
    net_Adam = Net(1, 20, 1)
    nets = [net_SGD, net_Momentum, net_RMSprop, net_Adam]

    # 定义优化器
    optimizer_SGD = torch.optim.SGD(net_SGD.parameters(), lr=LR)
    optimizer_Momentum = torch.optim.SGD(net_Momentum.parameters(), lr=LR, momentum=0.8)
    optimizer_RMSprop = torch.optim.RMSprop(net_RMSprop.parameters(), lr=LR, alpha=0.9)
    optimizer_Adam = torch.optim.Adam(net_Adam.parameters(), lr=LR, betas=(0.9, 0.99))
    optimizers = [optimizer_SGD, optimizer_Momentum, optimizer_RMSprop, optimizer_Adam]

    # 定义损失函数
    loss_function = torch.nn.MSELoss()
    losses = [[], [], [], []]

    for epoch in range(epoches):
        for step, (batch_x, batch_y) in enumerate(loader):
            for net, optimizer, loss_list in zip(nets, optimizers, losses):
                pred_y = net(batch_x)
                loss = loss_function(pred_y, batch_y)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                loss_list.append(loss.data.numpy())

    labels = ['SGD', 'Momentum', 'RMSprop', 'Adam']
    for i, loss in enumerate(losses):
        plt.plot(loss, label=labels[i])
    plt.legend(loc='best')
    plt.xlabel('Steps')
    plt.ylabel('Loss')
    plt.ylim((0, 0.2))
    plt.show()

if __name__ == "__main__":
    train()
