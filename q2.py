#!/usr/bin/env python
# coding: utf-8

# In[101]:


import sys
import re
import numpy as np
import sklearn
import os
import nltk
from collections import Counter
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

def feat_vector(bigram_l):
    #skeleton dictionary
    temp_dict = dict.fromkeys(unique_bigrams,0)
    temp_counter = Counter(bigram_l)
    for k in temp_counter:
        temp_dict[k] = temp_counter[k]
    return list(temp_dict.values())


# In[87]:


label_list = []
sent_slot_list = []
sent_empty_list = []
with open('/Users/devinbrown/Desktop/Data1/group1.txt') as f:
    for i,l in enumerate(f):
        if i == 0:
            continue
        label_list.append(l.split()[0])
        temp_sent = ' '.join(l.split()[1:])
        temp_sent = re.sub('<[^>]*>','',temp_sent)
        temp_sent = 'BOS {} EOS'.format(temp_sent)
        sent_empty_list.append(temp_sent)
        sent_list.append(' '.join(l.split()[1:]))
        
        
#convert text input to bigrams
bigram_list = []
for l in sent_empty_list:
    bigram_list.append(list(nltk.bigrams(l.split())))

#get unique bigrams
biglist = []
for l in bigram_list:
    biglist+=l
unique_bigrams = sorted(list(set(biglist)))


# In[91]:





# In[95]:


#initialize training set
total_train = [feat_vector(l) for l in bigram_list]
train_X = total_train[:int(len(total_train)*(.8))]
test_X = total_train[int(len(total_train)*(.8)):]
train_Y = label_list[:int(len(total_train)*(.8))]
test_Y = label_list[int(len(total_train)*(.8)):]


# # TRAIN MODEL 

# In[96]:


model = sklearn.svm.SVC()
model.fit(train_X,train_Y)


# # PREDICTIONS 

# In[98]:


preds = list(model.predict(test_X))


# In[114]:


for x,y,z in zip(preds,test_Y,sent_empty_list[80:]):
    print('REAL:',x,'ACTUAL:',y,'SENT:',z)


# In[108]:


print(classification_report(test_Y,preds))


# In[ ]:




