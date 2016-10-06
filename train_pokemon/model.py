# -*- coding: utf-8 -*-
import json, os, sys
from args import args
sys.path.append(os.path.split(os.getcwd())[0])
from dcdgm import DCDGM, Params

# load params.json
try:
	os.mkdir(args.model_dir)
except:
	pass
filename = args.model_dir + "/params.json"
if os.path.isfile(filename):
	print "loading", filename
	f = open(filename)
	try:
		dict = json.load(f)
		params = Params(dict)
	except:
		raise Exception("could not load {}".format(filename))

	params.gpu_enabled = True if args.gpu_enabled == 1 else False
else:
	params = Params()
	params.x_width = 40
	params.x_height = params.x_width
	params.x_channels = 3
	params.ndim_z = 10
	params.apply_dropout = False
	params.distribution_x = "tanh"

	params.energy_model_num_experts = 128
	params.energy_model_feature_extractor_hidden_channels = [16, 32, 64]
	params.energy_model_feature_extractor_stride = 2
	params.energy_model_feature_extractor_ksize = 4
	params.energy_model_feature_extractor_ndim_output = 128
	params.energy_model_batchnorm_to_input = False
	params.energy_model_batchnorm_before_activation = False
	params.energy_model_batchnorm_enabled = False
	params.energy_model_wscale = 1
	params.energy_model_activation_function = "elu"

	params.generative_model_hidden_channels = [64, 32, 16]
	params.generative_model_stride = 2
	params.generative_model_ksize = 4
	params.generative_model_batchnorm_to_input = False
	params.generative_model_batchnorm_before_activation = True
	params.generative_model_batchnorm_enabled = True
	params.generative_model_wscale = 1
	params.generative_model_activation_function = "elu"

	params.gradient_clipping = 10
	params.weight_decay = 0
	params.learning_rate = 0.0001
	params.gpu_enabled = True if args.gpu_enabled == 1 else False

	params.check()
	with open(filename, "w") as f:
		json.dump(params.to_dict(), f, indent=4)

params.dump()
dcdgm = DCDGM(params)
dcdgm.load(args.model_dir)