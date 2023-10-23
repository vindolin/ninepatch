import os
from io import BytesIO
from pathlib import Path
import unittest
import filecmp
import tempfile

import ninepatch


class TestNinepatch(unittest.TestCase):
    def render_compare(self, test_image_name, good_test_result_image_name, width, height):
        # get the test image
        with open(Path(__file__).parent / 'data' / test_image_name, 'rb') as fp:
            test_image = BytesIO(fp.read())

        # get the result image to test against
        with open(Path(__file__).parent / 'data' / good_test_result_image_name, 'rb') as fp:
            good_result_image = BytesIO(fp.read())

        # copy package resource into temp file
        good_result_image_temp_path = os.path.join(tempfile.gettempdir(), 'good_result_image_temp.png')
        with open(good_result_image_temp_path, 'wb') as good_result_image_temp:
            good_result_image_temp.write(good_result_image.read())

        scaled_image_path = tempfile.gettempdir() + os.sep + 'test_scaled.png'
        ninepatch_ = ninepatch.Ninepatch(test_image)
        ninepatch_.render(width, height).save(scaled_image_path, format='PNG')

        self.assertTrue(filecmp.cmp(scaled_image_path, good_result_image_temp_path))

        os.remove(scaled_image_path)
        os.remove(good_result_image_temp_path)

    def test_ninepatch(self):
        self.render_compare('test_ninepatch.9.png', 'test_ninepatch_421x333_good_test_result.png', 421, 333)
