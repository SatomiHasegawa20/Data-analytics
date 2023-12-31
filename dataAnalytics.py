# -*- coding: utf-8 -*-
"""データ分析.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13OHunWWWz-w4WdfpB5YkY2VCGha2NvNM
"""

!pip install -q japanize-matplotlib

# Commented out IPython magic to ensure Python compatibility.
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import japanize_matplotlib

from scipy import stats

# グラフのスタイルの指定
plt.style.use('bmh')
# %matplotlib inline
# %precision 3

df = pd.read_csv('/content/exercise.csv')
df.head(5)

from google.colab import drive
drive.mount('/content/drive')

df.info()

df.describe()

#CV別の各変数の平均
df_cv_mean = df.groupby("conversion", as_index=False) .mean()
df_cv_mean

"""## 各変数に対するCV率とその他平均"""

#全体のCV率
df['conversion'].mean()

# recencyとCV率
df_recency_mean = df.groupby("recency", as_index=False) .mean()
df_recency_mean

# used_discountとCV率
df_used_discount_mean = df.groupby("used_discount", as_index=False) .mean()
df_used_discount_mean

# used_bogoとCV率
df_used_bogo_mean = df.groupby("used_bogo", as_index=False) .mean()
df_used_bogo_mean

#zip_codeとCV率
df_zip_code_mean = df.groupby("zip_code", as_index=False) .mean()
df_zip_code_mean

#is_referralとCV率
df_is_referral_mean = df.groupby("is_referral", as_index=False) .mean()
df_is_referral_mean

#channelとCV率
df_channel_mean = df.groupby("channel", as_index=False) .mean()
df_channel_mean

#offerとCV率
df_offer_mean = df.groupby("offer", as_index=False) .mean()
df_offer_mean

"""## 各変数に対するCV率の可視化"""

# recencyとCV率
cross_recency = pd.crosstab(df["recency"], df["conversion"], normalize="index")
cross_recency

# recencyとCV率
cross_recency.plot.bar(stacked=True, colormap='Paired')

# used_discountとCV率
cross_used_discount = pd.crosstab(df["used_discount"], df["conversion"], normalize="index")
cross_used_discount

# used_discountとCV率
cross_used_discount.plot.bar(stacked=True, colormap='Paired')

# used_bogoとCV率
cross_used_bogo = pd.crosstab(df["used_bogo"], df["conversion"], normalize="index")
cross_used_bogo

# used_bogoとCV率
cross_used_bogo.plot.bar(stacked=True, colormap='Paired')

# zip_codeとCV率
cross_zip_code = pd.crosstab(df["zip_code"], df["conversion"], normalize="index")
cross_zip_code

# zip_codeとCV率
cross_zip_code.plot.bar(stacked=True, colormap='Paired')

# is_referralとCV率
cross_is_referral = pd.crosstab(df["is_referral"], df["conversion"], normalize="index")
cross_is_referral

# is_referralとCV率
cross_is_referral.plot.bar(stacked=True, colormap='Paired')

# channelとCV率
cross_channel = pd.crosstab(df["channel"], df["conversion"], normalize="index")
cross_channel

# channelとCV率
cross_channel.plot.bar(stacked=True, colormap='Paired')

# offerとCV率
cross_offer = pd.crosstab(df["offer"], df["conversion"], normalize="index")
cross_offer

# offerとCV率
cross_offer.plot.bar(stacked=True, colormap='Paired')

"""## その他の変数"""

# used_discountとoffer
used_discount_offer = df.groupby(["used_discount", "offer"], as_index=False) .mean()
used_discount_offer

# used_bogoとoffer
used_bogo_offer = df.groupby(["used_bogo", "offer"], as_index=False) .mean()
used_bogo_offer

# used_bogoとoffer
used_bogo_offer = df.groupby(["used_bogo", "used_discount", "offer"], as_index=False) .mean()
used_bogo_offer

"""## ここまでの洞察
**全体のCV率=0.147**
- recency
  - 前回購入した日からの期間が短いほどCV率が高そう
- history
 - 過去の購入品の価値が高いほどCV率が高そう
- used_discount
  - 以前割引を使ったか否かはCVに関係がなさそう
- used_bogo
  - 以前BoGoを利用した人ほどCV率が高そう
- zip_code
  - 農村に住んでいる人の方が、都市や郊外に住んでいる人よりもCV率が高そう
- is_referral
  - リファラルで流入していない人の方がCV率が高そう
- channel
  - マルチチャネル、ウェブ、電話の順にCV率が高くなりそう（マルチチャネルとは？）
- offer
  - 割引のオファー、BoGoのオファーの順に受け取った人のCV率が高そう

## 平均値・関連性の検定
※有意水準 5%
"""

df_cv0 = df.query('conversion==0')
sns.pairplot(df_cv0)

df_cv1 = df.query('conversion==1')
sns.pairplot(df_cv1)

"""## [仮説1]前回購入した日からの期間が短いほどCV率が高そう"""

plt.hist(df['recency'], alpha=0.5);
plt.hist(df_cv0['recency'], alpha=0.5);
plt.hist(df_cv1['recency'], alpha=0.7);

# 購入後、2 ヶ月未満で CV した人と、 3 ヶ月以降でした人で差があるのではないか
dic1 = {1:0, 2:0,3:1,4:1,5:1,6:1,7:1,8:1,9:1,10:1,11:1,12:1}

cross_recency_conv = pd.crosstab(df.query('offer!="No Offer"')['recency'].map(dic1), df.query('offer!="No Offer"')['conversion'])
cross_recency_conv

cross_recency_conv[1][0] / (cross_recency_conv[1][0] + cross_recency_conv[0][0])

cross_recency_conv[1][1] / (cross_recency_conv[1][1] +cross_recency_conv[0][1])

"""帰無仮説：　前回購入した日からの2ヶ月以内顧客の方がCV率（CVの平均）が低い

対立仮説：　前回購入した日から2ヶ月以内の顧客の方がCV率（CVの平均）が高い

"""

chi2, p, dof, ef = stats.chi2_contingency(cross_recency_conv, correction=False)
p

"""**前回購入した日から2ヶ月以内の顧客の方がCV率（CVの平均）が高い**

## [仮説2]過去の購入品の価値が高いほどCV率が高そう
"""

# 分布を確認
plt.hist(df['history'], bins=200);
plt.hist(df_cv0['history'], bins=200);
plt.hist(df_cv1['history'], bins=200);

df_cv1['history'].value_counts(ascending=True)
# 29.99 が以上に多い = 平均値が引っ張られるため削除して考える

# 29.99 の値のものを削除
df_cv0_his = df_cv0[df_cv0['history']!=29.99]['history']
df_cv1_his = df_cv1[df_cv1['history']!=29.99]['history']
df_cv0_his.value_counts(ascending=True)

plt.hist(df_cv0_his, bins=200);
plt.hist(df_cv1_his, bins=200);

# 対数変換：データにゼロや負がなければ np.log(), あるなら np.log1p を使用する
# 外れ値を弾いてからならOK
plt.hist(df_cv0_his.apply(np.log), bins=100);
plt.hist(df_cv1_his.apply(np.log), bins=100);

# バートレット検定 → 棄却できない（等分散を仮定）
stats.bartlett(df_cv0_his.apply(np.log), df_cv1_his.apply(np.log))

"""帰無仮説：　過去の購入品の価値が高いほどCV率が低い

対立仮説：　過去の購入品の価値が高いほどCV率が高い

"""

# t 検定
stats.ttest_ind(df_cv0_his.apply(np.log), df_cv1_his.apply(np.log), equal_var=True)

3.9702101461691662e-59

"""**過去の購入品の価値が高いほどCV率が高い**

## [仮説3]以前割引を使ったか否かはCVに関係がなさそう
"""

cross_used_discount_noindex = pd.crosstab(df['used_discount'], df['conversion'])
cross_used_discount_noindex

"""帰無仮説：　used_discountとconversionは関係がない

対立仮説：　used_discountとconversionは関係がある
"""

chi2, p, dof, ef = stats.chi2_contingency(cross_used_discount_noindex, correction=False)
p

"""**以前割引を使ったか否かはCVに関係があるとは言えない**

## [仮説4]以前BoGoを利用した人ほどCV率が高そう
"""

cross_used_bogo_noindex = pd.crosstab(df['used_bogo'], df['conversion'])
cross_used_bogo_noindex

"""帰無仮説：　used_bogoとconversionは関係がない

対立仮説：　used_bogoとconversionは関係がある
"""

chi2, p, dof, ef = stats.chi2_contingency(cross_used_bogo_noindex, correction=False)
p

"""**過去のBoGoの利用とCVは関係がある**

## [仮説5]農村に住んでいる人の方が、都市や郊外に住んでいる人よりもCV率が高そう
"""

plt.hist(df['zip_code'], alpha=0.5);
plt.hist(df_cv0['zip_code'], alpha=0.5);
plt.hist(df_cv1['zip_code'], alpha=0.7);

# 「農村」と「都市or郊外」でのCVの違いがあるのでは
# 「農村」→1, 「都市or郊外」→0
dic2 = {'Surburban':0, 'Urban':0, 'Rural':1}

cross_zip_code_cv_2 = pd.crosstab(df['zip_code'].map(dic2), df['conversion'])
cross_zip_code_cv_2

cross_zip_code_cv_per = pd.crosstab(df['zip_code'].map(dic2), df['conversion'], normalize='index')
cross_zip_code_cv_per

"""帰無仮説：　農村に住んでいる人の方が、都市や郊外に住んでいる人よりもCV率が高くない

対立仮説：　農村に住んでいる人の方が、都市や郊外に住んでいる人よりもCV率が高い
"""

chi2, p, dof, ef = stats.chi2_contingency(cross_zip_code_cv_2, correction=False)
p

"""**農村に住んでいる人の方が、都市や郊外に住んでいる人よりもCV率が高い**

## [仮説6]リファラルで流入していない人の方がCV率が高そう
"""

cross_is_referral_noindex = pd.crosstab(df['is_referral'], df['conversion'])
cross_is_referral_noindex

"""帰無仮説：　リファラルで流入していない人の方がCV率が高くない

対立仮説：　リファラルで流入していない人の方がCV率が高い
"""

chi2, p, dof, ef = stats.chi2_contingency(cross_is_referral_noindex, correction=False)
p

"""**リファラルで流入していない人の方がCV率が高い（リファラルはあまり意味がない？）**

## [仮説7]Webの方が電話よりCVに繋がりそう（今回マルチチャネルは省く）
"""

plt.hist(df['channel'], alpha=0.5);
plt.hist(df_cv0['channel'], alpha=0.5);
plt.hist(df_cv1['channel'], alpha=0.7);

# 電話とWebのCVの違いがあるのでは
# 電話→1, Web→0
dic3 = {'Phone':1, 'Web':0}

cross_channel_cv_2 = pd.crosstab(df.query('channel!="Multichannel"')['channel'].map(dic3), df.query('channel!="Multichannel"')['conversion'])
cross_channel_cv_2

dic3 = {'Phone':1, 'Web':0, 'Multichannel':1}

cross_channel_cv_2_per = pd.crosstab(df.query('channel!="Multichannel"')['channel'].map(dic3), df.query('channel!="Multichannel"')['conversion'], normalize='index')
cross_channel_cv_2_per

"""帰無仮説： Webの方が電話よりCVに繋がるわけではない（今回マルチチャネルは省く）

対立仮説：　Webの方が電話よりCVに繋がる（今回マルチチャネルは省く）
"""

chi2, p, dof, ef = stats.chi2_contingency(cross_channel_cv_2, correction=False)
p

"""**Webの方が電話よりCVに繋がる（今回マルチチャネルは省く）**

## [仮説8-1]オファーを出した方がCVに繋がる
"""

plt.hist(df['offer'], alpha=0.5);
plt.hist(df_cv0['offer'], alpha=0.5);
plt.hist(df_cv1['offer'], alpha=0.7);

# オファーありとなしではCVに違いがあるのでは
# 「Bogo or Discountのオファーあり」→0, 「No Offer」→1
dic4 = {'Buy One Get One':0, 'Discount':0,  'No Offer':1}

cross_offer_cv_2 = pd.crosstab(df['offer'].map(dic4), df['conversion'])
cross_offer_cv_2

cross_offer_cv_2_per = pd.crosstab(df['offer'].map(dic4), df['conversion'], normalize='index')
cross_offer_cv_2_per

"""
帰無仮説：　オファーを出した方がCV率が高くない

対立仮説：　オファーを出した方がCV率が高い"""

chi2, p, dof, ef = stats.chi2_contingency(cross_offer_cv_2, correction=False)
p

"""**オファーを出した方がCV率が高い**

## [仮説8-2]offerはdiscountの方がBoGoよりCV率が高い
"""

# offerの種類でCVの違いが出るのでは
# Bogo→0, Discount→1
dic5 = {'Buy One Get One':0, 'Discount':1}

cross_offer_cv_3 = pd.crosstab(df.query('offer!="No Offer"')['offer'].map(dic5), df.query('offer!="No Offer"')['conversion'])
cross_offer_cv_3

cross_offer_cv_3_per = pd.crosstab(df.query('offer!="No Offer"')['offer'].map(dic5), df.query('offer!="No Offer"')['conversion'], normalize='index')
cross_offer_cv_3_per

"""帰無仮説： offerはdiscountの方がBoGoよりCVに繋がるわけではない

対立仮説：　offerはdiscountの方がBoGoよりCVに繋がる
"""

chi2, p, dof, ef = stats.chi2_contingency(cross_offer_cv_3, correction=False)
p

"""**offerはdiscountの方がBoGoよりCVに繋がる**

## ここまでのまとめ
- 前回購入した日から2ヶ月以内の顧客の方がCV率（CVの平均）が高い
- 過去の購入品の価値が高いほどCV率が高い
- 以前discountを使ったか否かはCVに関係があるとは言えない
- 過去のBoGoの利用とCVは関係がある
- 農村に住んでいる人の方が、都市や郊外に住んでいる人よりもCV率が高い
- リファラルで流入していない人の方がCV率が高い（→リファラルはあまり意味がない？）
- Webの方が電話よりCVに繋がる（今回マルチチャネルは省く）
-オファーを出した方がCV率が高い
- offerはdiscountの方がBoGoよりCVに繋がる

## さらに他の変数同士の関係を調べる
"""

# discount使った顧客を抽出
df_used_discount = df[df["used_discount"] == 1]
df_used_discount.head()

# discount使った顧客のofferに対するCV
cross_dis_offer_cv = pd.crosstab(df_used_discount["offer"], df_used_discount["conversion"], normalize="index")
cross_dis_offer_cv

cross_dis_offer_cv.plot.bar(stacked=True, colormap='Paired')

# bogo使った顧客を抽出
df_used_bogo = df[df["used_bogo"] == 1]
df_used_bogo.head()

# bogo使った顧客のofferに対するCV
cross_bogo_offer_cv = pd.crosstab(df_used_bogo["offer"], df_used_bogo["conversion"], normalize="index")
cross_bogo_offer_cv

cross_bogo_offer_cv.plot.bar(stacked=True, colormap='Paired')

# 郊外に住んでいる顧客を抽出
df_zip_sur = df[df["zip_code"] == "Surburban"]
df_zip_sur.head()

# 郊外に住んでいる顧客のchannel別のCV
cross_zip_sur_channel_cv = pd.crosstab(df_zip_sur.query('channel!="Multichannel"')["channel"], df_zip_sur.query('channel!="Multichannel"')["conversion"], normalize="index")
cross_zip_sur_channel_cv

cross_zip_sur_channel_cv.plot.bar(stacked=True, colormap='Paired')

# 都市に住んでいる顧客を抽出
df_zip_urban = df[df["zip_code"] == "Urban"]
df_zip_urban.head()

# 都市に住んでいる顧客のchannel別のCV
cross_zip_urb_channel_cv = pd.crosstab(df_zip_urban.query('channel!="Multichannel"')["channel"], df_zip_urban.query('channel!="Multichannel"')["conversion"], normalize="index")
cross_zip_urb_channel_cv

cross_zip_urb_channel_cv.plot.bar(stacked=True, colormap='Paired')

# 農村に住んでいる顧客を抽出
df_zip_rural = df[df["zip_code"] == "Rural"]
df_zip_rural.head()

# 都市に住んでいる顧客のchannel別のCV
cross_zip_rural_channel_cv = pd.crosstab(df_zip_rural.query('channel!="Multichannel"')["channel"], df_zip_rural.query('channel!="Multichannel"')["conversion"], normalize="index")
cross_zip_rural_channel_cv

cross_zip_rural_channel_cv.plot.bar(stacked=True, colormap='Paired')

# 電話で購入した顧客を抽出
df_channel_phone = df[df["channel"] == "Phone"]
df_channel_phone.head()

# 電話で購入した顧客のdiscountの使用別のCV
cross_chan_phone_dis_cv = pd.crosstab(df_channel_phone["used_discount"], df_channel_phone["conversion"], normalize="index")
cross_chan_phone_dis_cv

cross_chan_phone_dis_cv.plot.bar(stacked=True, colormap='Paired')

# 電話で購入した顧客のbogoの使用別のCV
cross_chan_phone_bogo_cv = pd.crosstab(df_channel_phone["used_bogo"], df_channel_phone["conversion"], normalize="index")
cross_chan_phone_bogo_cv

cross_chan_phone_bogo_cv.plot.bar(stacked=True, colormap='Paired')

#recencyとhistory
df_recency_history = df.groupby("recency").mean()
df_recency_history

#recencyとhistory
df_recency_history_mean = df.groupby("recency").mean()
df_recency_history_mean

df_rec_dis = df[(df["recency"] <= 2)]
df_rec_dis.head()

df_rec_dis.describe()

df_rec_dis2 = df[(df["recency"] >= 3) ]
df_rec_dis2.head()

df_rec_dis2.describe()

"""## ここまでの洞察2
- 以前にdiscountを使った顧客はofferを受け取ったらCVする確率が高そう
- 以前にdiscountを使った顧客はdiscountのofferを受け取った方がBoGoのofferを受け取るよりCVに繋がりそう
- 以前にBoGoを使った顧客はofferを受け取ったらCVする確率が高そう
- 以前にBoGoを使った顧客はdiscountのofferでもBoGoのofferでもどちらのofferを受け取ったかはCVに関係なさそう
- 郊外に住んでいる顧客はWebで購入する方がCVに繋がりそう
- 都市に住んでいる顧客はWebで購入する方がCVに繋がりそう
- 農村に住んでいる顧客はWebで購入する方がCVに繋がりそう
- 電話で購入した顧客のused_discountの有無はCVに関係なさそう
- 電話で購入した顧客はBoGoを過去に利用した顧客の方がCVに繋がりそう


→→住んでる場所によってchannelの利用比率は変わらなそう
- 前回購入から月数が経っていないほど購入品の過去の価値も高そう
- 前回購入から2ヶ月以内の顧客の方が購入品の価値が高そう

## 平均値・関連性の検定2

## [仮説9]以前discountを使った顧客はdiscountのofferを受け取ったらCVする確率が高そう
"""

# Bogo→0, Discount→1
dic6 = {'Buy One Get One':0, 'Discount':1}

cross_offer_cv_５ = pd.crosstab(df_used_discount.query('offer!="No Offer"')['offer'].map(dic6), df_used_discount.query('offer!="No Offer"')['conversion'])
cross_offer_cv_5

cross_offer_cv_5_per = pd.crosstab(df_used_discount.query('offer!="No Offer"')['offer'].map(dic6), df_used_discount.query('offer!="No Offer"')['conversion'], normalize='index')
cross_offer_cv_5_per

chi2, p, dof, ef = stats.chi2_contingency(cross_offer_cv_5, correction=False)
p

"""**以前discountを使った顧客はdiscountのofferを受け取ったらCVする確率が高い**

## [仮説10]前回購入から2ヶ月以内の顧客の方が購入品の価値の平均が高そう
"""

df_rec2 = df.query('recency<=2')

df_rec3 = df.query('recency>=3')

#差を確認
print(df_rec2['history'].mean())
print(df_rec3['history'].mean())

# 分布を確認
plt.hist(df['history'], bins=200);
plt.hist(df_rec2['history'], bins=200);
plt.hist(df_rec3['history'], bins=200);

df_rec2['history'].value_counts(ascending=True)
# 29.99 が以上に多い = 平均値が引っ張られるため削除して考える

# 29.99 の値のものを削除
df_rec2_his = df_rec2[df_rec2['history']!=29.99]['history']
df_rec3_his = df_rec3[df_rec3['history']!=29.99]['history']
df_rec2_his.value_counts(ascending=True)

plt.hist(df_rec2_his.apply(np.log), bins=100);
plt.hist(df_rec3_his.apply(np.log), bins=100);

# バートレット検定
stats.bartlett(df_rec2_his.apply(np.log), df_rec3_his.apply(np.log))

# t 検定
stats.ttest_ind(df_rec2_his.apply(np.log), df_rec3_his.apply(np.log), equal_var=True)

"""**前回購入から2ヶ月以内の顧客の方が購入品の価値の平均が高い**

## ここまでのまとめ2
- 以前discountを使った顧客はdiscountのofferを受け取ったらCVする確率が高い
- 前回購入から2ヶ月以内の顧客の方が購入品の価値の平均が高い

## その他計算
"""

df_zip_mean = df.groupby("zip_code", as_index="False").mean()
df_zip_mean

#recencyとhistory
df_recency_history_sum = df.groupby("recency").sum()
df_recency_history_sum

#recencyとhistory
df_recency_history_mean = df.groupby("recency").mean()
df_recency_history_mean

df_rec_dis = df[(df["recency"] == 1) | (df["recency"] == 2) ]
df_rec_dis.head()

df_rec_dis.describe()

df_rec_dis2 = df[(df["recency"] >= 3) ]
df_rec_dis2.head()

df_rec_dis2.describe()

df_rec_num = df["recency"].value_counts()
df_rec_num

df.describe()

# recency=1 or 2 かつ used_discount =1
# 電話で購入した顧客を抽出
df_rec_dis = df[(df["recency"] == 1) | (df["recency"] == 2) ]
df_rec_dis.head()

df_rec_dis_count = df_rec_dis["used_bogo"].value_counts()
df_rec_dis_count

df.describe()

(9366/64000)*100

df_test = df.drop('recency', axis=1)
df_test['recency'] = df['recency'].map(dic1)
df_test.head()

len(df_test.query('recency==0 & channel=="Web" & offer=="Discount" & conversion==1')) / len(df)

len(df)*0.009

df_cv1['history'].median()*len(df)*0.009

116616.960*113

import plotly.graph_objects as go

dep = pd.DataFrame({
    "label":["該当する顧客", "その他"],
    "value":[576, 63424]
})

fig = go.Figure(data=[go.Pie(labels=dep["label"],
                             values=dep["value"],
                             hole=0.5)])


fig.update_layout(annotations=[{
    "text":"全顧客データ",
    "x":0.5,
    "y":0.5,
    "font_size":20,
    "showarrow":False
    }])
fig.show()

