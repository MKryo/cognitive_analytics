import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

# データ読み込み ls00exp123
# 3 は実験の回数
df_est_ls = [0]*3
df_est_ls[0] = pd.read_csv('/Users/bezi/cognitive_analytics/ls00_exp123_data/res_estimations_exp1_ls00.csv')
df_est_ls[1] = pd.read_csv('/Users/bezi/cognitive_analytics/ls00_exp123_data/res_estimations_exp2_ls00.csv')
df_est_ls[2] = pd.read_csv('/Users/bezi/cognitive_analytics/ls00_exp123_data/res_estimations_exp3_ls00.csv')
df_pred_ls = [0]*3
df_pred_ls[0] = pd.read_csv('/Users/bezi/cognitive_analytics/ls00_exp123_data/res_predictions_exp1_ls00.csv')
df_pred_ls[1] = pd.read_csv('/Users/bezi/cognitive_analytics/ls00_exp123_data/res_predictions_exp2_ls00.csv')
df_pred_ls[2] = pd.read_csv('/Users/bezi/cognitive_analytics/ls00_exp123_data/res_predictions_exp3_ls00.csv')

# データ読み込み exp123
# 3 は実験の回数
df_est = [0]*3
df_est[0] = pd.read_csv('/Users/bezi/cognitive_analytics/exp123_data/res_estimations_exp1.csv')
df_est[1] = pd.read_csv('/Users/bezi/cognitive_analytics/exp123_data/res_estimations_exp2.csv')
df_est[2] = pd.read_csv('/Users/bezi/cognitive_analytics/exp123_data/res_estimations_exp3.csv')
df_pred = [0]*3
df_pred[0] = pd.read_csv('/Users/bezi/cognitive_analytics/exp123_data/res_predictions_exp1.csv')
df_pred[1] = pd.read_csv('/Users/bezi/cognitive_analytics/exp123_data/res_predictions_exp2.csv')
df_pred[2] = pd.read_csv('/Users/bezi/cognitive_analytics/exp123_data/res_predictions_exp3.csv')


# 刺激ごとグルーピングし平均値を算出
# estimate_mean : 実験ごと,刺激ごとの参加者の平均推定値
df_est_mean = []
for i in range(len(df_est_ls)):
    df_est_mean.append(df_est_ls[i].groupby('frequency').mean())
# print(df_est_mean)
estimate_mean = list(df_est_mean[0]['estimation'])+list(df_est_mean[1]['estimation'])+list(df_est_mean[2]['estimation'])
print(estimate_mean)

# 刺激ごとグルーピングし標準偏差を算出
# estimate_mean : 実験ごと,刺激ごとの参加者の推定値の標準偏差
df_est_std = []
for i in range(len(df_est)):
    df_est_std.append(df_est[i].groupby('frequency').std())
# print(df_est_std[0])
estimate_std = list(df_est_std[0]['estimation'])+list(df_est_std[1]['estimation'])+list(df_est_std[2]['estimation'])
# print(estimate_std)