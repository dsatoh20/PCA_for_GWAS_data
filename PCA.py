### numpyだけでPCAを実装
# ところどころコメントアウトしているコードは.ipynbで実行したときのもの

import pandas as pd
import datetime
import time
import numpy as np
import numpy.linalg as LA

from var import var
from covar import covar

# 不偏分散を定義
def var_(x):
    n = len(x)
    s = var(x) * n / (n-1)
    return s
def covar_(x,y):
    n = len(x)
    s = covar * n / (n-1)
    return s
def correl(sx,sy,sxy):
    r = sxy / (sx * sy)**0.5
    return r

npz = np.load("SNP_data.npz", allow_pickle=True)
data = pd.DataFrame(npz["arr_0"])

n = len(data)
p = len(data.columns)
data = data.astype("float64")
start = time.time()
data_center = np.array(data)

means = np.mean(data, axis=0)
for i in range(p):
    data_center[:,i] -= means[i]
data_center = pd.DataFrame(data_center)
end = time.time()
print(end-start, "seconds")
# data_center

# 標本分散共分散行列の作成 方法1
S = np.empty((p,1))
data = np.array(data)
start = time.time()
for j in range(p):
    sj_vec = []
    for k in range(p):
        sjk = covar(data[:,j], data[:,k])
        sj_vec.append(sjk)
    sj_vec = np.array([sj_vec]).T
    S = np.concatenate([S,sj_vec],1)
    print(p-j-1, "patches left")
S = S[:, 1:]
end = time.time()
print(end-start, "seconds")
# S
"""
# 標本分散共分散行列の作成 方法2
start = time.time()

data = np.array(data).T
S = np.cov(data)

end = time.time()
print(end-start)

# S.shape

# 標本分散共分散行列の作成 方法3
S = np.empty((p,1))
data = np.array(data)
start = time.time()
for j in range(p):
    sj_vec = []
    for k in range(p):
        sjk = np.cov(data[:,j], data[:,k])
        sj_vec.append(sjk)
    sj_vec = np.array([sj_vec]).T
    S = np.concatenate([S,sj_vec],1)
    print(p-j-1, "patches left")
S = S[:, 1:]
end = time.time()
print(end-start, "seconds")
# S 
"""

# 固有値問題Ru=λuを解く
start = time.time()
w, v = LA.eig(S)
end = time.time()
print(end-start, "seconds")
print("w:", w)
print("v:", v)

# 固有ベクトル
df_v = pd.DataFrame(v, index=data.columns)
# df_v

# 主成分得点 new_data
new_data = np.dot(data_center.values, v)
new_data = pd.DataFrame(new_data, index=data_center.index)
# new_data

# 主成分で散布図を描画
import matplotlib.pyplot as plt
%matplotlib inline
PC1 = new_data[0].values
PC2 = new_data[1].values
PC3 = new_data[2].values
plt.scatter(PC1, PC2, s=10)
plt.axis('square')
plt.show()

# PC1とPC3で描画
plt.scatter(PC1,PC3, s=10)
plt.show()

# 寄与率を求める
w_sum = sum(w)
contri_rate = w/w_sum
contri_rate = pd.DataFrame(contri_rate, columns=['寄与率'])
# contri_rate

# 主成分負荷量
PCL = pd.DataFrame()
for i in range(len(w)):
    ind = df_v[i].values
    ind = ind * (w[i] ** 0.5) / var(data[data.columns[i]])
    ind = pd.DataFrame(ind)
    PCL = pd.concat([PCL, ind], axis='columns')
PCL.columns = [x for x in range(len(PCL.columns))]
PCL.index = data.columns
# PCL
