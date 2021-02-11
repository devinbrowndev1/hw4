
from q2 import NLUDefault

invalue = ''
while invalue != 'q':
	print('Prompt:')
	invalue = input()
	NLU = NLUDefault()
	print(NLU.parse(invalue))

