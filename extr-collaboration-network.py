#!/usr/bin/env python3
import json

f_input = 'contributors.json'
# Load the data
with open(f_input) as f:
    data = json.load(f)

for repo in data:
    contributors = []
    for contributor in data[repo]:
        contributors.append(contributor['login'])

    # print as A-B list
    for i in range(len(contributors)):
        for j in range(i+1, len(contributors)):
            print(contributors[i], contributors[j])
