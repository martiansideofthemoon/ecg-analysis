"""Extract data from positive_points.txt."""
import os
import wfdb
import numpy as np
import scipy.signal as signal


def filter_sig(input_sig):
    """Filter the signal to remove noise."""
    f_sample = 1000
    f_cutoff = 25
    b, a = signal.butter(6, f_cutoff / (f_sample / 2.0))
    sig1 = signal.lfilter(b, a, input_sig)
    sig11 = signal.medfilt(sig1, 201)
    sig12 = signal.medfilt(sig11, 601)
    sig1 = sig1 - sig12
    return sig1

with open('positive_points3.txt', 'r') as f:
    points = f.read().split('\n')

# Uncomment for control points
# with open('negative_points3.txt', 'r') as f:
#     points = f.read().split('\n')

if not os.path.exists('final_positive'):
    os.makedirs('final_positive')
if not os.path.exists('final_negative'):
    os.makedirs('final_negative')

folder = 'final_positive/'
# Uncomment for control points
# folder = 'final_negative/'

for i, point in enumerate(points):
    print i
    record = point.split()
    # Uncomment for control points
    # sig, fields = wfdb.rdsamp("negative/" + record[0], channels=[7], sampfrom=6000, sampto=9000)
    sig, fields = wfdb.rdsamp("positive/" + record[0], channels=[7], sampfrom=6000, sampto=9000)
    sig[:, 0] = filter_sig(sig[:, 0])
    sig = sig[int(record[2]):int(record[3]), 0]
    output = ""
    for i in range(len(sig)):
        output += str(i / 1000.0) + "," + str(sig[i]) + "\n"
    with open(folder + record[0].replace('/', '-') + ".csv", 'w') as f:
        f.write(output)
