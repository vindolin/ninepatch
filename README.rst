Slice Android style 9-patch images, resize and interactively preview them.
--------------------------------------------------------------------------

.. image:: https://travis-ci.org/vindolin/ninepatch.svg?branch=master
   :width: 90
   :alt: Travis CI
   :target: https://travis-ci.org/vindolin/ninepatch

See https://developer.android.com/tools/help/draw9patch.html for a 9-patch description.

.. image:: https://raw.githubusercontent.com/vindolin/ninepatch/master/ninepatch/data/ninepatch_bubble.9.png
   :width: 320
   :alt: Example image
   :target: https://raw.githubusercontent.com/vindolin/ninepatch/master/ninepatch/data/ninepatch_bubble.9.png

Installation
------------

If you want to use the interactive viewer read the additional installation notes under "Interactive viewer".

::

    $ pip install ninepatch

Python usage
------------
.. code-block:: python


    from ninepatch import Ninepatch
    ninepatch = Ninepatch('ninepatch_bubble.9.png')
    print(ninepatch.content_area)  # content_area(left=23, top=20, right=27, bottom=59)

    # render the image to a specific size
    scaled_image = ninepatch.render(500, 400) # creates a new PIL image

    # render the image so it's content area fits (width, height)
    image_fit = ninepatch.render_fit(300, 200)

    # render the image so it wraps another PIL image
    image_to_wrap = Image.open('dmt.png')
    wrapped_image = ninepatch.render_wrap(image_to_wrap)


Command line usage
------------------
Your image must be a PNG image with a transparent background.
The scale and fill guide color must be 100% opaque black.

Scale and open image in a viewer (PIL image.show()):

::

    $ ninepatch render ninepatch_bubble.9.png 300 300

Save the scaled image to a new file:

::

    $ ninepatch render ninepatch_bubble.9.png 300 300 scaled.png

.. image:: https://raw.githubusercontent.com/vindolin/ninepatch/master/ninepatch/data/ninepatch_bubble_300x300.png


Render an image to fit a given width and height

::

    $ ninepatch fit ninepatch_bubble.9.png 250 250 scaled.png

Render an image to include another image

::

    $ ninepatch wrap ninepatch_bubble.9.png image_to_wrap.png wrapped.png

.. image:: https://raw.githubusercontent.com/vindolin/ninepatch/master/ninepatch/data/wrapped.png

Slice the 9patch into tiles:

::

    $ ninepatch slice ninepatch_bubble.9.png ./outputdir

.. image:: https://raw.githubusercontent.com/vindolin/ninepatch/master/ninepatch/data/slice_export.png

Interactive viewer
------------------


.. image:: https://raw.githubusercontent.com/vindolin/ninepatch/master/ninepatch/data/ninepatch_viewer_screenshot.png
   :width: 419
   :alt: ninepatch viewer screenshot
   :target: https://raw.githubusercontent.com/vindolin/ninepatch/master/ninepatch/data/ninepatch_viewer_screenshot.png


Interactively resize and preview an image in a Tkinter viewer:

::

    $ ninepatch_viewer ninepatch_bubble.9.png

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
0.1.20
  * new commands `fit` and `wrap` courtesy of Nicolas Laurance
0.1.19
  * fixed error in caching
0.1.18
  * optional caching for slice() and render()
0.1.17
  * new method export_slices()
  * changed command line parameters (render/slice)
...
