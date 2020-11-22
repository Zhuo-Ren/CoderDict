import _pickle as cPickle
from raw_to_html import raw_to_html

memorize_dict = {}

# output to pkl file
with open('./pkl/memorize.pkl', 'wb') as pkl_file:
    cPickle.dump(memorize_dict, pkl_file)
