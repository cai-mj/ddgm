# -*- coding: utf-8 -*-
import json, os, sys
from args import args
sys.path.append(os.path.split(os.getcwd())[0])
from ddgm import DDGM, Params

# load params.json
try:
	os.mkdir(args.params_dir)
except:
	pass
filename = args.params_dir + "/{}".format(args.params_filename)
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
	params.ndim_x = 2
	params.ndim_z = 4
	params.activation_function = "elu"
	params.apply_dropout = False

	params.energy_model_num_experts = 4
	params.energy_model_features_hidden_units = [128, 128]
	params.energy_model_apply_batchnorm_to_input = False
	params.energy_model_batchnorm_before_activation = True
	params.energy_model_batchnorm_enabled = False

	params.generative_model_hidden_units = [128, 128]
	params.generative_model_apply_batchnorm_to_input = False
	params.generative_model_batchnorm_before_activation = True
	params.generative_model_batchnorm_enabled = False

	params.wscale = 0.01
	params.gradient_clipping = 5
	params.gradient_momentum = 0.9
	params.weight_decay = 0
	params.learning_rate = 0.0003
	params.gpu_enabled = True if args.gpu_enabled == 1 else False

	params.check()
	with open(filename, "w") as f:
		json.dump(params.to_dict(), f, indent=4)

params.dump()
ddgm = DDGM(params)
ddgm.load(args.model_dir)