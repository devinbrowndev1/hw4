
from q2 import NLUDefault

print('Prompt:')
invalue = input()
NLU = NLUDefault()
print(NLU.parse(invalue))

