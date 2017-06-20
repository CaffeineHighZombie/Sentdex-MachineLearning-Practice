#!/usr/bin/env python

import re

handle = open('mbox-short.txt')
count = 0
for line in handle:
	line = line.rstrip()
	if re.search('^From: ', line):
		print(line)
		count+=1

print('Count: ', count)
