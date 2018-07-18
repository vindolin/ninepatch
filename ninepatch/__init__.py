#!/usr/bin/env python
from PIL import Image
from collections import namedtuple
import os
import re

__all__ = ['Ninepatch', 'ScaleError']

content_area = namedtuple('content_area', ['left', 'top', 'right', 'bottom'])


class ScaleError(Exception):
    pass


class NinepatchError(Exception):
    pass


def is_even(value):
    return value % 2 == 0


class Ninepatch(object):

    slice_cache = {}
    render_cache = {}

    @classmethod
    def get_cache_size(cls):
        # return sys.getsizeof(cls.slice_cache), sys.getsizeof(cls.render_cache)
        return cls.render_cache

    def __init__(self, filename, cache=False):
        self.filename = filename

        if filename in self.slice_cache:
            self.image_size = self.slice_cache[filename]['image_size']
            self.slice_data = self.slice_cache[filename]['slice_data']
            self.marks = self.slice_cache[filename]['marks']
        else:
            self.image = Image.open(filename)
            self.image_size = self.image.size
            self.marks = self.find_marks(self.image)
            self.slice_data = self.slice()

            if cache:
                self.slice_cache[filename] = {
                    'image_size': self.image_size,
                    'slice_data': self.slice_data,
                    'marks': self.marks,
                }

    @property
    def min_scale_size(self):
        return self.slice_data['min_scale_size']

    @property
    def content_area(self):
        if self.marks['fill']['x'] == [] or self.marks['fill']['y'] == []:
            return None

        return content_area(
            self.marks['fill']['x'][0],
            self.marks['fill']['y'][0],
            self.image.size[0] - self.marks['fill']['x'][1],
            self.image.size[1] - self.marks['fill']['y'][1],
        )

    @staticmethod
    def _chain(marks):
        for mark in marks:
            yield mark[0]
            yield mark[1] + 1  # shift end of black region to next tile

    @staticmethod
    def find_marks(image):
        """ find the cut marks

        :param image: a PIL Image
        :return:
        :rtype: dict
        """
        pixels = image.load()

        scale_marks = {'x': [], 'y': []}
        fill_marks = {'x': [], 'y': []}
        axes = {'x': 0, 'y': 1}

        marker_color = (0, 0, 0, 255)

        for axis in axes.keys():
            start_scale_mark = end_scale_mark = None
            start_fill_mark = end_fill_mark = None

            scale_coord = [0, 0]  # our handle to rotate the axes
            fill_coord = [0, 0]

            # last pixel on that axis
            fill_coord[axes[axis] - 1] = image.size[not axes[axis]] - 1

            # iterate over the first pixels on that axis
            for i in range(image.size[axes[axis]]):
                scale_coord[axes[axis]] = i  # select axis to search
                fill_coord[axes[axis]] = i

                scale_pixel = pixels[tuple(scale_coord)]
                fill_pixel = pixels[tuple(fill_coord)]

                # scale marks
                if scale_pixel == marker_color:
                    if not start_scale_mark:
                        start_scale_mark = i
                    end_scale_mark = i

                else:
                    if start_scale_mark:
                        scale_marks[axis].append(
                            (start_scale_mark, end_scale_mark))
                        start_scale_mark = end_scale_mark = None

                # fill marks
                if fill_pixel == marker_color:
                    if not start_fill_mark:
                        start_fill_mark = i
                    end_fill_mark = i
                else:
                    if start_fill_mark:
                        fill_marks[axis] = (start_fill_mark, end_fill_mark - 1)

        return {
            'scale': scale_marks,
            'fill': fill_marks,
        }

    def slice(self):
        """ slice a 9 patch image
        """
        slice_data = {}

        slice_marks = {
            'x': [],
            'y': []
        }
        image_size = {
            'x': self.image.size[0],
            'y': self.image.size[1]
        }
        for axis in ('x', 'y'):
            slice_marks[axis] = [1] + list(
                self._chain(self.marks['scale'][axis])) + [image_size[axis] - 1]

        counts = {
            'x': len(slice_marks['x']) - 1,
            'y': len(slice_marks['y']) - 1,
        }

        tiles = [[0 for y in range(counts['y'])] for x in range(counts['x'])]
        for x in range(counts['x']):
            for y in range(counts['y']):

                # cut our tile region
                tiles[x][y] = self.image.crop((
                    slice_marks['x'][x],
                    slice_marks['y'][y],
                    slice_marks['x'][x + 1],
                    slice_marks['y'][y + 1],
                ))

        slice_data['tiles'] = tiles

        slice_data['tile_count'] = {
            'x': len(tiles) - 1,
            'y': len(tiles[0]) - 1,
        }
        slice_data['scaleable_tile_count'] = {
            'x': float(slice_data['tile_count']['x']) / 2,
            'y': float(slice_data['tile_count']['y']) / 2,
        }
        slice_data['fixed_tile_size'] = {
            'x': 0,
            'y': 0,
        }

        # calculate fixed_tile_size
        for x, column in enumerate(tiles):
            for y, tile in enumerate(column):
                if y == 0 and is_even(x):  # only on first row
                    slice_data['fixed_tile_size']['x'] += tile.size[0]
                if x == 0 and is_even(y):  # only on first column
                    slice_data['fixed_tile_size']['y'] += tile.size[1]

        # add 1 pixel for every scalable region
        slice_data['min_scale_size'] = {
            'x': slice_data['fixed_tile_size']['x'] + slice_data['scaleable_tile_count']['x'],
            'y': slice_data['fixed_tile_size']['y'] + slice_data['scaleable_tile_count']['y'],
        }

        return slice_data

    @staticmethod
    def _distributor(start):
        """ decrement start and yield 1 until it is exhausted, then yield 0
        """
        n = start
        while True:
            yield 1 if n > 0 else 0
            n -= 1

    @staticmethod
    def _tile_scale(total_scale, scalable_tile_count):
        if scalable_tile_count > 0:
            return int(total_scale / scalable_tile_count)
        else:
            return 0

    def render_fit(self, width, height):
        """ expands so that a content area of width/height can fit

        :return: PIL Image
        """
        ca = self.content_area

        min_width = int(self.slice_data['min_scale_size']['x'])
        min_height = int(self.slice_data['min_scale_size']['y'])

        # creates a new PIL image
        return self.render(max(width + ca.left + ca.right, min_width),
                           max(height + ca.top + ca.bottom, min_height))

    def render_wrap(self, image):
        """ paste image in content area
        :param image: a PIL image to insert in the content area
        :return: PIL Image
        """
        scaled_image = self.render_fit(*image.size)
        ca = self.content_area
        scaled_image.paste(image, (ca.left, ca.top), image)
        return scaled_image

    def render(self, width, height, img_filter=Image.ANTIALIAS, cache=False):
        """ render the sliced tiles to a new scaled image
        """
        cache_hash = '{} {} {}'.format(width, height, self.filename)
        if cache and cache_hash in self.render_cache:
            scaled_image = self.render_cache[cache_hash]
        else:
            scaled_image = Image.new('RGBA', (width, height), None)

            # all the even tiles are the ones that can be scaled

            # raise error when undersized
            if width < self.slice_data['min_scale_size']['x']:
                raise ScaleError('width cannot be smaller than %i'
                                 % self.slice_data['min_scale_size']['x'])

            if height < self.slice_data['min_scale_size']['y']:
                raise ScaleError('height cannot be smaller than %i'
                                 % self.slice_data['min_scale_size']['y'])

            total_scale = {
                'x': width - self.slice_data['fixed_tile_size']['x'],
                'y': height - self.slice_data['fixed_tile_size']['y'],
            }
            tile_scale = {
                'x': self._tile_scale(total_scale['x'], self.slice_data['scaleable_tile_count']['x']),
                'y': self._tile_scale(total_scale['y'], self.slice_data['scaleable_tile_count']['y']),
            }
            # rounding differences
            extra = {
                'x': total_scale['x'] - (tile_scale['x'] * self.slice_data['scaleable_tile_count']['x']),
                'y': total_scale['y'] - (tile_scale['y'] * self.slice_data['scaleable_tile_count']['y']),
            }

            # distributes the pixels from the rounding differences until exhausted
            extra_x_distributor = self._distributor(extra['x'])

            x_coord = y_coord = 0

            for x, column in enumerate(self.slice_data['tiles']):
                extra_x = 0 if is_even(x) else next(extra_x_distributor)
                extra_y_distributor = self._distributor(extra['y'])

                for y, tile in enumerate(column):
                    extra_y = 0 if is_even(y) else next(extra_y_distributor)

                    if y == 0:
                        y_coord = 0  # reset y_coord

                    if is_even(x) and is_even(y):
                        pass  # use tile as is
                    elif is_even(x):  # scale y
                        tile = tile.resize((tile.size[0], tile_scale['y'] + extra_y), img_filter)
                    elif is_even(y):  # scale x
                        tile = tile.resize((tile_scale['x'] + extra_x, tile.size[1]), img_filter)
                    else:  # scale both
                        tile = tile.resize((
                            tile_scale['x'] + extra_x,
                            tile_scale['y'] + extra_y
                        ), img_filter)

                    scaled_image.paste(tile, (x_coord, y_coord))

                    y_coord += tile.size[1]

                x_coord += tile.size[0]

            if cache:
                self.render_cache[cache_hash] = scaled_image

        return scaled_image

    @staticmethod
    def _column(image, pixels, x):
        return [pixels[(x, y)] for y in range(image.size[1])]

    @staticmethod
    def _row(image, pixels, y):
        return [pixels[(x, y)] for x in range(image.size[0])]

    def compress_tile(self, tile):
        """ look if pixels are repeated on one or two axes and compress the tile
        """
        pixels = tile.load()

        x_compress = True
        y_compress = True

        first_column = self._column(tile, pixels, 0)
        first_row = self._column(tile, pixels, 0)

        for x in range(tile.size[0]):
            pixel_column = self._column(tile, pixels, x)
            if pixel_column != first_column:
                x_compress = False

        for y in range(tile.size[1]):
            pixel_row = self._row(tile, pixels, y)
            if pixel_row != first_row:
                y_compress = False

        if x_compress or y_compress:
            width = 1 if x_compress else tile.size[0]
            height = 1 if y_compress else tile.size[1]

            compressed_tile = Image.new('RGBA', (width, height), None)
            compressed_tile.paste(tile.crop((0, 0, width, height)))

            return compressed_tile

        return tile

    def export_slices(self, path):
        """ export slices as PNG images into a directory
        """
        file_prefix = os.path.basename(self.filename)
        file_prefix = re.match('(.*)\.9\.png', file_prefix).groups()[0]
        for x, column in enumerate(self.slice_data['tiles']):
            for y, tile in enumerate(column):
                tile = self.compress_tile(tile)
                slice_image = Image.new('RGBA', (tile.size[0], tile.size[1]), None)
                slice_image.paste(tile)
                slice_image.save('{}/{}_{}_{}.png'.format(path, file_prefix, x, y))
