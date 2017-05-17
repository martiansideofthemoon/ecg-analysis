"""Extract all the csv data."""
import os
import requests

base_url = 'https://www.physionet.org/physiobank/database/ptbdb/'
records = 'RECORDS'
response = requests.get(base_url + records)
records = response.text.split()

data = '.dat'
xyz = '.xyz'
hea = '.hea'

for index, record in enumerate(records):
    print str(index) + " / " + str(len(records)) + " - " + record
    data_url = base_url + record + data
    xyz_url = base_url + record + xyz
    hea_url = base_url + record + hea
    response = requests.get(data_url)
    if not os.path.exists(record.split('/')[0]):
        os.makedirs(record.split('/')[0])
    with open(record + data, 'wb') as f:
        f.write(response.content)
    response = requests.get(xyz_url)
    with open(record + xyz, 'wb') as f:
        f.write(response.content)
    response = requests.get(hea_url)
    with open(record + hea, 'w') as f:
        f.write(response.text)
