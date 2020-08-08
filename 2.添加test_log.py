import _pickle as cPickle
from raw_to_html import raw_to_html

# read the pkl file
with open('./pkl/entry.pkl', 'rb') as pkl_file:
    entry_dict = cPickle.load(pkl_file)


# go through the dict
for cur_entry in entry_dict.keys():
    entry_dict[cur_entry]['test_log'] = []
    entry_dict[cur_entry]['test_log_old'] = []
del cur_entry

# output to pkl file
with open('./pkl/entry.pkl', 'wb') as pkl_file:
    cPickle.dump(entry_dict, pkl_file)
