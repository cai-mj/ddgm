import numpy as np
import os, sys, time
from chainer import cuda
from chainer import functions as F
sys.path.append(os.path.split(os.getcwd())[0])
from model import params, ddgm
from args import args
from dataset import binarize_data, load_images
import dataset

def sample_from_data(images, batchsize):
	example = images[0]
	ndim_x = example.size
	x_batch = np.zeros((batchsize, ndim_x), dtype=np.float32)
	indices = np.random.choice(np.arange(len(images), dtype=np.int32), size=batchsize, replace=False)
	for j in range(batchsize):
		data_index = indices[j]
		img = (images[data_index] - 0.5) * 2
		x_batch[j] = img.reshape((ndim_x,))

	# binalize
	x_batch = binarize_data(x_batch)

	return x_batch

def main():
	# load MNIST images
	images = load_images(args.image_dir)
	
	# settings
	max_epoch = 1000
	n_trains_per_epoch = 5000
	batchsize_positive = 128
	batchsize_negative = 128

	# seed
	np.random.seed(args.seed)
	if params.gpu_enabled:
	    cuda.cupy.random.seed(args.seed)

	total_time = 0
	for epoch in xrange(1, max_epoch):
		sum_energy_positive = 0
		sum_energy_negative = 0
		sum_kld = 0
		epoch_time = time.time()

		for t in xrange(n_trains_per_epoch):
			# sample from data distribution
			x_positive = sample_from_data(images, batchsize_positive)

			# train energy model
			x_negative = ddgm.generate_x(batchsize_negative)
			loss, energy_positive, energy_negative = ddgm.compute_loss(x_positive, x_negative)
			# ddgm.backprop_energy_model(energy_positive)
			# ddgm.backprop_energy_model(-energy_negative)
			ddgm.backprop_energy_model(loss)

			# train generative model
			# TODO: KLD must be greater than or equal to 0
			x_negative = ddgm.generate_x(batchsize_negative)
			kld = ddgm.compute_kld_between_generator_and_energy_model(x_negative)
			ddgm.backprop_generative_model(kld)

			sum_energy_positive += float(energy_positive.data)
			sum_energy_negative += float(energy_negative.data)
			sum_kld += float(kld.data)
			if t % 10 == 0:
				sys.stdout.write("\rTraining in progress...({} / {})".format(t, n_trains_per_epoch))
				sys.stdout.flush()

		epoch_time = time.time() - epoch_time
		total_time += epoch_time
		sys.stdout.write("\r")
		print "epoch: {} energy: x+ {:.3f} x- {:.3f} kld: {:.3f} time: {} min total: {} min".format(epoch + 1, sum_energy_positive / n_trains_per_epoch, sum_energy_negative / n_trains_per_epoch, sum_kld / n_trains_per_epoch, int(epoch_time / 60), int(total_time / 60))
		sys.stdout.flush()
		ddgm.save(args.model_dir)

if __name__ == '__main__':
	main()
