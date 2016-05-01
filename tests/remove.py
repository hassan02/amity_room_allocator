import os
class Remove(object):
  def __init__(self):
    if os.path.isfile(os.path.realpath('test_data_files/test_persons_ids.db')):
      os.remove(os.path.realpath('test_data_files/test_persons_ids.db'))
      print('Removed')
    if os.path.isfile(os.path.realpath('test_data_files/test_offices.db')):
      os.remove(os.path.realpath('test_data_files/test_offices.db'))
      print('Removed')
    if os.path.isfile(os.path.realpath('test_data_files/test_living.db')):
      os.remove(os.path.realpath("test_data_files/test_living.db"))
      print('Removed')
    if os.path.isfile(os.path.realpath('test_data_files/test_fellows.db')):
      os.remove(os.path.realpath("test_data_files/test_fellows.db"))
      print('Removed')
    if os.path.isfile(os.path.realpath('test_data_files/test_staff.db')):
      os.remove(os.path.realpath("test_data_files/test_staff.db"))
      print('Removed')
Remove()
