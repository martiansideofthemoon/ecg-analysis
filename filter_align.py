"""Use exisiting software to display waves one by one."""
import wfdb
import numpy as np
import scipy.signal as signal


def passband(fs, f1, f2):
    """Implement a passband."""
    b = signal.firwin(20, [f1 * 2 / fs, f2 * 2 / fs], pass_zero=False)
    return b


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

# Uncomment for control point analysis
# print "Starting negative sequence of files"
# with open('control.txt', 'r') as f:
#     control = f.read().split()

print "Starting positive sequence of files"
with open('positive.txt', 'r') as f:
    control = f.read().split()

output1 = ""
for p in control:
    sig, fields = wfdb.rdsamp("positive/" + p, channels=[7], sampfrom=6000, sampto=9000)
    sig[:, 0] = filter_sig(sig[:, 0])
    output2 = signal.find_peaks_cwt(-1 * sig[:, 0], np.arange(10, 20))
    minima = list(sig[output2])
    for x in output2:
        print str(x) + " - " + str(sig[x])
    sum_vals = []
    threshold = -1
    while len(sum_vals) <= 2:
        sum_vals = [x for x in minima if x < threshold]
        threshold += 0.1
    index = output2[minima.index(sum_vals[len(sum_vals) / 2])]
    # Uncomment for control points
    # max_found = False
    # while max_found is False:
    #     if sig[index] > sig[index - 1] and \
    #        sig[index] > sig[index - 2] and \
    #        sig[index] > sig[index + 1] and \
    #        sig[index] > sig[index + 2] and \
    #        sig[index] > sig[index + 3] and \
    #        sig[index] > sig[index - 3]:
    #        max_found = True
    #     else:
    #         index -= 1
    # print index
    # print sig[index]
    # while abs(sig[index]) > 0.01:
    #     print sig[index]
    #     index -= 1
    output1 += p + " " + str(index) + " " + str(index - 200) + " " + str(index + 600) + "\n"

# Uncomment for control points
# with open("negative_points3.txt", 'w') as f:
#     f.write(output1)

with open("positive_points3.txt", 'w') as f:
    f.write(output1)
