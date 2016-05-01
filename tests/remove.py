import os
if os.path.isfile(os.path.realpath('test_data_files/test_persons_ids.db')):
  os.remove(os.path.realpath('test_data_files/test_persons_ids.db')) 
if os.path.isfile(os.path.realpath('test_data_files/test_offices.db')):
  os.remove(os.path.realpath("test_data_files/test_offices.db"))
if os.path.isfile(os.path.realpath('test_data_files/test_living.db')):
  os.remove(os.path.realpath("test_data_files/test_living.db"))
if os.path.isfile(os.path.realpath('test_data_files/test_fellows.db')):
  os.remove(os.path.realpath("test_data_files/test_fellows.db"))
if os.path.isfile(os.path.realpath('test_data_files/test_staff.db')):
  os.remove(os.path.realpath("test_data_files/test_staff.db"))
