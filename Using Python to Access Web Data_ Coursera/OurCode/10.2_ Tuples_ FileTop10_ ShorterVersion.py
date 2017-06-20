#!/usr/bin/env python

# Getting the local file name and opening it
fileName = input('Enter the file name: ')
if len(fileName) < 1 : fileName = 'clown.txt'
handle = open(fileName)

# Making a histogram of word counts int the file
counts = dict()
for line in handle:
	words = line.split()
	for word in words:
		counts[word] = counts.get(word, 0) + 1

# Sorting the word count and printing out top 10 values

print('The top 10 word counts are: ')
for count, word in sorted([(v,k) for (k,v) in counts.items()], reverse=True)[:10]:
	print(word, count)

