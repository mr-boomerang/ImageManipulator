from tkinter import *
from tkinter.colorchooser import askcolor
from PIL import ImageTk, Image
import cv2

class Paint(object):

    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'

    def __init__(self):
        self.root = Tk()

        self.pen_button = Button(self.root, text='pen', command=self.use_pen)
        self.pen_button.grid(row=0, column=0)

        self.brush_button = Button(self.root, text='brush', command=self.use_brush)
        self.brush_button.grid(row=0, column=1)

        self.color_button = Button(self.root, text='color', command=self.choose_color)
        self.color_button.grid(row=0, column=2)

        self.eraser_button = Button(self.root, text='eraser', command=self.use_eraser)
        self.eraser_button.grid(row=0, column=3)

        self.choose_size_button = Scale(self.root, from_=1, to=10, orient=HORIZONTAL)
        self.choose_size_button.grid(row=0, column=4)

        self.GaussianBlur_button = Button(self.root, text='Gaussian Blur', command=self.gaussian_blur)
        self.GaussianBlur_button.grid(row=2, column=0)

        self.AveragingBlur_button = Button(self.root, text='Averaging Blur', command=self.average_blur)
        self.AveragingBlur_button.grid(row=2, column=1)

        self.MedianBlur_button = Button(self.root, text='Median Blur', command=self.median_blur)
        self.MedianBlur_button.grid(row=2, column=2)

        self.BilateralFiltering_button = Button(self.root, text='Bilateral Filtering', command=self.bilateral_filtering)
        self.BilateralFiltering_button.grid(row=2, column=3)

        self.SimpleThresholding_button = Button(self.root, text='Simple Thresholding', command=self.simple_thresholding)
        self.SimpleThresholding_button.grid(row=3, column=0)

        self.AdaptiveMeanThresholdin_button = Button(self.root, text='Adaptive Mean', command=self.adaptive_mean)
        self.AdaptiveMeanThresholdin_button.grid(row=3, column=1)

        self.AdaptiveGaussianThresholdin_button = Button(self.root, text='Adaptive Gaussian', command=self.adaptive_gaussian)
        self.AdaptiveGaussianThresholdin_button.grid(row=3, column=2)

        self.OtsuThresholding_button = Button(self.root, text='Otsu Thresholding', command=self.otsu_thresholding)
        self.OtsuThresholding_button.grid(row=3, column=3)

        self.Grayscale_button = Button(self.root, text='GrayScale', command=self.grayscale)
        self.Grayscale_button.grid(row=4, columnspan=4)

        self.img = cv2.cvtColor(cv2.imread("cameraman.jpg"), cv2.COLOR_BGR2RGB)
        scale_percent = 60 # percent of original size
        self.img = cv2.resize(self.img, (500,500), interpolation = cv2.INTER_AREA)

        self.origimg = self.img
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.img))
        
        self.c = Canvas(self.root, bg='white', width=500, height = 500 )
        self.c.grid(row=1, columnspan=5)


        # self.c.image = ImageTk.PhotoImage(self.img)
        self.c.create_image(0,0, image = self.photo, anchor = NW)

        self.setup()
        self.root.mainloop()

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = self.pen_button
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

    def use_pen(self):
        self.activate_button(self.pen_button)

    def use_brush(self):
        self.activate_button(self.brush_button)

    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]

    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def paint(self, event):
        self.line_width = self.choose_size_button.get()
        paint_color = 'white' if self.eraser_on else self.color
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y

    def gaussian_blur(self):
        self.img = cv2.GaussianBlur(self.img, (5, 5),0)
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.img))
        self.c.create_image(0, 0, image=self.photo, anchor=NW)

    def average_blur(self):
        self.img = cv2.blur(self.img, (5,5))
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.img))
        self.c.create_image(0, 0, image=self.photo, anchor=NW)

    def median_blur(self):
        self.img = cv2.medianBlur(self.img, 5)
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.img))
        self.c.create_image(0, 0, image=self.photo, anchor=NW)

    def bilateral_filtering(self):
        self.img = cv2.bilateralFilter(self.img,9,75,75)
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.img))
        self.c.create_image(0, 0, image=self.photo, anchor=NW)

    def simple_thresholding(self):
        ret,self.img = cv2.threshold(self.img,127,255,cv2.THRESH_BINARY)
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.img))
        self.c.create_image(0, 0, image=self.photo, anchor=NW)
    
    def adaptive_mean(self):
        self.img = cv2.adaptiveThreshold(self.img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.img))
        self.c.create_image(0, 0, image=self.photo, anchor=NW)
    
    def adaptive_gaussian(self):
        self.img = cv2.adaptiveThreshold(self.img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.img))
        self.c.create_image(0, 0, image=self.photo, anchor=NW)

    def otsu_thresholding(self):
        ret,self.img = cv2.threshold(self.img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.img))
        self.c.create_image(0, 0, image=self.photo, anchor=NW)
        
    def grayscale(self):
        self.img = cv2.cvtColor(self.img, cv2.COLOR_RGB2GRAY)
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.img))
        self.c.create_image(0, 0, image=self.photo, anchor=NW)

    def reset(self, event):
        self.old_x, self.old_y = None, None



if __name__ == '__main__':
    Paint()
