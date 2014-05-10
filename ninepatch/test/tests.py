import os
import unittest
import filecmp
import tempfile
import pkg_resources

import ninepatch


class TestNinepatch(unittest.TestCase):
    def test_ninepatch(self):
        # compare with the test image
        test_image = pkg_resources.resource_stream('ninepatch', 'data/9patch_test.png')
        original_image = pkg_resources.resource_stream('ninepatch', 'data/test_original_421_333.png')

        # copy package resourc into temp file
        original_image_temp_path = os.path.join(tempfile.gettempdir(), 'original_image_temp.png')
        with open(original_image_temp_path, 'wb') as original_image_temp:
            original_image_temp.write(original_image.read())

        scaled_image_path = tempfile.gettempdir() + os.sep + 'test_scaled_421_333.png'
        ninepatch_ = ninepatch.Ninepatch(test_image)
        ninepatch_.render(421, 333).save(scaled_image_path, format='PNG')

        self.assertTrue(filecmp.cmp(scaled_image_path, original_image_temp_path))

        os.remove(scaled_image_path)
        os.remove(original_image_temp_path)
