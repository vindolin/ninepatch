#### Slice Android style 9-patch images into tiles and resize them into a scaled version

see https://developer.android.com/tools/help/draw9patch.html

##### Python usage

    >>> from ninepatch import Ninepatch
    >>> ninepatch = Ninepatch('9patch_test.png')
    >>> scaled_image = ninepatch.render(500, 400) # creates a new PIL image

##### Command line usage

open the scaled image in a viewer

    $ ninepatch.py 9patch_test.png 300 300

save the scaled image to a new file

    $ ninepatch.py 9patch_test.png 300 300 scaled.png

##### Notes

You can see the module in action in the ninepatch_actor.py from my Clutter example project: https://github.com/vindolin/Clutter-Python-examples

##### Issues

Your image must be a png image with a transparent background.
<<<<<<< HEAD
The scale guide color must be 100% opaque black.

See the example/unittest image:

![alt text](https://raw.githubusercontent.com/vindolin/Clutter-Python-examples/master/ninepatch/9patch_test.png "Example image")

Only the scalable area is used, fill area is ignored.

=======

Only the scalable area is used, fill area is ignored.


>>>>>>> d474ac61afc086e2fb137728143e9752803bb0dd
##### TODO

Add setup.py

Unittest

