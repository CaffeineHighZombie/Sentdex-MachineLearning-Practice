#!/usr/bin/env python

handle = open('mbox-short.txt')
count = 0
for line in handle:
	line = line.rstrip()
	if line.find('From: ') >= 0:
		print(line)
		count += 1

print('Count: ', count)
