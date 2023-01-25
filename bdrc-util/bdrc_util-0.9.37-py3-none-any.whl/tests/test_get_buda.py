import unittest

from util_lib.GetFromBUDA import get_disk_volumes_in_work, get_buda_ig_from_disk, get_ig_folders_from_igs, old_hack_get_ig_disk


class TestGetBUDAig(unittest.TestCase):


    def test_get_BUDA_ig_from_disk_when_empty(self):
        expect_when_empty_arg:str = ""
                    # Act
        empty_rc = get_buda_ig_from_disk("")
        self.assertEqual(empty_rc,expect_when_empty_arg)

    def test_get_BUDA_ig_from_disk_when_hack(self):
        no_hyphen_arg= "1234"
        expect_when_no_hyphen = "I1234"
        no_hyphen_rc= get_buda_ig_from_disk(no_hyphen_arg)
        self.assertEqual(expect_when_no_hyphen, no_hyphen_rc)

    def test_get_BUDA_ig_from_disk_when_not_hack(self):
        no_hyphen_arg = "I1PD1234"
        no_hyphen_rc = get_buda_ig_from_disk(no_hyphen_arg)
        self.assertEqual(no_hyphen_arg, no_hyphen_rc)

    def test_get_BUDA_ig_from_disk_when_hyphen_and_not_hack(self):
        expected_hyphen_val = "I1PD1234"
        no_hyphen_rc = get_buda_ig_from_disk('W1PD4321-' + expected_hyphen_val)
        self.assertEqual(expected_hyphen_val, no_hyphen_rc)

    def test_get_BUDA_ig_from_disk_when_file_and_hyphen_and_not_hack(self):
        expected_hyphen_val = "I1PD1234"
        no_hyphen_rc = get_buda_ig_from_disk('/dir1/first-hyphen/W1PD4321-' + expected_hyphen_val)
        self.assertEqual(expected_hyphen_val, no_hyphen_rc)

    def test_get_BUDA_ig_from_disk_when_hyphen_and_hack(self):
        test_val = "W100KAtME-1234"
        expected_hyphen_val = "I1234"
        hyphen_rc = get_buda_ig_from_disk(test_val)
        self.assertEqual(expected_hyphen_val, hyphen_rc)

    def test_get_BUDA_ig_from_disk_when_file_and_hyphen_and_hack(self):
        expected_hyphen_val = "I1234"
        test_str: str  = '/dir1/first-hyphen/W1PD4321-' + expected_hyphen_val
        hyphen_rc = get_buda_ig_from_disk(test_str)
        self.assertEqual(expected_hyphen_val, hyphen_rc)


class TestGetDiskFromBUDA(unittest.TestCase):
    def test_fetch(self):
        v_n = get_disk_volumes_in_work('W00EGS1016733')
        self.assertEqual(len(v_n), 50)
        for v in v_n:
            self.assertTrue(str(v['vol_label']).startswith("I8LS"))

    def test_old_hack_get_ig_disk_empty(self):
        expected_str: str = ''
        actual:str = old_hack_get_ig_disk('')
        self.assertEqual(expected_str, actual)

    def test_old_hack_when_hack(self):
        expected_str = '1234'
        test_str = 'I1234'
        actual = old_hack_get_ig_disk(test_str)
        self.assertEqual(expected_str, actual)

    def test_old_hack_when_not_hack(self):
        expected_str = 'I12345'
        test_str = expected_str
        actual = old_hack_get_ig_disk(test_str)
        self.assertEqual(expected_str, actual)

        # Test hack exception Image group folder name, although this case doesn't actually arise
        expected_str = 'Howdy-I1234'
        test_str = expected_str
        actual = old_hack_get_ig_disk(test_str)
        self.assertEqual(expected_str, actual)




if __name__ == '__main__':
    unittest.main()


