'''
 # @ Author: feng
 # @ Create Time: 2023-04-28 11:36:47
 # @ Modified by: feng
 # @ Modified time: 2023-04-28 11:37:56
 # @ Description: Copy postprocessed images.
 '''

import os
from os.path import join as opj
import pandas as pd
import shutil
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

rawDf = pd.read_csv("sourcedata/participants.csv", header=0)
rawDf = rawDf.loc[rawDf.Site == "BNUOLD"]
logging.info(rawDf.head())

df = pd.read_csv("all_beh_686.csv", header=0)
df["OLDID"] = [f"BNU{i}" for i in df.MRINumber]
logging.info(df.head())

der = "derivatives/fmriprep"
dst = "toLIZIlin/fmriprep"
if not os.path.exists(dst): os.makedirs(dst)

resDf = pd.merge(rawDf, df, how="right", on=["OLDID"])
resDf = resDf.dropna()
logging.info(len(resDf))
logging.info(resDf)

for i in resDf.index.values:
    logging.info(i)
    tmpNewId = resDf.loc[i, "participant_id"]
    tmpSrcPath = opj(der, tmpNewId)
    if not os.path.exists(tmpSrcPath): continue
    tmpDstPath = opj(dst, tmpNewId)
    shutil.copytree(tmpSrcPath, tmpDstPath)
    
logging.info("Done.")