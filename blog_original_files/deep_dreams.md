Title: ICYM AI & ML - Week #29 of 2016
Date: 2016-07-25
Category: AI, ML, Review


About an year ago, Google


The results are breathtaking to say the least. Lower levels reveal edge-like regions in the images. Intermediate layers are able to represent basic shapes and components of objects (doorknob, eye, nose, etc.). And lastly, the final layers are able to form the complete interpretation (dog, cat, tree, etc.) — and often in a psychedelic, spaced out manner.


For each of the original images (top), I have generated a “deep dream” using the conv2/3x3 , inception_3b/5x5_reduce , inception_4c/output  layers, respectively.

The conv2/3x3  and inception_3b/5x5_reduce  layers are lower level layers in the network that give more “edge-like” features. The inception_4c/output  layer is the final output that generates trippy hallucinations of dogs, snails, birds, and fish.


* [bat-country](https://github.com/jrosebr1/bat-country)