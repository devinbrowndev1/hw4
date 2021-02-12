
from q1 import NLUDefault

line_list = []
with open('/Users/devinbrown/Desktop/Data5/part1.tsv') as f:
	for l in f:
		line_list.append(' '.join(l.split()[2:]))


for i,l in enumerate(line_list):
	if i == 0:
		continue
	print('User:{}'.format(l))
	invalue = l
	NLU = NLUDefault()
	print(NLU.parse(invalue))

