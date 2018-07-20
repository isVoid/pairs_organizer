#!/usr/bin/python

import os

try:
    input = raw_input
except NameError:
    pass

d = input("The folder where the pairs locates, in full path: ")
n = input("Name of the shot? ")
dng = input("Is this a DNG folder? y/n")
if not dng == 'y':
    j = input("Is this a JPG folder? y/n: ")
    if not j == "y" and not j == "n":
        raise ValueError("Unrecognized input j: %s" % j)
    elif j == "y":
        j = True
    elif j == "n":
        j = False
else:
    dng = True;
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
    ext = f.split(".")[-1].upper()
    if ext == "ARW" or ext == "JPG" or ext == 'DNG':
        if (CleanCount + NoisyCount) % 2 == flag:
            if not j:
                if not dng:
                    os.rename(os.path.join(d, f), os.path.join(d, "Clean", "%s_c_" % n + str(CleanCount).zfill(5) + ".ARW"))
                else:
                    os.rename(os.path.join(d, f), os.path.join(d, "Clean", "%s_c_" % n + str(CleanCount).zfill(5) + ".dng"))
            else:
                os.rename(os.path.join(d, f), os.path.join(d, "Clean", "%s_c_" % n + str(CleanCount).zfill(5) + ".JPG"))
            CleanCount += 1
        else:
            if not j:
                if not dng:
                    os.rename(os.path.join(d, f),os.path.join(d, "Noisy", "%s_n_" % n + str(NoisyCount).zfill(5) + ".ARW"))
                else:
                    os.rename(os.path.join(d, f),os.path.join(d, "Noisy", "%s_n_" % n + str(NoisyCount).zfill(5) + ".dng"))
            else:
                os.rename(os.path.join(d, f), os.path.join(d, "Noisy", "%s_n_" % n + str(CleanCount).zfill(5) + ".JPG"))
            NoisyCount += 1

print ("%d Clean imgs and %d Noisy imgs" % (CleanCount, NoisyCount))
