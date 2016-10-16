import sys, os
import numpy as np
sys.path.append(os.path.split(os.getcwd())[0])
import visualizer
from args import args
from model import params, dcdgm

def plot(filename="gen"):
	try:
		os.mkdir(args.plot_dir)
	except:
		pass

	x_negative = dcdgm.generate_x(100, test=True, as_numpy=True)
	x_negative = (x_negative + 1) / 2
	visualizer.tile_rgb_images(x_negative.transpose(0, 2, 3, 1), dir=args.plot_dir, image_width=params.x_width, image_height=params.x_height, filename=filename)

if __name__ == '__main__':
	plot()
