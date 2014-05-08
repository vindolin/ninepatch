import sys
import os
import unittest
import filecmp
import tempfile

sys.path.insert(0, os.path.dirname(__file__) + '/')

import ninepatch


class TestNinepatch(unittest.TestCase):
    def test_ninepatch(self):
        # compare with the test image
        image_path = os.path.dirname(os.path.realpath(__file__)) + os.sep
        test_image = image_path + os.sep + '9patch_test.png'
        original_image = image_path + 'test_original_421_333.png'
        scaled_image = tempfile.gettempdir() + os.sep + 'test_scaled_421_333.png'
        ninepatch_ = ninepatch.Ninepatch(test_image)
        ninepatch_.render(421, 333).save(scaled_image, format='PNG')
        self.assertTrue(filecmp.cmp(scaled_image, original_image))
        os.remove(scaled_image)
