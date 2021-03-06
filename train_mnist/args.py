# -*- coding: utf-8 -*-
import argparse

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument("--gpu_enabled", type=int, default=1)
parser.add_argument("--model_dir", type=str, default="model")
parser.add_argument("--plot_dir", type=str, default="plot")

# seed
parser.add_argument("--seed", type=int, default=None)

args = parser.parse_args()