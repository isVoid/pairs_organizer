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

import subprocess
import os
import logging
import threading
from sys import platform
from tqdm import tqdm
from const import RAWEXT, MAX_CONCURRENT_RENDER_THREAD

if platform == "linux" or platform == "linux2":
    raise NotImplementedError("dng converter is not available in Linux")
elif platform == "darwin":
    adobeDNGPathCMD = "/Applications/Adobe\ DNG\ Converter.app/Contents/MacOS/Adobe\ DNG\ Converter -c %s"
elif platform == "win32":
    adobeDNGPathCMD = "\"C:\\Program Files\\Adobe\\Adobe DNG Converter\\Adobe DNG Converter.exe\" -c %s"

logger = logging.getLogger(__name__)

def render_single(s, file):
    # logger.debug(adobeDNGPathCMD % file)
    tqdm.write(adobeDNGPathCMD % file)
    subprocess.call(adobeDNGPathCMD % file, shell=True)
    s.release()

def raw2dng(d):

    s = threading.Semaphore(MAX_CONCURRENT_RENDER_THREAD)
    threads = []
    for dir, _, files in os.walk(d):
        logger.info("Currently processing %s folder, %d file(s) to process." %
                    (d, len(files)))
        for f in tqdm(files):
            s.acquire()
            EXT = f.split('.')[-1].upper()
            if EXT in RAWEXT:
                t = threading.Thread(target=render_single, name="Rdr_"+f, args=(s, os.path.join(dir, f)))
                threads.append(t)
                t.start()

    for x in threads:
        x.join()
