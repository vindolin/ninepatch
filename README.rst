Slice Android style 9-patch images into tiles and resize them into a scaled version
-----------------------------------------------------------------------------------

.. image:: https://travis-ci.org/vindolin/ninepatch.svg?branch=master
   :width: 90
   :alt: Travis CI
   :target: https://travis-ci.org/vindolin/ninepatch

see https://developer.android.com/tools/help/draw9patch.html

.. image:: https://raw.githubusercontent.com/vindolin/ninepatch/master/ninepatch/data/ninepatch_bubble.png
   :width: 320
   :alt: Example image
   :target: https://raw.githubusercontent.com/vindolin/ninepatch/master/ninepatch/data/ninepatch_bubble.png


Python usage
------------
.. code-block:: python


    from ninepatch import Ninepatch
    ninepatch = Ninepatch('9patch_test.png')
    print(ninepatch.fill_area)  # (left, top, right, bottom)
    scaled_image = ninepatch.render(500, 400) # creates a new PIL image

Command line usage
------------------
Your image must be a png image with a transparent background. The scale
guide color must be 100% opaque black.

open the scaled image in a viewer

::

    $ ninepatch 9patch_test.png 300 300

save the scaled image to a new file

::

    $ ninepatch 9patch_test.png 300 300 scaled.png

There's also a Tkinter viewer you can use to interactively preview your 9-patch images:

::

    $ ninepatch_viewer 9patch_test.png

tk8.5-dev has to be installed before installing with pip.

Ubuntu: sudo apt-get install tk8.5-dev

You can reinstall with: "pip install -I ninepatch" after fixing this.


Changelog
---------
0.1.9
  * parse the fill area
  * switched to setuptools
0.1.4
  * added Tkinter viewer

Notes
-----
You can see the module in action in the ninepatch\_actor.py from my
Clutter example project:
https://github.com/vindolin/Clutter-Python-examples

Issues
------
...

TODO
----
Validate Image and show user errors

