#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2019 Patrick Lumban Tobing (Nagoya University)
# based on PyTorch implementation for WaveNet vocoder by Tomoki Hayashi (Nagoya University)
#  Apache 2.0  (http://www.apache.org/licenses/LICENSE-2.0)

from __future__ import print_function

import argparse
import logging

import numpy as np
from sklearn.preprocessing import StandardScaler

from utils import check_hdf5
from utils import read_hdf5
from utils import read_txt
from utils import write_hdf5
from distutils.util import strtobool


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--feats", default=None, required=True,
        help="name of the list of hdf5 files")
    #--feats_extendは、ファインチューニングなどでデータセットを拡張する用のコマンド
    parser.add_argument(
        "--feats_extend", default=None,
        help="name of the list of hdf5 files")
    parser.add_argument(
        "--stats", default=None, required=True,
        help="filename of hdf5 format")
    parser.add_argument("--dtw", default=False,
        type=strtobool, help="flag for computing stats of dtw-ed feature")
    parser.add_argument("--expdir", required=True,
        type=str, help="directory to save the log")
    parser.add_argument("--spkr", default=None,
        type=str, help="directory to save the log")
    parser.add_argument(
        "--verbose", default=1,
        type=int, help="log message level")

    args = parser.parse_args()

    # set log level
    if args.verbose == 1:
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s (%(module)s:%(lineno)d) %(levelname)s: %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S',
                            filename=args.expdir + "/calc_stats.log")
        logging.getLogger().addHandler(logging.StreamHandler())
    elif args.verbose > 1:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s (%(module)s:%(lineno)d) %(levelname)s: %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S',
                            filename=args.expdir + "/calc_stats.log")
        logging.getLogger().addHandler(logging.StreamHandler())
    else:
        logging.basicConfig(level=logging.WARN,
                            format='%(asctime)s (%(module)s:%(lineno)d) %(levelname)s: %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S',
                            filename=args.expdir + "/calc_stats.log")
        logging.getLogger().addHandler(logging.StreamHandler())
        logging.warn("logging is disabled.")

    # read list and define scaler
    #scpファイルの読み込み
    filenames = read_txt(args.feats)
    
    scaler_feat_org_lf0 = StandardScaler()
    #scaler_sdfeat_org_lf0 = StandardScaler()
    #scaler_sdmcep = StandardScaler()
    
    #print("number of training utterances =", len(filenames))
    logging.info(f"訓練データの発話数 ={len(filenames)}")
    if args.feats_extend is not None:
        filenames_extend = read_txt(args.feats_extend)
        logging.info(f"訓練データの発話数 ={len(filenames_extend)}")

    #var = []
    var_range = []
    #f0s_range = [] だけど、nupmy配列ではこのような初期化ができないので、下記のように書く。
    f0s_range = np.empty((0))
    
    # process over all of data
    for filename in filenames:
        logging.info(filename)
        feat_org_lf0 = read_hdf5(filename, "/feat_org_lf0")
        #feat_org_lf0の列ごとの平均、標準偏差を計算する。
        scaler_feat_org_lf0.partial_fit(feat_org_lf0)
        
        #sdfeat_org_lf0 = read_hdf5(filename, "/sdfeat_org_lf0")
        #scaler_sdfeat_org_lf0.partial_fit(sdfeat_org_lf0)
        #sdmcep = read_hdf5(filename, "/sdmcep_range")
        #scaler_sdmcep.partial_fit(sdmcep)
        
        if (args.spkr is None) or (args.spkr is not None and args.spkr in filename):
            mcep_range = read_hdf5(filename, "/mcep_range")
            
            #mcep_rangeの分散を計算
            var_range.append(np.var(mcep_range, axis=0))
            #logging.info(mcep_range.shape)
            logging.info(f"mcep_rangeの行列サイズ ={mcep_range.shape}")
            logging.info(f"var_rangeの行列サイズ ={len(var_range)}")
            
            f0_range = read_hdf5(filename, "/f0_range")
            logging.info(f"f0_rangeの要素数 ={f0_range.shape}")
            #非ゼロ要素の列番号を抽出
            nonzero_indices = np.nonzero(f0_range)
            #非ゼロのf0実数値をf0_range[nonzero_indices]で抽出し、それらの配列サイズを返す
            #logging.info(f0_range[nonzero_indices].shape)
            logging.info(f"f0_rangeの非ゼロf0の要素数 ={f0_range[nonzero_indices].shape}")
            
            #logging.info(f0s_range.shape)
            logging.info(f"f0s_rangeの要素数 ={f0s_range.shape}")
            
            f0s_range = np.concatenate([f0s_range,f0_range[nonzero_indices]])
            logging.info(f"f0s_rangeを、{f0_range[nonzero_indices].shape}と行方向に結合 = {f0s_range.shape}")
            #logging.info(f0s_range.shape)
            
            #データセットのファインチューニング、拡張用の処理
    if args.feats_extend is not None:
        for filename in filenames_extend:
            logging.info(filename)
            feat_org_lf0 = read_hdf5(filename, "/feat_org_lf0")
            scaler_feat_org_lf0.partial_fit(feat_org_lf0)
            if (args.spkr is None) or (args.spkr is not None and args.spkr in filename):
                mcep_range = read_hdf5(filename, "/mcep_range")
                var_range.append(np.var(mcep_range, axis=0))
                logging.info(mcep_range.shape)
                f0_range = read_hdf5(filename, "/f0_range")
                nonzero_indices = np.nonzero(f0_range)
                logging.info(f0_range[nonzero_indices].shape)
                logging.info(f0s_range.shape)
                f0s_range = np.concatenate([f0s_range,f0_range[nonzero_indices]])
                logging.info(f0s_range.shape)
    #特徴量全体の平均、分散（この後、各次元ごとにStandardScaler.transform()で正規化されるはず)
    mean_feat_org_lf0 = scaler_feat_org_lf0.mean_
    scale_feat_org_lf0 = scaler_feat_org_lf0.scale_
    #mean_sdfeat_org_lf0 = scaler_sdfeat_org_lf0.mean_
    #scale_sdfeat_org_lf0 = scaler_sdfeat_org_lf0.scale_
    #mean_sdmcep = scaler_sdmcep.mean_
    #scale_sdmcep = scaler_sdmcep.scale_
    #発話すべてのmcepの分散値(おそらく、1×50 が発話数個)が並べられたvar_rangeを、次元ごとに平均する。
    gv_range_mean = np.mean(np.array(var_range), axis=0)
    gv_range_var = np.var(np.array(var_range), axis=0)
    
    logging.info(f"mcepの分散要素：{np.array(var_range).shape}")
    logging.info(f"mcepの分散の平均値(GV)：{gv_range_mean.shape}")
    logging.info(f"mcepの分散の平均値(GV)：{gv_range_mean}")
    #logging.info(gv_range_mean)
    logging.info(f"mcepの分散の分散(GV)：{gv_range_var.shape}")
    logging.info(f"mcepの分散の分散(GV)：{gv_range_var}")
    #logging.info(gv_range_var)
    
    f0_range_mean = np.mean(f0s_range)
    f0_range_std = np.std(f0s_range)
    logging.info(f"f0_rangeの平均：{f0_range_mean}")
    logging.info(f"f0_rangeの標準偏差：{f0_range_std}")
    #logging.info(f0_range_mean)
    #logging.info(f0_range_std)
    lf0_range_mean = np.mean(np.log(f0s_range))
    lf0_range_std = np.std(np.log(f0s_range))
    logging.info(f"対数f0_rangeの平均：{lf0_range_mean}")
    logging.info(f"対数f0_rangeの標準偏差：{lf0_range_std}")
    # logging.info(lf0_range_mean)
    # logging.info(lf0_range_std)
    
    #logging.info(np.array_equal(f0_range_mean,np.exp(lf0_range_mean)))
    logging.info(f"対数f0_rangeの平均と、f0_rangeの平均は同一か：{np.array_equal(f0_range_mean,np.exp(lf0_range_mean))}")
    #logging.info(np.allclose(f0_range_std,np.exp(lf0_range_std)))
    logging.info(f"対数f0_rangeのstdと、f0_rangeのstdは同一か：{np.array_equal(f0_range_std,np.exp(lf0_range_std))}")
    
    logging.info(f"音響特徴量の平均要素：{np.array(mean_feat_org_lf0).shape}")
    logging.info(f"音響特徴量の平均：{mean_feat_org_lf0}")
    #logging.info(mean_feat_org_lf0)
    logging.info(f"音響特徴量の標準偏差要素(GV)：{np.array(scale_feat_org_lf0).shape}")
    logging.info(f"音響特徴量の標準偏差（GV)：{scale_feat_org_lf0}")
    #logging.info(scale_feat_org_lf0)
    
    write_hdf5(args.stats, "/mean_feat_org_lf0", mean_feat_org_lf0)
    write_hdf5(args.stats, "/scale_feat_org_lf0", scale_feat_org_lf0)
    #write_hdf5(args.stats, "/mean_sdfeat_org_lf0", mean_sdfeat_org_lf0)
    #write_hdf5(args.stats, "/scale_sdfeat_org_lf0", scale_sdfeat_org_lf0)
    #write_hdf5(args.stats, "/mean_sdmcep_range", mean_sdmcep)
    #write_hdf5(args.stats, "/scale_sdmcep_range", scale_sdmcep)
    write_hdf5(args.stats, "/gv_range_mean", gv_range_mean)
    write_hdf5(args.stats, "/gv_range_var", gv_range_var)
    write_hdf5(args.stats, "/f0_range_mean", f0_range_mean)
    write_hdf5(args.stats, "/f0_range_std", f0_range_std)
    write_hdf5(args.stats, "/lf0_range_mean", lf0_range_mean)
    write_hdf5(args.stats, "/lf0_range_std", lf0_range_std)


if __name__ == "__main__":
    main()
