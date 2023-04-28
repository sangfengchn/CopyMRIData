'''
 # @ Author: feng
 # @ Create Time: 2023-04-28 12:10:40
 # @ Modified by: feng
 # @ Modified time: 2023-04-28 12:22:01
 # @ Description: Rename file and folder by MRINumber.
 '''

import os
from os.path import join as opj
from glob import glob
import shutil
import re
import pandas as pd
import logging
logging.basicConfig(level=logging.INFO)

def func_replace(path, oldId, newId):
    with open(path, "r") as f:
        lines = f.readlines()
    newLines = []
    for line in lines:
        newLines.append(line.replace(oldId, newId))
    with open(path, "w") as f:
        f.writelines(newLines)

def func_rename(path, oldId, newId):
    exts = [".txt", ".html", ".json", ".gii", ".toml"]
    for pPath, dPaths, fPaths in os.walk(path):
        # if dPath is a empty folder.
        for dPath in dPaths:
            if len(os.listdir(opj(pPath, dPath))) == 0: shutil.rmtree(opj(pPath, dPath))
            
        for fPath in fPaths:
            tmpSrcPath = opj(pPath, fPath)
            logging.info(tmpSrcPath)
            if os.path.splitext(tmpSrcPath)[-1] in exts:
                func_replace(tmpSrcPath, oldId, newId)
            tmpDstPath = tmpSrcPath.replace(oldId, newId)
            os.renames(tmpSrcPath, tmpDstPath)

df = pd.read_csv("sourcedata/participants.csv", header=0, index_col=3)
df = df.loc[df.Site == "BNUOLD"]
# logging.info(df.head())
src = "toLIUCHEN/freesurfer"

for i in glob(opj(src, "sub-*")):
    subParId = os.path.split(i)[-1]
    subMriId = df.loc[subParId, "OLDID"]
    subMriId = f"sub-{subMriId}"
    func_rename(i, subParId, subMriId)
logging.info("Done.")