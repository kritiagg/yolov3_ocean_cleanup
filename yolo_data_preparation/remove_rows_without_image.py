import os
import glob

def convertFilenames(folder):
    for filename in os.listdir(folder):
        os.chdir(folder)
        new_name = str(filename)
        new_name = new_name.replace(" ", "_")
        os.rename(filename, new_name)

folder = "C:/Users/ziden/GitHub/plasticfreeoceans/Machinelearning/rivercam/images/river_cam/" #specify path
convertFilenames(folder)


# working = set()

# for filename in os.listdir(folder):
#     working.add(filename)
#
# with open("C:/Users/ziden/GitHub/plasticfreeoceans/Machinelearning/rivercam-Copy/corrected_train_rivercam.txt",
#           "w") as g:
#     with open(edit_file, "r") as f:
#         for line in f:
#
#             if line.split(' ')[1] in working:
#                 g.write(line)