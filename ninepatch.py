from PIL import Image


class ScaleError(Exception):
    pass


def find_marks(image):
    '''find the cut marks'''
    pixels = image.load()

    marks = {'x': [], 'y': []}

    black = (0, 0, 0, 255)

    for axis_i, axis in enumerate(('x', 'y')):
        start_mark = None
        end_mark = None

        coord = [0, 0]
        for i in range(image.size[axis_i]):
            coord[axis_i] = i
            if pixels[tuple(coord)] == black:
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


def _chain(marks):
    for mark in marks:
        yield mark[0]
        yield mark[1] + 1


is_even = lambda value: value % 2 == 0


def slice_image(im):
    '''slice a 9 patch image'''
    marks = find_marks(im)

    slice_marks = {'x': [], 'y': []}
    image_size = {'x': im.size[0], 'y': im.size[1]}
    for axis in ('x', 'y'):
        slice_marks[axis] = [1] + list(_chain(marks[axis])) + [image_size[axis]]

    x_count = len(slice_marks['x']) - 1
    y_count = len(slice_marks['y']) - 1
    pieces = [[0 for y in range(y_count)] for x in range(x_count)]
    for x in range(x_count):
        for y in range(y_count):
            pieces[x][y] = im.crop(
                (
                    slice_marks['x'][x],
                    slice_marks['y'][y],
                    slice_marks['x'][x + 1],
                    slice_marks['y'][y + 1],
                )
            )
    return pieces


def _distribute(start):
    n = start
    while True:
        yield 1 if n > 0 else 0
        n -= 1


def scale_image(filename, width, height, filter=Image.ANTIALIAS):
    '''slices an image an scales the scalable pieces'''
    im = Image.open(filename)

    pieces = slice_image(im)
    scaled_im = Image.new('RGBA', (width, height), None)

    piece_count = {
        'x': len(pieces) - 1,
        'y': len(pieces[0]),
    }
    scaleable_piece_count = {
        'x': piece_count['x'] / 2,
        'y': piece_count['y'] / 2,
    }
    min_size = {
        'x': 0,
        'y': 0,
    }

    # calculate min_size
    for x, column in enumerate(pieces):
        for y, piece in enumerate(column):
            if y == 0 and is_even(x):  # only on first row
                min_size['x'] += piece.size[0]
            if x == 0 and is_even(y):  # only on first column
                min_size['y'] += piece.size[1]

    # sanity check
    if width < min_size['x'] + scaleable_piece_count['x']:
        raise ScaleError('width cannot be smaller than %s' % (min_size['x'] + scaleable_piece_count['x']))
    if height < min_size['y'] + scaleable_piece_count['y']:
        raise ScaleError('height cannot be smaller than %s' % (min_size['y'] + scaleable_piece_count['y']))

    total_scale = {
        'x': width - min_size['x'],
        'y': height - min_size['y'],
    }
    piece_scale = {
        'x': int(total_scale['x'] / scaleable_piece_count['x']),
        'y': int(total_scale['y'] / scaleable_piece_count['y']),
    }
    # rounding differences
    extra = {
        'x': total_scale['x'] - (piece_scale['x'] * scaleable_piece_count['x']),
        'y': total_scale['y'] - (piece_scale['y'] * scaleable_piece_count['y']),
    }

    x_coord = 0
    y_coord = 0

    extra_x_distributor = _distribute(extra['x'])

    for x, column in enumerate(pieces):
        extra_x = 0 if is_even(x) else extra_x_distributor.next()
        extra_y_distributor = _distribute(extra['y'])

        for y, piece in enumerate(column):
            extra_y = 0 if is_even(y) else extra_y_distributor.next()

            if y == 0:
                y_coord = 0
            if is_even(x) and is_even(y):
                pass  # use piece as is

            elif is_even(x):  # scale y
                piece = piece.resize((piece.size[0], piece_scale['y'] + extra_y), filter)
            elif is_even(y):  # scale x
                piece = piece.resize((piece_scale['x'] + extra_x, piece.size[1]), filter)
            else:  # scale both
                piece = piece.resize((piece_scale['x'] + extra_x, piece_scale['y'] + extra_y), filter)

            scaled_im.paste(piece, (x_coord, y_coord))

            y_coord += piece.size[1]

        x_coord += piece.size[0]

    return scaled_im

if __name__ == '__main__':
    scale_image('9patch_test.png', 506, 601).show()
