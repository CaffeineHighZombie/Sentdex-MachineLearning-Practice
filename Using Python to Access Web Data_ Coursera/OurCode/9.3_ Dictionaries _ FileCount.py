#!/usr/bin/env python

# Getting the file name and opening it
fileName = input('Enter the file name: ')
handle = open(fileName)

# parsing the words in the file and making a histogram in a dictionary
counts = dict()
for line in handle:
	words = line.split()
	for word in words:
		counts[word] = counts.get(word, 0) + 1

# Finding the word with largest count and print out both word and its count
bigWord = None
bigCount = None
for word, count in counts.items():
	if bigCount is None or bigCount < count:
		bigCount = count
		bigWord = word

print(bigWord, bigCount)
