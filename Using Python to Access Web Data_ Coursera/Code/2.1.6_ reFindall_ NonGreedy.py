#!/usr/bin/env python

import re

x = 'From: Using the: character'
y = re.findall('^F.+:', x)
print('Greedy')
print(y)
y = re.findall('^F.+?:', x)
print('Non-Greedy')
print(y)

