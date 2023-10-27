# scikit-learnを用いてGWASデータのPCAを行う

import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

npz = np.load("SNP_data.npz", allow_pickle=True)
data = pd.DataFrame(npz["arr_0"])
# data

start = time.time()
pca = PCA()  # PCA を行ったり PCA の結果を格納したりするための変数を、pca として宣言
pca.fit(data)  # PCA を実行
end = time.time()

# print(end-start)

loadings = pd.DataFrame(pca.components_.T)
# loadings

score = pd.DataFrame(pca.transform(data))
# score

# 寄与率を算出
contribution_ratios = pd.DataFrame(pca.explained_variance_ratio_)
# contribution_ratios

# 累積寄与率を算出（.cusum()で累積和を計算 .sum()では総和しか得られない）
cumulative_contribution_ratios = contribution_ratios.cumsum()
# cumulative_contribution_ratios


# 以下、グラフの描画をする
from pyplink import PyPlink
pyp = PyPlink('Illu_East-Asian_HapMap3_JPT+CHB_set2') # plink形式ファイルの読み込み
fam = pyp.get_fam()
status = fam["status"] # 地域を取り出す

# 各地域に割り当てる色を決める
region = "Okinawa" # 任意の地域
num = 0
color = []
for i in range(len(status)):
    if region == status[i]:
        color.append(num)
    else:
        region = status[i]
        num += 1
        color.append(num)
        print(region)
# color

score_status = pd.concat([score, status], axis=1)

# 地域ごとにスコアを取り出す
Okinawa = score_status[score_status["status"] == "Okinawa"].drop("status", axis=1)
Miyako = score_status[score_status["status"] == "Miyako"].drop("status", axis=1)
Yaeyama = score_status[score_status["status"] == "Yaeyama"].drop("status", axis=1)
MainlandJapan = score_status[score_status["status"] == "Mainland-Japan"].drop("status", axis=1)
Korea = score_status[score_status["status"] == "Korea"].drop("status", axis=1)
HapMap3_JPT = score_status[score_status["status"] == "HapMap3_JPT"].drop("status", axis=1)
HapMap3_CHB = score_status[score_status["status"] == "HapMap3_CHB"].drop("status", axis=1)

fig = plt.figure()
regions = ["Okinawa", "Miyako", "Yaeyama", "Mainland-Japan", "Korea", "HapMap3_JPT", "HapMap3_CHB"]
score_regions = [Okinawa, Miyako, Yaeyama, MainlandJapan, Korea, HapMap3_JPT, HapMap3_CHB]
for i in range(len(regions)):
    plt.scatter(score_regions[i].iloc[:,0], score_regions[i].iloc[:,1], cmap=plt.get_cmap("jet"), s=10, label=regions[i]) # 第一主成分、第二主成分を用いる
    plt.xlabel('Component1')
    plt.ylabel('Component2')
    plt.legend(loc="upper right")
plt.show()
fig.savefig("skpca1_2.png") # skpca1_2.pngとして画像を保存
