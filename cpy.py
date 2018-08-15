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
import shutil
import argparse
import logging
from logging.config import dictConfig
import datetime
import json
from tqdm import tqdm
from organizer import organize_pairs
from const import RAWEXT
from todng import raw2dng
from pathlib import Path

try:
    input = raw_input
except NameError:
    pass

desc = """
RAW file copy utility.
"""

def copy_pairs_raw_only(s, d, o):

    if not os.path.exists(d):
        os.mkdir(d)

    for dir, _, files in os.walk(s):
        logger.info("Copying RAW files, %d to copy." % (len(files) - o))
        # for f in tqdm(files):
        for i in tqdm(range(o+1, len(files))):
            f = files[i]
            EXT = f.split('.')[-1].upper()
            if EXT in RAWEXT:
                shutil.copy(os.path.join(dir, f), os.path.join(d, f))

def del_raw_files(d):
    logger.debug(d)
    for dir, _, files in os.walk(d):
        for f in files:
            EXT = f.split('.')[-1].upper()
            if EXT in RAWEXT and EXT != "DNG":
                os.remove(os.path.join(d, f))

if __name__ == "__main__":
    with open("logging.json", 'r') as logging_configuration_file:
        config_dict = json.load(logging_configuration_file)
        # logname = os.path.join(os.getcwd(), "log", datetime.date.today().strftime("%B-%d-%Y") + ".log")
        # print (logname)
        # config_dict["handlers"]["filename"] = logname
        # print (config_dict)
        logging.config.dictConfig(config_dict)

    logger = logging.getLogger(__name__)
    # Parse args or take input
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--source', '-s', type=str, help='Full path of source folder.')
    parser.add_argument('--destination', '-d', type=str, help='Full path of destination folder.')
    parser.add_argument('--name', '-n', type=str, help='Name of the shot, [3A]Batch###')
    parser.add_argument('--offset', '-o', type=int, default = 0, help='Number of FILES (Including JPGS) to Offset During Copy. Sorted by name.')
    args = parser.parse_args()
    try:
        s = args.source
    except:
        s = input("Input the source folder: ")

    try:
        d = args.destination
    except:
        d = input("Input the destination folder: ")

    try:
        n = args.name
    except:
        n = input("Name of the shot?")

    o = args.offset

    copy_pairs_raw_only(s, d, o)
    organize_pairs(d, n, False, False)
    raw2dng(os.path.join(d, "Noisy"))
    raw2dng(os.path.join(d, "Clean"))
    del_raw_files(os.path.join(d, "Noisy"))
    del_raw_files(os.path.join(d, "Clean"))
