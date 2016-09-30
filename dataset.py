# -*- coding: utf-8 -*-
import os, re, math, pylab, sys
from math import *
import numpy as np
from StringIO import StringIO
from PIL import Image
from chainer import cuda, Variable, function
from chainer.utils import type_check
from sklearn import preprocessing
import matplotlib

def load_images(image_dir, is_grayscale=True):
	dataset = []
	fs = os.listdir(image_dir)
	i = 0
	for fn in fs:
		f = open("%s/%s" % (image_dir, fn), "rb")
		if is_grayscale:
			img = np.asarray(Image.open(StringIO(f.read())).convert("L"), dtype=np.float32) / 255.0
		else:
			img = np.asarray(Image.open(StringIO(f.read())).convert("RGB"), dtype=np.float32).transpose(2, 0, 1) / 255.0
		dataset.append(img)
		f.close()
		i += 1
		if i % 100 == 0:
			sys.stdout.write("\rloading images...({:d} / {:d})".format(i, len(fs)))
			sys.stdout.flush()
	sys.stdout.write("\n")
	return dataset

def binarize_data(x):
	threshold = np.random.uniform(size=x.shape)
	return np.where(threshold < x, 1.0, 0.0).astype(np.float32)