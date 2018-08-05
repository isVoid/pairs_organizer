#!/usr/bin/python
# Copyright [2018] [Wang Yinghao]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import argparse
import logging
try:
    input = raw_input
except NameError:
    pass

desc = """
Utility to organize pairs in folder.
"""
logger = logging.getLogger(__name__)

def organize_pairs(d, n, dng, j):

    if not os.path.exists(os.path.join(d, "Clean")):
        os.mkdir(os.path.join(d, "Clean"))
    if not os.path.exists(os.path.join(d, "Noisy")):
        os.mkdir(os.path.join(d, "Noisy"))

    CleanCount = 0
    NoisyCount = 0

    flag = 1
    # flag == 1, first frame is noisy
    # flag == 0, first frame is clean
    # Check before run.
    # Generally first frame must be noisy, if not, think why.

    fs = []
    for f in os.listdir(d):
        ff = os.path.join(d, f)
        if not os.path.isdir(ff):
            fs.append(ff)
    fs = sorted(fs)

    for f in fs:
        logger.debug("  Organizing  " + f)
        ext = f.split(".")[-1].upper()
        if ext == "ARW" or ext == "JPG" or ext == 'DNG':
            if (CleanCount + NoisyCount) % 2 == flag:
                if not j:
                    if not dng:
                        os.rename(os.path.join(d, f), os.path.join(d, "Clean", str(CleanCount).zfill(5) + ".ARW"))
                    else:
                        os.rename(os.path.join(d, f), os.path.join(d, "Clean", str(CleanCount).zfill(5) + ".dng"))
                else:
                    os.rename(os.path.join(d, f), os.path.join(d, "Clean", str(CleanCount).zfill(5) + ".JPG"))
                CleanCount += 1
            else:
                if not j:
                    if not dng:
                        os.rename(os.path.join(d, f),os.path.join(d, "Noisy", str(NoisyCount).zfill(5) + ".ARW"))
                    else:
                        os.rename(os.path.join(d, f),os.path.join(d, "Noisy", str(NoisyCount).zfill(5) + ".dng"))
                else:
                    os.rename(os.path.join(d, f), os.path.join(d, "Noisy", str(CleanCount).zfill(5) + ".JPG"))
                NoisyCount += 1

    logger.info("Sorted %d Clean imgs and %d Noisy imgs" % (CleanCount, NoisyCount))

if __name__ == "__main__":

    d = input("The folder where the pairs locates, in full path: ")
    n = input("Name of the shot?")
    dng = input("Is this a DNG folder? y/n")
    if not dng == 'y':
        j = input("Is this a JPG folder? y/n: ")
        if j == "y":
            j = True
        else:
            j = False
    else:
        dng = True;
        j = False

    organize_pairs(d, n, dng, j)
