Slice Android style 9-patch images into tiles, resize and interactively preview them.
-------------------------------------------------------------------------------------

.. image:: https://travis-ci.org/vindolin/ninepatch.svg?branch=master
   :width: 90
   :alt: Travis CI
   :target: https://travis-ci.org/vindolin/ninepatch

See https://developer.android.com/tools/help/draw9patch.html for a 9-patch description.

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
Your image must be a PNG image with a transparent background.
The scale and fill guide color must be 100% opaque black.

Scale and open image in a viewer (PIL image.show()):

::

    $ ninepatch 9patch_test.png 300 300

Save the scaled image to a new file:

::

    $ ninepatch 9patch_test.png 300 300 scaled.png


Interactively resize and preview an image in a Tkinter viewer:

::

    $ ninepatch_viewer 9patch_test.png

    or just:

    $ ninepatch_viewer

    without arguments to see the demo image


If you want to use the viewer then python-pil.imagetk has to be installed.

On Ubuntu do:

::

  $ sudo apt-get install python-pil.imagetk


If you want to install into a virtualenv, pip needs the following packages to compile PIL with Tkinter support:

::

   $  sudo apt-get install python-tk tk8.6-dev

(You can trigger a recompile of PIL with: "pip install -I ninepatch")


Changelog
---------
0.1.10
  * missing guides are now handled properly
0.1.9
  * parse the fill area
  * switched to setuptools
0.1.4
  * added Tkinter viewer

Notes
-----
I wrote this tool for the ninepatch\_actor.py in my Clutter example project:
https://github.com/vindolin/Clutter-Python-examples

Issues
------
...

TODO
----
...
