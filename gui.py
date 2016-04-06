from tkinter import *
import os
import shutil
from PIL import Image
import ex7


BASE_OUT_DIR = "images"
DEFAULT_NUM_FRAMES = 40
IMAGE_1_NAME = "im1.jpg"
IMAGE_2_NAME = "im2.jpg"
DEFAULT_MAX_X = 500
DEFAULT_MAX_Y = 350
TRIANGLE_VERTICES_NUM = 3
NUMBER_OF_ARGUMENTS = 7


def pixel(image, pos, color):
    """Place pixel at pos=(x,y) on image, with color=(r,g,b)."""
    r,g,b = color
    x,y = pos
    image.put("#%02x%02x%02x" % (r,g,b), (y, x))


def pil_image_from_lists(image_as_lists, max_x, max_y):
    """ Generate an Image obj from list of lists """
    #Support for two types of indexing:
    #First where the image is indexed image[y][x]
    #and second where the image is indexed image[x][y].
    #This allows to accept either a (max_x X max_y)
    #or (max_y X max_x) list of lists as the image.
    first_indexing = len(image_as_lists) == max_y
    im = Image.new("RGB", (max_x, max_y))
    for i in range(max_x):
        for j in range(max_y):
            if first_indexing:
                im.putpixel((i, j), image_as_lists[j][i])
            else:
                im.putpixel((i, j), image_as_lists[i][j])
    return im


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class TrianglesHandler (object):
    def __init__(self, handler1, handler2):
        self.handler1 = handler1
        self.handler2 = handler2

    def button_draw_triangles(self, event):
        print("draw triangles : ")

        self.handler1.draw_triangles()
        self.handler2.draw_triangles()
        matching = ex7.do_triangle_lists_match(self.handler1.coord_list,
                                                 self.handler2.coord_list)

        if not matching:
            print("Marked points are not in matching triangles.\
                Please mark the points again.")
            exit(1)


class MorphingHandler (object):
    def __init__(self, source_image, target_image, source_triangles_list,
            target_triangles_list, num_frames, base_out_dir, max_x, max_y):
        self.source_image = source_image
        self.target_image = target_image
        self.source_triangles_list = source_triangles_list
        self.target_triangles_list = target_triangles_list
        self.num_framse = num_frames
        self.base_out_dir = base_out_dir
        self.max_x = max_x
        self.max_y = max_y

    def button_show_morph(self, event):
        pixels_src = self.source_image.load()
        pixels_target = self.target_image.load()

        images_seq = ex7.create_sequence_of_images((self.max_x, self.max_y),
                                                   pixels_src, pixels_target,
            self.source_triangles_list, self.target_triangles_list,
            self.num_framse)

        # convert then save all images ; create dir to save them in
        if os.path.exists(self.base_out_dir):
            shutil.rmtree(self.base_out_dir)
        os.makedirs(self.base_out_dir)

        images = [pil_image_from_lists(im, self.max_x, self.max_y)
                  for im in images_seq]
        for idx, image in enumerate(images):
            # save image
            im_name = "image%02i.png"%idx 
            im_path = os.path.join(self.base_out_dir, im_name)
            image.save(im_path)
            print("Saving image :", im_path)


class ClickEventHandler (object):

    def __init__(self, img, canvas, max_x, max_y):
        self.img = img
        self.coord_list = []
        self.coord_ovals_list = []
        self.coord_ovals_indices_list = []
        self.lines = []
        self.triangles = []
        self.canvas = canvas
        self.max_x = max_x
        self.max_y = max_y

        # these points are default -- the corners of the image  
        self.save_click_coords(Point(0, 0))
        self.save_click_coords(Point(self.max_x, 0))
        self.save_click_coords(Point(self.max_x, self.max_y))
        self.save_click_coords(Point(0, self.max_y))

        
    def get_triangles(self):
        return self.triangles

    def save_click_coords(self, event):
        self.coord_list.append((event.x, event.y))
        print("add new point : ", (event.x, event.y))
        event.x = max(0, event.x-4)+4
        event.y = max(0, event.y-5)+5
        self.coord_ovals_list.append(self.canvas.create_oval(event.x-10,
            event.y-10, event.x+10, event.y+10, fill="white"))
        self.coord_ovals_indices_list.append(self.canvas.create_text
            (event.x, event.y, text=str(len(self.coord_ovals_list))))

    def button_click_delete_last_point(self, event):
        print("delete last point : ", self.coord_list.pop())
        self.canvas.delete(self.coord_ovals_list.pop())
        self.canvas.delete(self.coord_ovals_indices_list.pop())
        # remove all lines from the canvas
        for line in self.lines:
            self.canvas.delete(line)
        self.lines = list()
        self.triangles[:] = [] #have to keep the id because MorphHandler 
                               #keeps a ref. 

    def get_coords_list(self):
        return self.coord_list

    def draw_triangles(self):

        # first clear ovals that are now under the triangles
        for i in range(len(self.coord_list)):
            self.canvas.delete(self.coord_ovals_list.pop())
            self.canvas.delete(self.coord_ovals_indices_list.pop())

        # draw the triangles
        self.triangles[:] = []  # empty but keep same id!

        for triangle in ex7.create_triangles(self.get_coords_list()):
            self.triangles.append(triangle)
            for i in range(TRIANGLE_VERTICES_NUM):
                self.lines.append(self.canvas.create_line(triangle[i],
                    triangle[(i+1) % TRIANGLE_VERTICES_NUM], fill="blue",
                    width=5))

        # now put the ovals on again, over the triangles
        click_pnts = self.coord_list.copy()
        self.coord_list = []
        for pnt in click_pnts:
            self.save_click_coords(Point(pnt[0], pnt[1]))



def run_gui(image1, image2, num_frames, base_out_dir, max_x, max_y):

    root = Tk()
    #setting up a tkinter canvas with scrollbars
    frame = Frame(root, bd=2, relief=SUNKEN)
    canvas = Canvas(frame, bd=0)

    # image 1:
    img_name = image1
    img = Image.open(img_name)
    img = img.resize((max_x, max_y))
    pix = img.load()
    img_tk = PhotoImage(width=max_x,
                        height=max_y)
    for y in range(max_y):
        for x in range(max_x):
            pixel(img_tk, (y, x), pix[x, y])

    canvas.create_image(0,0,image=img_tk, anchor="nw")
    canvas.config(scrollregion=canvas.bbox(ALL))

    #function to be called when mouse is clicked

    handler1 = ClickEventHandler(img, canvas, max_x, max_y)
    #mouseclick event
    canvas.bind("<Button 1>", handler1.save_click_coords)

    b1 = Button(frame, text="delete last point")
    b1.bind("<Button 1>", handler1.button_click_delete_last_point)

    canvas.pack(fill=BOTH,expand=1)
    b1.place(x=520, y=0, width=100, height=30)
    frame.pack(fill=BOTH,expand=1)

    ######################################################################
    # image 2:
    img_name2 = image2
    #setting up a tkinter canvas with scrollbars
    frame2 = Frame(root, bd=2, relief=SUNKEN)
    canvas2 = Canvas(frame2, bd=0)

    #adding the image
    img2 = Image.open(img_name2)
    img2 = img2.resize((max_x, max_y))
    pix2 = img2.load()
    img_tk2 = PhotoImage(width=max_x,
                         height=max_y)
    for x in range(max_x):
        for y in range(max_y):
            pixel(img_tk2, (y, x), pix2[x, y])

    canvas2.create_image(0,0,image=img_tk2,anchor="nw")
    canvas2.config(scrollregion=canvas2.bbox(ALL))

    #function to be called when mouse is clicked
    handler2 = ClickEventHandler(img, canvas2, max_x, max_y)
    #mouseclick event
    canvas2.bind("<Button 1>", handler2.save_click_coords)

    b2 = Button(frame2, text="delete last point")
    b2.bind("<Button 1>", handler2.button_click_delete_last_point)

    triangles_handler = TrianglesHandler(handler1, handler2)

    # button for drawing triangles
    triangles_button = Button(frame2, text="draw triangles")
    triangles_button.bind("<Button 1>",
                          triangles_handler.button_draw_triangles)

    morph_handler = MorphingHandler(img, img2, handler1.get_triangles(),
        handler2.get_triangles(), num_frames, base_out_dir, max_x, max_y)

    morph_button = Button(frame2, text="morphing!")
    morph_button.bind("<Button 1>", morph_handler.button_show_morph)

    canvas2.pack(fill=BOTH, expand=1)
    b2.place(x=520, y=0, width=100, height=30)
    triangles_button.place(x=820, y=100, width=200, height=80)
    morph_button.place(x=820, y=180, width=200, height=80)
    frame2.pack(fill=BOTH, expand=1)

    #########################################################################

    root.mainloop()

if __name__ == "__main__":

    if 1 < len(sys.argv) < NUMBER_OF_ARGUMENTS:
        print("Usage: python3 gui.py <image_source> <image_target>\
         <num_frames> <out_dir> <max_x> <max_y>")
        exit(1)

    elif len(sys.argv) == NUMBER_OF_ARGUMENTS:
        image1, image2, num_frames, base_out_dir, max_x, max_y =\
            sys.argv[1:NUMBER_OF_ARGUMENTS]

    else:
        image1, image2, num_frames, base_out_dir, max_x, max_y = \
            IMAGE_1_NAME, IMAGE_2_NAME, DEFAULT_NUM_FRAMES, BASE_OUT_DIR,\
            DEFAULT_MAX_X, DEFAULT_MAX_Y

    run_gui(image1, image2, int(num_frames), base_out_dir,
            int(max_x), int(max_y))
