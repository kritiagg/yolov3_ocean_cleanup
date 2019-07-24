import os

folder = "/home/ziweideng_linux_gpu/GitHub/yolov3_ocean_cleanup/data/"
edit_file = "3_set_combined_train.txt"
#edit_file = "3_set_combined_train.txt"

# Sanity check
if os.path.isfile(folder + './ocean_data/ocean_drone_images/2018.10.20_DJI_0001_BL.jpg'):
	print("Sanity passed!")
else:
	print("Sanity failed!")



with open("corrected_" + edit_file, "w") as g:
	with open(edit_file, "r") as f:
		for line in f:
			if os.path.isfile(folder + line.split( )[1]):
				g.write(line)
