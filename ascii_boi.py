from PIL import Image, ImageFilter
from math import atan, pi
import argparse
import numpy as np

parser = argparse.ArgumentParser(description='Converts a given image to ascii art.')
parser.add_argument('image_path', metavar='--path', type=str, nargs=1, help="The path to the image of which ascii art is desired.")
parser.add_argument('threshold', metavar='--threshold', type=int, default = 150, nargs=1, help="The grayscale value above which lines are highlighted.")

args = parser.parse_args()
paths = args.image_path
threshold = args.threshold[0]

syms = {

}

for path in paths:
	image = Image.open(path)
	image = image.convert('L')
#	image = image.filter(ImageFilter.GaussianBlur(radius=5))

	kernels = {
		'horizontal_edge':ImageFilter.Kernel((3,3),[1,2,1,0,0,0,-1,-2,-1], scale=1),
		'vertical_edge': ImageFilter.Kernel((3,3), [1,0,-1,2,0,-2,1,0,-1], scale=1) 
	}
	
	results = dict()
	for name, kernel in kernels.items():
		results[name] = image.filter(kernel)
		
	angle  = np.matrix(np.asarray(image))
	magnitude  = np.matrix(np.asarray(image))
	for y, rows in enumerate(zip(np.asarray(image.filter(kernels['horizontal_edge'])), np.asarray(image.filter(kernels['vertical_edge'])))):		
		angle[y] = [(2/pi * 360 * atan(b/a)) // 1 if (a > 0) else 359 for a, b in zip(rows[0], rows[1])]
		magnitude[y] = [(a**2 + b**2)**.5 for a, b in zip(rows[0], rows[1])]


	# Map angles onto RGB color space
	image = Image.new(mode = 'HSV',size = image.size)
	print(image.size, magnitude.shape)
	for x, y in np.ndindex((magnitude.shape[0], magnitude.shape[1])):
		if magnitude[x,y] > threshold:
			image.putpixel((y,x), (angle[x,y], 100, 100))
		else:
			image.putpixel((y,x), (0,0,0))

	

	image.show()
