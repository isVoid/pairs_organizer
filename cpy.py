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

try:
    input = raw_input
except NameError:
    pass

desc = """
RAW file copy utility.
"""
RAWEXT = ['ARW', 'CR2', 'NEF', 'DNG']

def copy_pairs_raw_only(s, d):
    for dir, _, files in os.walk(s):
        for f in files:
            EXT = f.split('.')[-1].to_upper()
            if EXT in RAWEXT:
                shutil.copy(os.path.join(dir, f), os.path.join(d, f))

if __name__ == "__main__":
    # Parse args or take input
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--source', '-s', help='Full path of source folder.')
    parser.add_argument('--destination', '-d', help='Full path of destination folder.')

    args = parser.parse_args()
    try:
        s = args.source
    except:
        s = input("Input the source folder: ")

    try:
        d = args.destination
    except:
        d = input("Input the destination folder: ")

    copy_pairs_raw_only(s, d)

    
