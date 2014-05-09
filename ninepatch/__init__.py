#!/usr/bin/env python

from PIL import Image


__all__ = ['Ninepatch', 'ScaleError']


class ScaleError(Exception):
    pass


class NinepatchError(Exception):
    pass

is_even = lambda value: value % 2 == 0


class Ninepatch(object):

    def __init__(self, filename):
        self.image = Image.open(filename)
        self.tiles = self.slice()

    def _chain(self, marks):
        for mark in marks:
            yield mark[0]
            yield mark[1] + 1  # shift end of black region to next tile

    def find_marks(self, image):
        '''find the cut marks'''
        pixels = image.load()

        marks = {'x': [], 'y': []}

        scalable_marker_color = (0, 0, 0, 255)

        for axis_i, axis in enumerate(('x', 'y')):
            start_mark = None
            end_mark = None

            coord = [0, 0]  # our handle to rotate the axes

            # iterate over the first pixels on that axis
            for i in range(image.size[axis_i]):
                coord[axis_i] = i  # select axis to search

                if pixels[tuple(coord)] == scalable_marker_color:
                    if start_mark:
                        end_mark = i
                    else:
                        start_mark = i

                else:
                    if end_mark:
                        marks[axis].append((start_mark, end_mark))
                        start_mark = None
                        end_mark = None

        return marks

    def slice(self):
        '''slice a 9 patch image'''
        marks = self.find_marks(self.image)

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
                self._chain(marks[axis])) + [image_size[axis]]

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
        return tiles

    @staticmethod
    def distributor(start):
        '''decrement start and yield 1 until it is exhausted, then yield 0'''
        n = start
        while True:
            yield 1 if n > 0 else 0
            n -= 1

    def render(self, width, height, filter=Image.ANTIALIAS):
        '''render the sliced tiles to a new scaled image'''

        scaled_image = Image.new('RGBA', (width, height), None)

        tile_count = {
            'x': len(self.tiles) - 1,
            'y': len(self.tiles[0]),
        }
        scaleable_tile_count = {
            'x': float(tile_count['x']) / 2,
            'y': float(tile_count['y']) / 2,
        }
        min_size = {
            'x': 0,
            'y': 0,
        }

        # all the even tiles are the ones that can be scaled

        # calculate min_size
        for x, column in enumerate(self.tiles):
            for y, tile in enumerate(column):
                if y == 0 and is_even(x):  # only on first row
                    min_size['x'] += tile.size[0]
                if x == 0 and is_even(y):  # only on first column
                    min_size['y'] += tile.size[1]

        # sanity check
        if width < min_size['x'] + scaleable_tile_count['x']:
            raise ScaleError('width cannot be smaller than %s' %
                             (min_size['x'] + scaleable_tile_count['x']))

        if height < min_size['y'] + scaleable_tile_count['y']:
            raise ScaleError('height cannot be smaller than %s' %
                             (min_size['y'] + scaleable_tile_count['y']))

        total_scale = {
            'x': width - min_size['x'],
            'y': height - min_size['y'],
        }
        tile_scale = {
            'x': int(total_scale['x'] / scaleable_tile_count['x']),
            'y': int(total_scale['y'] / scaleable_tile_count['y']),
        }
        # rounding differences
        extra = {
            'x': total_scale['x'] - (tile_scale['x'] *
                                     scaleable_tile_count['x']),
            'y': total_scale['y'] - (tile_scale['y'] *
                                     scaleable_tile_count['y']),
        }

        # distributes the pixels from the rounding differences until exhausted
        extra_x_distributor = Ninepatch.distributor(extra['x'])

        x_coord = 0
        y_coord = 0

        for x, column in enumerate(self.tiles):
            extra_x = 0 if is_even(x) else next(extra_x_distributor)
            extra_y_distributor = Ninepatch.distributor(extra['y'])

            for y, tile in enumerate(column):
                extra_y = 0 if is_even(y) else next(extra_y_distributor)

                if y == 0:
                    y_coord = 0  # reset y_coord

                if is_even(x) and is_even(y):
                    pass  # use tile as is
                elif is_even(x):  # scale y
                    tile = tile.resize(
                        (tile.size[0], tile_scale['y'] + extra_y), filter)
                elif is_even(y):  # scale x
                    tile = tile.resize(
                        (tile_scale['x'] + extra_x, tile.size[1]), filter)
                else:  # scale both
                    tile = tile.resize((
                        tile_scale['x'] + extra_x,
                        tile_scale['y'] + extra_y
                    ), filter)

                scaled_image.paste(tile, (x_coord, y_coord))

                y_coord += tile.size[1]

            x_coord += tile.size[0]

        return scaled_image
