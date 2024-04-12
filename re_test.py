import sys, re
from unicodedata import *
import json
from pprint import pprint

unicode_dict = {}
for i in range(sys.maxunicode):
    c = chr(i)
    try:
        x = (name(c))
        unicode_dict[c] = x
    except:
        pass
#
#
#inFile = open('unicode_list.txt', 'a')
#for unicode_str in unicode_list:
#    try:      
#        inFile.write(unicode_str)
#    except:
#        pass
#inFile.close()

