import os
import shutil

try:
    input = raw_input
except NameError:
    pass

def uniform_meta(f):
    xmp_path = ""
    f_list = []

    for root, dirs, files in os.walk(f):
        for f in files:
            if f.split(".")[-1].upper() == "ARW":
                f_list.append(os.path.join(root, f))
            if f.split(".")[-1].upper() == "XMP":
                a = input("Found XMP file %s, apply to all other frames? y/n " % f)
                a = True if a == "y" else False
                if a:
                    xmp_path = os.path.join(root, f)
                else:
                    quit("Aborted")

    if xmp_path == "":
        raise FileNotFoundError("XMP file not found. Aborting.")
    # print (f_list)
    # print (xmp_path)
    for f in f_list:
        dst = f.replace("ARW", "xmp")
        try:
            shutil.copyfile(xmp_path, dst)
            print ("%s ~> %s" % (xmp_path, dst))
        except shutil.Error:
            pass

f = input("Please input training example folder path:")
uniform_meta(f)
