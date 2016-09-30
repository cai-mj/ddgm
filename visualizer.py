import pylab
import numpy as np
from StringIO import StringIO
from PIL import Image
import matplotlib.patches as mpatches

def tile_x(x, image_width=28, image_height=28, image_channel=1, dir=None, filename="x"):
	if dir is None:
		raise Exception()
	try:
		os.mkdir(dir)
	except:
		pass
	fig = pylab.gcf()
	fig.set_size_inches(16.0, 16.0)
	pylab.clf()
	if image_channel == 1:
		pylab.gray()
	for m in range(100):
		pylab.subplot(10, 10, m + 1)
		if image_channel == 1:
			pylab.imshow(x[m].reshape((image_width, image_height)), interpolation="none")
		elif image_channel == 3:
			pylab.imshow(x[m].reshape((image_channel, image_width, image_height)), interpolation="none")
		pylab.axis("off")
	pylab.savefig("{}/{}.png".format(dir, filename))

def plot_z(z, dir=None, filename="z"):
	if dir is None:
		raise Exception()
	try:
		os.mkdir(dir)
	except:
		pass
	fig = pylab.gcf()
	fig.set_size_inches(20.0, 16.0)
	pylab.clf()
	for n in xrange(z.shape[0]):
		result = pylab.scatter(z[n, 0], z[n, 1], s=40, marker="o", edgecolors='none')
	pylab.xlabel("z1")
	pylab.ylabel("z2")
	pylab.savefig("{}/{}.png".format(dir, filename))
