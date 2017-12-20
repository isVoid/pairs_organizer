#!/usr/bin/python

import os

d = raw_input("The folder where the pairs locates, in full path: ")
n = raw_input("Name of the shot? ")
j = raw_input("Is this a JPG folder? y/n: ")

if not j == "y" and not j == "n":
    raise ValueError("Unrecognized input j: %s" % j)
elif j == "y":
    j = True
elif j == "n":
    j = False

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
    print (f)
    if (CleanCount + NoisyCount) % 2 == flag:
        if not j:
            os.rename(os.path.join(d, f), os.path.join(d, "Clean", "%s_c_" % n + str(CleanCount).zfill(5) + ".ARW"))
        else:
            os.rename(os.path.join(d, f), os.path.join(d, "Clean", "%s_c_" % n + str(CleanCount).zfill(5) + ".JPG"))
        CleanCount += 1
    else:
        if not j:
            os.rename(os.path.join(d, f),os.path.join(d, "Noisy", "%s_n_" % n + str(NoisyCount).zfill(5) + ".ARW"))
        else:
            os.rename(os.path.join(d, f), os.path.join(d, "Noisy", "%s_n_" % n + str(CleanCount).zfill(5) + ".JPG"))
        NoisyCount += 1
