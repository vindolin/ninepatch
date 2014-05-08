#### Slice Android style 9-patch images into tiles and resize into a scaled version

see https://developer.android.com/tools/help/draw9patch.html

##### Python usage

    >>> import ninepatch
    >>> ninepatch = ninepatch.Ninepatch('9patch_test.png')
    >>> scaled_image = ninepatch.render(500, 400) # creates a new PIL image

##### Command line usage

open the scaled image in a viewer

    $ python ninepatch.py 9patch_test.png 300 300

save the scaled image to a new file

    $ ninepatch.py 9patch_test.png 300 300 scaled.png

