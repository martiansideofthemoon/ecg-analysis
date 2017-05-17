"""This generates the vectors."""
import glob
import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import random

from pywt import wavedec
from tsne import tsne

np.random.seed(0)

files = glob.glob("final_positive/*.csv")
outputs = []
labels = []
print len(files)
for file1 in files:
    data = np.genfromtxt(file1, delimiter=",")
    samples = data[:, 1]
    output = wavedec(samples, wavelet='db8', level=4)
    output = np.concatenate((output[0], output[1], output[2]))
    outputs.append(output)
    labels.append(0)

files = glob.glob("final_negative/*.csv")

for file1 in files:
    data = np.genfromtxt(file1, delimiter=",")
    samples = data[:, 1]
    output = wavedec(samples, wavelet='db8', level=4)
    output = np.concatenate((output[0], output[1], output[2]))
    outputs.append(output)
    labels.append(1)

c = list(zip(outputs, labels))
random.shuffle(c)
outputs, labels = zip(*c)

outputs = np.array(outputs)
labels = np.array(labels)

# Uncomment below to generate random data
# outputs = np.random.rand(len(labels), 100)

# Put `no_dims=3` for 3D plots
final = tsne(outputs, no_dims=2)

# Use the following snippet for 3-D plots
# fig = pylab.figure()
# ax = Axes3D(fig)
# ax.scatter(final[:, 0], final[:, 1], final[:, 2], c=labels)
# plt.show()

plt.scatter(final[:, 0], final[:, 1], c=labels, marker='o')
plt.show()
