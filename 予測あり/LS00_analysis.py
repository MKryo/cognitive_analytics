import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# データ読み込み
df_est = pd.read_csv('estimations_ls00_cre.csv')
df_pred = pd.read_csv('predictions_ls00_cre.csv')

# 推定値データを動物ごとに振り分け
df_est_mouse = df_est[df_est['animal'] == 'mouse']
df_est_rabbit = df_est[df_est['animal'] == 'rabbit']
df_est_pigeon = df_est[df_est['animal'] == 'pigeon']

# マウス # ΔP = 0.70
df_est_mouse_each = [0,0,0,0,0,0]
df_est_mouse_each_mean = []
for i in range(5):
    df_est_mouse_each[i] = df_est_mouse[df_est_mouse['est_i'] == i+1]
df_est_mouse_each[5] = df_est_mouse[df_est_mouse['est_i'] == 0]
for i in range(len(df_est_mouse_each)):
    df_est_mouse_each_mean.append(df_est_mouse_each[i]['estimation'].mean())
# print(df_est_mouse_each_mean)

# うさぎ # ΔP = 0.47
df_est_rabbit_each = [0,0,0,0,0,0]
df_est_rabbit_each_mean = []
for i in range(5):
    df_est_rabbit_each[i] = df_est_rabbit[df_est_rabbit['est_i'] == i+1]
df_est_rabbit_each[5] = df_est_rabbit[df_est_rabbit['est_i'] == 0]
for i in range(len(df_est_rabbit_each)):
    df_est_rabbit_each_mean.append(df_est_rabbit_each[i]['estimation'].mean())
# print(df_est_rabbit_each_mean)

# はと # ΔP = 0.23
df_est_pigeon_each = [0,0,0,0,0,0]
df_est_pigeon_each_mean = []
for i in range(5):
    df_est_pigeon_each[i] = df_est_pigeon[df_est_pigeon['est_i'] == i+1]
df_est_pigeon_each[5] = df_est_pigeon[df_est_pigeon['est_i'] == 0]
for i in range(len(df_est_pigeon_each)):
    df_est_pigeon_each_mean.append(df_est_pigeon_each[i]['estimation'].mean())
# print(df_est_pigeon_each_mean)

# それぞれのリストからDFを作成
Blocks_of_Trials = [1,2,3,4,5,6]
df = pd.DataFrame({'Blocks_of_Trials':Blocks_of_Trials , '0.70(mouse)':df_est_mouse_each_mean, '0.47(rabbit)':df_est_rabbit_each_mean, '0.23(pigeon)':df_est_pigeon_each_mean})

# 各動物ごとの推定値の平均グラフ描画
df.plot(title='Estimate Mean',grid=True,x=df.columns[0], xlabel='Blocks of Trials', ylabel='Estimated Causal Relationship', ylim=[40,80])
# plt.show()

# モデル定義
# ΔP
def deltaP (a, b, c, d) :
    return (a / (a+b)) - (c / (c+d))
# DFH
def DFH (a, b, c, d):
    return a / math.sqrt((a+b)*(a+c))
# pARIs
def pARIs (a, b, c, d):
    return a / (a+b+c)


# マウス刺激 
df_pred_mouse_b = [0,0,0,0,0,0]
a = [0,0,0,0,0,0]
b = [0,0,0,0,0,0]
c = [0,0,0,0,0,0]
d = [0,0,0,0,0,0]
ΔP_pre = [0,0,0,0,0,0]
DFH_pre = [0,0,0,0,0,0]
pARIs_pre = [0,0,0,0,0,0]

for i in range(6):
    df_pred_mouse = df_pred[df_pred['animal']=='mouse']
    df_pred_mouse_b[i] = df_pred_mouse[(df_pred_mouse['pred_i']>=0) & (df_pred_mouse['pred_i']<=(10*i) + 9)]
    a[i] = len(df_pred_mouse_b[i][df_pred_mouse_b[i]['stimulation']=='a'])
    b[i] = len(df_pred_mouse_b[i][df_pred_mouse_b[i]['stimulation']=='b'])
    c[i] = len(df_pred_mouse_b[i][df_pred_mouse_b[i]['stimulation']=='c'])
    d[i] = len(df_pred_mouse_b[i][df_pred_mouse_b[i]['stimulation']=='d'])
    ΔP_pre[i] = deltaP(a[i], b[i], c[i], d[i]) * 100
    DFH_pre[i] = DFH(a[i], b[i], c[i], d[i]) * 100
    pARIs_pre[i] = pARIs(a[i], b[i], c[i], d[i]) * 100
# print('ΔP: ', ΔP_pre)
# print('DFH: ', DFH_pre)
# print('pARIs: ', pARIs_pre)
# print('mean: ', df_est_mouse_each_mean)

# それぞれのリストからDFを作成
Blocks_of_Trials = [1,2,3,4,5,6]
df_mouse = pd.DataFrame({'Blocks_of_Trials':Blocks_of_Trials , 'ΔP':ΔP_pre, 'DFH':DFH_pre, 'pARIs':pARIs_pre, 'human':df_est_mouse_each_mean})
df_mouse.head(6)
# マウス設定のグラフ描画
df_mouse.plot(title='mouse', grid=True, x=df_mouse.columns[0], xlabel='Blocks of Trials', ylabel='Estimated Causal Relationship', ylim=[0,100])
# plt.show()
# 相関係数
human = np.array(df_mouse['human'])
dfhcoef = np.corrcoef(human, np.array(df_mouse['DFH']))
pariscoef = np.corrcoef(human, np.array(df_mouse['pARIs']))
deltapcoef = np.corrcoef(human, np.array(df_mouse['ΔP']))
print('mouse DFH corr: ', dfhcoef[0,1])
print('mouse pARIs corr: ',pariscoef[0,1])
print('mouse ΔP corr: ',deltapcoef[0,1])
# 決定係数
print('mouse DFH r2_score:', r2_score(df_mouse['human'], df_mouse['DFH']))
print('mouse pARIs r2_score:', r2_score(df_mouse['human'], df_mouse['pARIs']))
print('mouse ΔP r2_score:', r2_score(df_mouse['human'], df_mouse['ΔP']))


# ウサギ刺激 
df_pred_rabbit_b = [0,0,0,0,0,0]
a = [0,0,0,0,0,0]
b = [0,0,0,0,0,0]
c = [0,0,0,0,0,0]
d = [0,0,0,0,0,0]
ΔP_pre = [0,0,0,0,0,0]
DFH_pre = [0,0,0,0,0,0]
pARIs_pre = [0,0,0,0,0,0]

for i in range(6):
    df_pred_rabbit = df_pred[df_pred['animal']=='rabbit']
    df_pred_rabbit_b[i] = df_pred_rabbit[(df_pred_rabbit['pred_i']>=0) & (df_pred_rabbit['pred_i']<=(10*i) + 9)]
    a[i] = len(df_pred_rabbit_b[i][df_pred_rabbit_b[i]['stimulation']=='a'])
    b[i] = len(df_pred_rabbit_b[i][df_pred_rabbit_b[i]['stimulation']=='b'])
    c[i] = len(df_pred_rabbit_b[i][df_pred_rabbit_b[i]['stimulation']=='c'])
    d[i] = len(df_pred_rabbit_b[i][df_pred_rabbit_b[i]['stimulation']=='d'])
    ΔP_pre[i] = deltaP(a[i], b[i], c[i], d[i]) * 100
    DFH_pre[i] = DFH(a[i], b[i], c[i], d[i]) * 100
    pARIs_pre[i] = pARIs(a[i], b[i], c[i], d[i]) * 100
# print('ΔP: ', ΔP_pre)
# print('DFH: ', DFH_pre)
# print('pARIs: ', pARIs_pre)
# print('mean: ', df_est_rabbit_each_mean)

# それぞれのリストからDFを作成
Blocks_of_Trials = [1,2,3,4,5,6]
df_rabbit = pd.DataFrame({'Blocks_of_Trials':Blocks_of_Trials , 'ΔP':ΔP_pre, 'DFH':DFH_pre, 'pARIs':pARIs_pre, 'human':df_est_rabbit_each_mean})
df_rabbit.head(6)
# ウサギ設定のグラフ描画
df_rabbit.plot(title='rabbit', grid=True, x=df_rabbit.columns[0], xlabel='Blocks of Trials', ylabel='Estimated Causal Relationship', ylim=[0,100])
# plt.show()
# 相関係数
human = np.array(df_rabbit['human'])
dfhcoef = np.corrcoef(human, np.array(df_rabbit['DFH']))
pariscoef = np.corrcoef(human, np.array(df_rabbit['pARIs']))
deltapcoef = np.corrcoef(human, np.array(df_rabbit['ΔP']))
print('rabbit DFH corr: ', dfhcoef[0,1])
print('rabbit pARIs corr: ',pariscoef[0,1])
print('rabbit ΔP corr: ',deltapcoef[0,1])
# 決定係数
print('rabbit DFH r2_score:', r2_score(df_rabbit['human'], df_rabbit['pARIs']))
print('rabbit pARIs r2_score:', r2_score(df_rabbit['human'], df_rabbit['DFH']))
print('rabbit ΔP r2_score:', r2_score(df_mouse['human'], df_mouse['ΔP']))

# ハト刺激 
df_pred_pigeon_b = [0,0,0,0,0,0]
a = [0,0,0,0,0,0]
b = [0,0,0,0,0,0]
c = [0,0,0,0,0,0]
d = [0,0,0,0,0,0]
ΔP_pre = [0,0,0,0,0,0]
DFH_pre = [0,0,0,0,0,0]
pARIs_pre = [0,0,0,0,0,0]

for i in range(6):
    df_pred_pigeon = df_pred[df_pred['animal']=='pigeon']
    df_pred_pigeon_b[i] = df_pred_pigeon[(df_pred_pigeon['pred_i']>=0) & (df_pred_pigeon['pred_i']<=(10*i) + 9)]
    a[i] = len(df_pred_pigeon_b[i][df_pred_pigeon_b[i]['stimulation']=='a'])
    b[i] = len(df_pred_pigeon_b[i][df_pred_pigeon_b[i]['stimulation']=='b'])
    c[i] = len(df_pred_pigeon_b[i][df_pred_pigeon_b[i]['stimulation']=='c'])
    d[i] = len(df_pred_pigeon_b[i][df_pred_pigeon_b[i]['stimulation']=='d'])
    ΔP_pre[i] = deltaP(a[i], b[i], c[i], d[i]) * 100
    DFH_pre[i] = DFH(a[i], b[i], c[i], d[i]) * 100
    pARIs_pre[i] = pARIs(a[i], b[i], c[i], d[i]) * 100
# print('ΔP: ', ΔP_pre)
# print('DFH: ', DFH_pre)
# print('pARIs: ', pARIs_pre)
# print('mean: ', df_est_pigeon_each_mean)

# それぞれのリストからDFを作成
Blocks_of_Trials = [1,2,3,4,5,6]
df_pigeon = pd.DataFrame({'Blocks_of_Trials':Blocks_of_Trials , 'ΔP':ΔP_pre, 'DFH':DFH_pre, 'pARIs':pARIs_pre, 'human':df_est_pigeon_each_mean})
df_pigeon.head(6)
# ハト設定のグラフ描画
df_pigeon.plot(title='pigeon', grid=True, x=df_pigeon.columns[0], xlabel='Blocks of Trials', ylabel='Estimated Causal Relationship', ylim=[0,100])
plt.show()
# 相関係数
human = np.array(df_pigeon['human'])
dfhcoef = np.corrcoef(human, np.array(df_pigeon['DFH']))
pariscoef = np.corrcoef(human, np.array(df_pigeon['pARIs']))
deltapcoef = np.corrcoef(human, np.array(df_pigeon['ΔP']))
print('pigeon DFH corr: ', dfhcoef[0,1])
print('pigeon pARIs corr: ',pariscoef[0,1])
print('pigeon ΔP corr: ',deltapcoef[0,1])
# 決定係数
print('pigeon DFH r2_score:', r2_score(df_pigeon['human'], df_pigeon['pARIs']))
print('pigeon pARIs r2_score:', r2_score(df_pigeon['human'], df_pigeon['DFH']))
print('pigeon ΔP r2_score:', r2_score(df_mouse['human'], df_mouse['ΔP']))
