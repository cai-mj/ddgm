# -*- coding: utf-8 -*-
import math
import json, os, sys
from chainer import cuda
from args import args
sys.path.append(os.path.split(os.getcwd())[0])
from params import Params
from ddgm import DDGM, EnergyModelParams, GenerativeModelParams, DeepEnergyModel, DeepGenerativeModel
from sequential import Sequential
from sequential.layers import Linear, BatchNormalization, Deconvolution2D, Convolution2D, MinibatchDiscrimination
from sequential.functions import Activation, dropout, gaussian_noise, tanh, sigmoid, reshape, reshape_1d
from sequential.util import get_conv_padding, get_paddings_of_deconv_layers, get_in_size_of_deconv_layers

# load params.json
try:
	os.mkdir(args.model_dir)
except:
	pass

# data
image_width = 64
image_height = image_width
ndim_latent_code = 10

# specify energy model
energy_model_filename = args.model_dir + "/energy_model.json"

if os.path.isfile(energy_model_filename):
	print "loading", energy_model_filename
	with open(energy_model_filename, "r") as f:
		try:
			params = json.load(f)
		except Exception as e:
			raise Exception("could not load {}".format(energy_model_filename))
else:
	config = EnergyModelParams()
	config.num_experts = 512
	config.weight_init_std = 0.05
	config.weight_initializer = "Normal"
	config.use_weightnorm = False
	config.nonlinearity = "elu"
	config.optimizer = "Adam"
	config.learning_rate = 0.0002
	config.momentum = 0.5
	config.gradient_clipping = 10
	config.weight_decay = 0

	# feature extractor
	feature_extractor = Sequential(weight_initializer=config.weight_initializer, weight_init_std=config.weight_init_std)
	feature_extractor.add(Convolution2D(3, 32, ksize=4, stride=2, pad=1, use_weightnorm=config.use_weightnorm))
	feature_extractor.add(BatchNormalization(32))
	feature_extractor.add(Activation(config.nonlinearity))
	feature_extractor.add(dropout())
	feature_extractor.add(Convolution2D(32, 64, ksize=4, stride=2, pad=1, use_weightnorm=config.use_weightnorm))
	feature_extractor.add(BatchNormalization(64))
	feature_extractor.add(Activation(config.nonlinearity))
	feature_extractor.add(dropout())
	feature_extractor.add(Convolution2D(64, 192, ksize=4, stride=2, pad=1, use_weightnorm=config.use_weightnorm))
	feature_extractor.add(BatchNormalization(192))
	feature_extractor.add(Activation(config.nonlinearity))
	feature_extractor.add(dropout())
	feature_extractor.add(Convolution2D(192, 256, ksize=4, stride=2, pad=1, use_weightnorm=config.use_weightnorm))
	feature_extractor.add(reshape_1d())
	feature_extractor.add(MinibatchDiscrimination(None, num_kernels=50, ndim_kernel=5, train_weights=True))
	feature_extractor.add(tanh())

	# experts
	experts = Sequential(weight_initializer=config.weight_initializer, weight_init_std=config.weight_init_std)
	experts.add(Linear(None, config.num_experts, use_weightnorm=config.use_weightnorm))

	# b
	b = Sequential(weight_initializer=config.weight_initializer, weight_init_std=config.weight_init_std)
	b.add(Linear(None, 1, nobias=True))

	params = {
		"config": config.to_dict(),
		"feature_extractor": feature_extractor.to_dict(),
		"experts": experts.to_dict(),
		"b": b.to_dict(),
	}

	with open(energy_model_filename, "w") as f:
		json.dump(params, f, indent=4, sort_keys=True, separators=(',', ': '))

params_energy_model = params

# specify generative model
generative_model_filename = args.model_dir + "/generative_model.json"

if os.path.isfile(generative_model_filename):
	print "loading", generative_model_filename
	with open(generative_model_filename, "r") as f:
		try:
			params = json.load(f)
		except:
			raise Exception("could not load {}".format(generative_model_filename))
else:
	config = GenerativeModelParams()
	config.ndim_input = ndim_latent_code
	config.distribution_output = "sigmoid"
	config.use_weightnorm = False
	config.weight_init_std = 0.05
	config.weight_initializer = "Normal"
	config.nonlinearity = "relu"
	config.optimizer = "Adam"
	config.learning_rate = 0.0002
	config.momentum = 0.5
	config.gradient_clipping = 10
	config.weight_decay = 0

	# model
	# compute projection width
	input_size = get_in_size_of_deconv_layers(image_width, num_layers=3, ksize=4, stride=2)
	# compute required paddings
	paddings = get_paddings_of_deconv_layers(image_width, num_layers=3, ksize=4, stride=2)

	model = Sequential(weight_initializer=config.weight_initializer, weight_init_std=config.weight_init_std)
	model.add(Linear(config.ndim_input, 512 * input_size ** 2, use_weightnorm=config.use_weightnorm))
	model.add(BatchNormalization(512 * input_size ** 2))
	model.add(Activation(config.nonlinearity))
	model.add(reshape((-1, 512, input_size, input_size)))
	model.add(Deconvolution2D(512, 256, ksize=4, stride=2, pad=paddings.pop(0), use_weightnorm=config.use_weightnorm))
	model.add(BatchNormalization(256))
	model.add(Activation(config.nonlinearity))
	model.add(Deconvolution2D(256, 128, ksize=4, stride=2, pad=paddings.pop(0), use_weightnorm=config.use_weightnorm))
	model.add(BatchNormalization(128))
	model.add(Activation(config.nonlinearity))
	model.add(Deconvolution2D(128, 3, ksize=4, stride=2, pad=paddings.pop(0), use_weightnorm=config.use_weightnorm))
	if config.distribution_output == "sigmoid":
		model.add(sigmoid())
	if config.distribution_output == "tanh":
		model.add(tanh())

	params = {
		"config": config.to_dict(),
		"model": model.to_dict(),
	}

	with open(generative_model_filename, "w") as f:
		json.dump(params, f, indent=4, sort_keys=True, separators=(',', ': '))

params_generative_model = params

ddgm = DDGM(params_energy_model, params_generative_model)
ddgm.load(args.model_dir)

if args.gpu_device != -1:
	cuda.get_device(args.gpu_device).use()
	ddgm.to_gpu()