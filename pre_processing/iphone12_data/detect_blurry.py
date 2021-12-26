import cv2
import argparse
import glob
import os
import numpy as np


ap = argparse.ArgumentParser()
ap.add_argument('-i', '--images', required=True,)
ap.add_argument('-t', '--threshold', type=float)
args = vars(ap.parse_args())

rgb_filelst = os.path.join(args['images'], "rgb")
file_list = [file for file in glob.glob("{}/*.jpg".format(rgb_filelst))]

num_blurry = 0
num_non_blurry = 0
non_blurry_file_list = []
for file in file_list:
	image = cv2.imread(file)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	fm = cv2.Laplacian(gray, cv2.CV_64F).var()
	text = "Not Blurry"

	if fm < args["threshold"]:
		text = "Blurry"
		num_blurry += 1
	else:
		non_blurry_file_list.append(file.split("/")[-1])
		print(file.split("/")[-1], fm)
		num_non_blurry += 1

print("total number of blurry ", len(file_list), num_blurry, num_non_blurry)

non_blurry_file = os.path.join(args['images'], "non_blurry.txt")

with open(non_blurry_file, 'w') as f:
    for item in non_blurry_file_list:
        f.write("%s\n" % item)



# cv2.putText(image, "{}: {:.2f}".format(text, fm), (10, 30),
# 	cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
# cv2.imshow("Image", image)
# cv2.waitKey(0)