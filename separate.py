"""This file extracts the diagnosis of various patients."""
import re
import os

disease_re = re.compile(
    r'\#\sReason\sfor\sadmission:\s(.*)\s\#\sAcute\sinfarction\s\(localization\):\s(.*)\s\#')

with open('data/patients.txt', 'r') as f:
    records = f.read()

records = records.split()
diagnosis = []
positive = []
control = []
for record in records:
    print record
    filename = os.path.join("data", record + ".hea")
    if not os.path.exists(filename):
        break
    with open(filename, 'r') as f:
        data = f.read()
    result = disease_re.search(data)
    if result is not None:
        disease = result.group(1)[:-1]
        location = result.group(2)[:-1]
        diagnosis.append((disease, location))
        if disease == "Myocardial infarction" and location == "anterior":
            positive.append(record)
        elif disease == "Healthy control":
            control.append(record)
    else:
        print "Error"

with open("positive.txt", "w") as f:
    f.write("\n".join(positive))
with open("control.txt", "w") as f:
    f.write("\n".join(control))

# Actual segregation of data

if not os.path.exists('positive'):
    os.makedirs('positive')
if not os.path.exists('negative'):
    os.makedirs('negative')

for p in positive:
    folder = p.split('/')[0]
    os.system('cp -r ' + folder + ' positive/')

for p in control:
    folder = p.split('/')[0]
    os.system('cp -r ' + folder + ' negative/')
