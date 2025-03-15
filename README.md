# Non-Parallel Voice Conversion with CycleVAE modified by Lemon_tea014


----
## 概要
* https://github.com/patrickltobing/cyclevae-vc を実行可能に修正, 改良したものになります.
* このソースコードのLICENCEは, [apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) に従います.
* [MWDLPニューラルボコーダ統合版](https://github.com/patrickltobing/cyclevae-vc-neuralvoco)
  
I would like to express my gratitude to the developer, P.L. Tobing.
Thanks!

----
## Requirements:
- Ubuntu >= 18.04
- python -dev >= 3.7-dev
- CUDA 11.1
- virtualenv

## 改良点
1. run.shに追加学習用実行コードを追加
2. 学習データの全体統計計算に, 話者ごとに統計を計算し, 入力に合わせて動的に正規化フィルタを変更できるように改良
3. 損失を可視化できるように[paper](https://arxiv.org/pdf/1907.10185)に基づくグラフ描画スクリプトを追加（Tonsorboardへの置き換えを要検討）
4. 1epochの対象を全発話になるよう, generatorを変更
5. スペクトル包絡に, GVポストフィルタとは別にmerlinのフォルマント強調ポストフィルタを導入
6. logの出力方法, ライブラリのバージョン等軽微な修正

## 使い方
    $cd tools
    $make
    $cd ../egs/one-to-one

run.sh を開く

*実行するレシピをstageで設定する.*

    $bash run.sh

*話者のハイパーパラメータ設定は, stage=1 を実行してからstage=a を実行し, 適宜変更してから, またstage=1 を実行してください*

*f0 と 波形パワーの統計ヒストグラムは, exp/init\_spk\_stat へ保存されます*

stage=4 で, モデルの訓練を行います.

    $bash run.sh


----
## レシピについて
STAGE 0: データディレクトリの作成

STAGE 1: 特徴量抽出

STAGE a: WORLDのf0推定に用いるf0閾値, 波形パワー閾値のための統計を計算 （これらの情報はconf/ へ保存されます）

STAGE 2: 正則化フィルタのための特徴量統計を計算

STAGE 3: 励起特徴量の線形変換を行う

STAGE 4: モデルの訓練を行う

STAGE 5: 変換特徴量からGV（Global Variance）を計算

STAGE 6: WORLD Vocoderを使って波形を生成


----
## Contact

irodorilemon226@gmail.com 

----
## Reference
P. L. Tobing, Y.-C. Wu, T. Hayashi, K. Kobayashi, and T. Toda, “Non-parallel voice conversion with cyclic
variational autoencoder”, CoRR arXiv preprint arXiv: 1907.10185, 2019. (Accepted for INTERSPEECH 2019)

