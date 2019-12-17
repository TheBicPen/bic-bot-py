

import unittest
from helpers_generic import read_dict_from_file

class TestDictRead(unittest.TestCase):
    file = "dict_test"
    def test_normal_line(self):
        self.assertDictContainsSubset({"normal":"line"}, read_dict_from_file(file))
    
    def test_semicolon_line(self):
        self.assertDictContainsSubset({"semicolon:;asd":"value"}, read_dict_from_file(file))
    
    def test_too_many_semicolons_line(self):
        self.assertDictContainsSubset({"too":"many"}, read_dict_from_file(file))
    
    def test_backslash_line(self):
        self.assertDictContainsSubset({"back\slash":"slashed"}, read_dict_from_file(file))
    
    def test_blank_key_2_line(self):
        self.assertDictContainsSubset({"":"2nd blank key"}, read_dict_from_file(file))
    
    def test_normal_line(self):
        self.assertDictContainsSubset({"normal":"line"}, read_dict_from_file(file))
    
    