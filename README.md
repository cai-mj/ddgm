## Deep Directed Generative Models with Energy-Based Probability Estimation

code for the [paper](https://arxiv.org/abs/1606.03439)

[この記事](http://musyoku.github.io/2016/10/28/Deep-Directed-Generative-Models-with-Energy-Based-Probability-Estimation/)で実装したコードです。

### Requirements

- Chainer 1.17
- PIL
- pylab

Contains the following repository:

- [chainer-sequential](https://github.com/musyoku/chainer-sequential)

## 2D datasets

![gaussian](https://github.com/musyoku/musyoku.github.io/blob/master/images/post/2016-10-28/gaussian.png?raw=true)
![swiss_roll](https://github.com/musyoku/musyoku.github.io/blob/master/images/post/2016-10-28/swissroll.png?raw=true)

See videos:

- [https://gfycat.com/DarlingShowyHypsilophodon](https://gfycat.com/DarlingShowyHypsilophodon)
- [https://gfycat.com/UnrulyMisguidedHornedviper](https://gfycat.com/UnrulyMisguidedHornedviper)

### Running

run `train_2d/train.py` to train the model.

run `train_2d/gif_gaussian.py` or `train_2d/gif_swissroll.py` to generate gif frames.

## MNIST

run `train_mnist/train.py`

It will automatically download MNIST dataset.

### Genereted images

![result](https://github.com/musyoku/musyoku.github.io/blob/master/images/post/2016-10-28/mnist_success.png?raw=true)

## killmebaby（キルミーベイベー）

Download 686 images from [http://killmebaby.tv/special_icon.html](http://killmebaby.tv/special_icon.html) and
resize all images to 64x64.

run `train_killmebaby/train.py` 

### Original images

![original](https://github.com/musyoku/musyoku.github.io/blob/master/images/post/2016-10-28/kb_original.png?raw=true)

### Images generated by Deep Generative Model

![gen](https://github.com/musyoku/musyoku.github.io/blob/master/images/post/2016-10-28/kb_gen.png?raw=true)