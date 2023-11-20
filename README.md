Slice Android style 9-patch images, resize and preview them interactively.
==========================================================================

See <https://developer.android.com/tools/help/draw9patch.html> for a
9-patch description.

[![Example image](https://raw.githubusercontent.com/vindolin/ninepatch/master/src/ninepatch/data/ninepatch_bubble.9.png)](https://raw.githubusercontent.com/vindolin/ninepatch/master/src/ninepatch/data/ninepatch_bubble.9.png)

Installation
============

If you want to use the interactive viewer read the additional
installation notes under "Interactive viewer".

    $ pip install ninepatch

Python usage
============

``` {.sourceCode .python}
from ninepatch import Ninepatch
ninepatch = Ninepatch('ninepatch_bubble.9.png')
print(ninepatch.content_area)  # content_area(left=23, top=20, right=27, bottom=59)

# render the image to a specific size
scaled_image = ninepatch.render(500, 400) # creates a new PIL image

# render the image so it's content area fits (width, height)
image_fit = ninepatch.render_fit(300, 200)

# render the image so it wraps another PIL image
image_to_wrap = Image.open('image_to_wrap.png')
wrapped_image = ninepatch.render_wrap(image_to_wrap)
```

Command line usage
==================

Your image must be a PNG image with a transparent background. The scale
and fill guide color must be 100% opaque black.

Scale and open image in a viewer (PIL image.show()):

    $ ninepatch render ninepatch_bubble.9.png 300 300

Save the scaled image to a new file:

    $ ninepatch render ninepatch_bubble.9.png 300 300 scaled.png

![image](https://raw.githubusercontent.com/vindolin/ninepatch/master/src/ninepatch/data/ninepatch_bubble_300x300.png)

Render an image so it's content area fits a given width and height

    $ ninepatch fit ninepatch_bubble.9.png 150 150 fit.png

![image](https://raw.githubusercontent.com/vindolin/ninepatch/master/src/ninepatch/data/fit.png)

Render an image to include another image

    $ ninepatch wrap ninepatch_bubble.9.png image_to_wrap.png wrapped.png

![image](https://raw.githubusercontent.com/vindolin/ninepatch/master/src/ninepatch/data/wrapped.png)

Slice the 9patch into tiles:

    $ ninepatch slice ninepatch_bubble.9.png ./outputdir

![image](https://raw.githubusercontent.com/vindolin/ninepatch/master/src/ninepatch/data/slice_export.png)

Slice the 9patch and return a JSON reprensentation of the slicing data:

    $ ninepatch info ninepatch_bubble.9.png

```JSON
{
    "marks": {
        "fill": {
            "x": [
                23,
                231
            ],
            "y": [
                20,
                82
            ]
        },
        "scale": {
            "x": [
                [
                    49,
                    49
                ],
                [
                    89,
                    196
                ]
            ],
            "y": [
                [
                    42,
                    63
                ]
            ]
        }
    },
    "size": [
        258,
        141
    ]
}
```

Interactive viewer
==================

[![ninepatch viewer screenshot](https://raw.githubusercontent.com/vindolin/ninepatch/master/src/ninepatch/data/ninepatch_viewer_screenshot.png)](https://raw.githubusercontent.com/vindolin/ninepatch/master/src/ninepatch/data/ninepatch_viewer_screenshot.png)

Interactively resize and preview an image in a Tkinter viewer:

    $ ninepatch-viewer ninepatch_bubble.9.png

    or just:

    $ ninepatch-viewer

    without arguments to see the demo image

If you want to use the viewer then python-pil.imagetk has to be
installed.

On Ubuntu do:

    $ sudo apt-get install python-pil.imagetk

If you want to install into a virtualenv, pip needs the following
packages to compile PIL with Tkinter support:

    $  sudo apt-get install python-tk tk8.6-dev

(You can trigger a recompile of PIL with: "pip install -I ninepatch")

Changelog
=========
0.2.0

:   -   allow 0-size tiles, now works with pillow >=10.0.0

0.1.22

:   -   fixed error that prevented the ninepatch_viewer to work

0.1.21

:   -   fixed bug in wrap()

0.1.20

:   -   new commands fit and wrap courtesy of Nicolas Laurance

0.1.19

:   -   fixed error in caching

0.1.18

:   -   optional caching for slice() and render()

0.1.17

:   -   new method export\_slices()
    -   changed command line parameters (render/slice)

...
