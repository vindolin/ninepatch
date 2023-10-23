from io import BytesIO
import argparse
from importlib import resources
import importlib.metadata
import tkinter as tk
from ninepatch import Ninepatch, ScaleError
from PIL import ImageTk


def main():
    parser = argparse.ArgumentParser(description='Interactively scale Android style 9-patch images.')
    parser.add_argument('image_filename', nargs='?', default='DEMO_IMAGE')
    parser.add_argument('--version', action='version', version=importlib.metadata.version('ninepatch'))
    args = parser.parse_args()

    if args.image_filename == 'DEMO_IMAGE':
        ref = resources.files('ninepatch').joinpath('data/ninepatch_bubble.9.png')
        with ref.open('rb') as fp:
            args.image_filename = BytesIO(fp.read())

    ninepatch = Ninepatch(args.image_filename)

    img = None

    border = 20

    def resize(event):
        global img
        root.title(title)
        try:
            scaled_image = ninepatch.render(event.width - border * 2, event.height - border * 2)
            img = ImageTk.PhotoImage(scaled_image)
            canvas.delete("all")
            canvas.create_image(border, border, anchor=tk.NW, image=img)
            if ninepatch.content_area:
                canvas.create_rectangle((
                    border + ninepatch.content_area[0],
                    border + ninepatch.content_area[1],
                    event.width - border - ninepatch.content_area[2],
                    event.height - border - ninepatch.content_area[3],
                ), dash=(3, 6), outline='black')
        except ScaleError as e:
            root.title(e)

    title = '9-patch viewer'

    root = tk.Tk()
    root.title(title)

    root.bind('<Escape>', lambda e: root.destroy())

    canvas = tk.Canvas(root, width=int(ninepatch.image.size[0] * 1.5), height=int(ninepatch.image.size[1] * 1.5), bg='#BBB')
    canvas.pack(fill=tk.BOTH, expand=tk.YES)
    canvas.bind('<Configure>', resize)

    root.mainloop()


if __name__ == "__main__":
    main()
