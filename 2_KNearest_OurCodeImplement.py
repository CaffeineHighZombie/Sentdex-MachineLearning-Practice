import numpy as np
import warnings
from collections import Counter
import pandas as pd
import random
import pprint


def k_nearest_neighbors(data, predict, k=3):
	if len(data) >= k:
		warnings.warn('K is set to a value less than total voting groups!')
	distances = []
	for group in data:
		for features in data[group]:
			euclidean_distance = np.linalg.norm(np.array(features)-np.array(predict))
			distances.append([euclidean_distance, group])
	votes = [i[1] for i in sorted(distances)[:k]]
	vote_result = Counter(votes).most_common(1)[0][0]
	confidence = Counter(votes).most_common(1)[0][1] / k
	return vote_result, confidence

df = pd.read_csv('breast-cancer-wisconsin.data')
df.replace('?', -99999, inplace=True)
df.drop(['id'], 1, inplace=True)
full_data = df.astype(float).values.tolist()
# print(df.head())
#pprint.pprint(full_data[:5])
random.shuffle(full_data)
# print('#'*20)
# pprint.pprint(full_data[:5])

test_size = 0.2
train_set = {2:[], 4:[]}
test_set = {2:[], 4:[]}
train_data = full_data[:-int(test_size*len(full_data))]
test_data = full_data[-int(test_size*len(full_data)):]

for data_row in train_data:
	train_set[data_row[-1]].append(data_row[:-1])

for data_row in test_data:
	test_set[data_row[-1]].append(data_row[:-1])

correct = 0
total = 0

for group in test_set:
	for data in test_set[group]:
		vote, confidence = k_nearest_neighbors(train_set, data, k=5)
		if vote == group:
			correct += 1
		else:
			print(confidence, group, data)
		total += 1

print("Accuracy: {}".format(correct/total))

