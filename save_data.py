import shelve
id_list = shelve.open('persons_ids')
print id_list['all_ids']
