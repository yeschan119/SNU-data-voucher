from xml.etree.ElementTree import Element, dump, ElementTree
import xml.etree.ElementTree as ET
import cv2
import numpy as np
from matplotlib import pyplot as plt
import tkinter as tk
from tkinter import Frame, filedialog, messagebox
from tkinter.filedialog import askopenfilenames
from PIL import Image
from PIL import ImageTk


root = tk.Tk()


class Polygon_Proj:
    def __init__(self, root):
        self.root = object()
        self.data = object()
        self.window = root
        self.label1 = object()
        self.label2 = object()
        self.raw_img_list = {}
        self.fine_img_list = {}
        self.coarse_img_list = {}
        self.masked_fine_img = {}
        self.masked_coarse_img = {}
        self.index = 0
        self.annotation_color = []
        self.coarse_figure = 0.025

    def upload_img(self):
        image_formats = [("JPEG", "*.jpg")]
        file_path_list = askopenfilenames(
            filetypes=image_formats, initialdir="/", title='Please select a picture to analyze')

        for file in file_path_list:
            img_name = file.split('/')
            img_name = img_name.pop()
            img = cv2.imread(file, cv2.IMREAD_COLOR)
            self.raw_img_list[img_name] = img
        tk.messagebox.showinfo('image upload', 'image uploaded!')

    def upload_xml(self):
        self.data = filedialog.askopenfilename(
            initialdir="/", title="Select file", filetypes=(("xml files", "*.xml"), ("all files", "*.*")))
        doc = ET.parse(self.data)
        self.root = doc.getroot()
        for labels in self.root[1][0]:
            if labels.tag == 'labels':
                label_name = [label[0].text for label in labels]
                break
        print('labels :', str(label_name).replace(",", ''))
        tk.messagebox.showinfo('xml upload', 'xml uploaded!')

    def extract_points(self, sub_root, img_name):
        point_list = []
        for points in sub_root:
            polygon = points.attrib
            point_list.append(polygon['points'])
        self.draw_annotation(1, img_name, point_list)
        self.draw_annotation(2, img_name, point_list)

    def xml_warning(self):
        if messagebox.askokcancel("warning!", "wrong xml file"):
            pass
        else:
            self.window.destroy()

    def parse_tree(self):
        for sub_root in self.root:
            if sub_root.tag == 'image':
                if sub_root.attrib['name'] in self.raw_img_list.keys():
                    self.extract_points(sub_root, sub_root.attrib['name'])
                else:
                    self.xml_warning()
                    break
        tk.messagebox.showinfo('annotation', 'annotation finished!')

    def show_cv(self, img, cv2):
        img = cv2.resize(img, dsize=(0, 0), fx=0.3, fy=0.3,
                         interpolation=cv2.INTER_LINEAR)
        cv2.imshow('image', img)
        k = cv2.waitKey()
        cv2.destroyAllWindows()

    def do_coarse(self, pts):
        x = [p[0] for p in pts]
        y = [p[1] for p in pts]
        meanx = np.mean(x)
        maxx = np.max(x)
        minx = np.min(x)
        meany = np.mean(y)
        maxy = np.max(y)
        miny = np.min(y)
        for p in pts:
            if p[0] > meanx and p[0] != maxx:
                p[0] = p[0] * (1 - self.coarse_figure)
            elif p[0] < meanx and p[0] != minx:
                p[0] = p[0] * (1 + self.coarse_figure)
            if p[1] > meany and p[1] != maxy:
                p[1] = p[1] * (1 - self.coarse_figure)
            elif p[1] < meany and p[1] != miny:
                p[1] = p[1] * (1 + self.coarse_figure)
        return pts

    def draw_annotation(self, option, img_name, point_list):
        pts = []
        if option == 1:
            self.annotation_color = []
            img1 = self.raw_img_list[img_name].copy()
            masked_img = self.raw_img_list[img_name].copy()
            for points in point_list:
                points = points.split(';')
                for point in points:
                    temp = point.split(',')
                    pts.append(list(map(float, temp)))
                pts = np.array(pts, np.int32)
                pts = pts.reshape((-1, 1, 2))
                color = list(map(int, (np.random.randint(256, size=3))))
                self.annotation_color.append(color)
                masked_img = cv2.fillPoly(masked_img, [pts], color)
                img1 = cv2.polylines(img1, [pts], True, color, 3)
                pts = []
            img1 = cv2.resize(img1, dsize=(0, 0), fx=0.35,
                              fy=0.35, interpolation=cv2.INTER_LINEAR)
            masked_img = cv2.resize(masked_img, dsize=(
                0, 0), fx=0.35, fy=0.35, interpolation=cv2.INTER_LINEAR)
            masked_img = cv2.addWeighted(masked_img, 0.6, img1, 1, 0)
            self.fine_img_list[img_name] = img1
            self.masked_fine_img[img_name] = masked_img
        else:
            img2 = self.raw_img_list[img_name].copy()
            masked_img = self.raw_img_list[img_name].copy()
            for i, points in zip(range(len(point_list)), point_list):
                points = points.split(';')
                for point in points:
                    temp = point.split(',')
                    pts.append(list(map(float, temp)))
                pts = self.do_coarse(pts)
                pts = np.array(pts, np.float32)
                pts = pts.astype(int)
                pts = pts.reshape((-1, 1, 2))
                masked_img = cv2.fillPoly(
                    masked_img, [pts], self.annotation_color[i])
                img2 = cv2.polylines(
                    img2, [pts], True, self.annotation_color[i], 3)
                pts = []
            img2 = cv2.resize(img2, dsize=(0, 0), fx=0.35,
                              fy=0.35, interpolation=cv2.INTER_LINEAR)
            masked_img = cv2.resize(masked_img, dsize=(
                0, 0), fx=0.35, fy=0.35, interpolation=cv2.INTER_LINEAR)
            masked_img = cv2.addWeighted(masked_img, 0.6, img2, 1, 0)
            self.coarse_img_list[img_name] = img2
            self.masked_coarse_img[img_name] = masked_img

    def masked_img(self):
        keys = list(self.fine_img_list.keys())
        img1 = cv2.cvtColor(
            self.masked_fine_img[keys[self.index]], cv2.COLOR_BGR2RGB)
        img1 = Image.fromarray(img1)
        img2 = cv2.cvtColor(
            self.masked_coarse_img[keys[self.index]], cv2.COLOR_BGR2RGB)
        img2 = Image.fromarray(img2)

        imgtk1 = ImageTk.PhotoImage(image=img1)
        imgtk2 = ImageTk.PhotoImage(image=img2)

        self.label1.config(image=imgtk1)
        self.label1.image = imgtk1

        self.label2.config(image=imgtk2)
        self.label2.image = imgtk2

    def next_img(self):
        if self.index >= len(self.raw_img_list):
            self.prev_next_warning(2)
        else:
            self.index += 1
            keys = list(self.fine_img_list.keys())
            img1 = cv2.cvtColor(
                self.fine_img_list[keys[self.index]], cv2.COLOR_BGR2RGB)
            img1 = Image.fromarray(img1)
            img2 = cv2.cvtColor(
                self.coarse_img_list[keys[self.index]], cv2.COLOR_BGR2RGB)
            img2 = Image.fromarray(img2)

            imgtk1 = ImageTk.PhotoImage(image=img1)
            imgtk2 = ImageTk.PhotoImage(image=img2)

            self.label1.config(image=imgtk1)
            self.label1.image = imgtk1

            self.label2.config(image=imgtk2)
            self.label2.image = imgtk2

    def prev_next_warning(self, choice):
        if choice == 1:
            if messagebox.askokcancel("warning!", "no prev image."):
                pass
            else:
                pass
        else:
            if messagebox.askokcancel("warning!", "no next image."):
                pass
            else:
                pass

    def prev_img(self):
        if self.index <= 0:
            self.prev_next_warning(1)
        else:
            self.index -= 1
            keys = list(self.fine_img_list.keys())
            img1 = cv2.cvtColor(
                self.fine_img_list[keys[self.index]], cv2.COLOR_BGR2RGB)
            img1 = Image.fromarray(img1)
            img2 = cv2.cvtColor(
                self.coarse_img_list[keys[self.index]], cv2.COLOR_BGR2RGB)
            img2 = Image.fromarray(img2)

            imgtk1 = ImageTk.PhotoImage(image=img1)
            imgtk2 = ImageTk.PhotoImage(image=img2)

            self.label1.config(image=imgtk1)
            self.label1.image = imgtk1

            self.label2.config(image=imgtk2)
            self.label2.image = imgtk2

    def open_img(self):
        keys = list(self.fine_img_list.keys())
        #print(i[0], self.fine_img_list[i[0]])
        img1 = cv2.cvtColor(
            self.fine_img_list[keys[self.index]], cv2.COLOR_BGR2RGB)
        img1 = Image.fromarray(img1)
        img2 = cv2.cvtColor(
            self.coarse_img_list[keys[self.index]], cv2.COLOR_BGR2RGB)
        img2 = Image.fromarray(img2)

        imgtk1 = ImageTk.PhotoImage(image=img1)
        imgtk2 = ImageTk.PhotoImage(image=img2)

        self.label1 = tk.Label(self.window, image=imgtk1)
        self.label1.image = imgtk1
        self.label1.place(x=12, y=45)

        self.label2 = tk.Label(self.window, image=imgtk2)
        self.label2.image = imgtk2  # class 내에서 작업할 경우에는 이 부분을 넣어야 보인다.
        self.label2.place(x=12, y=443)

    def download(self):
        pass
        #tree = ElementTree(self.root)
        # tree.write('ssu.xml')

    def show_polygon(self):

        self.window.title("script window")
        self.window.geometry("700x840+100+100")

        frame_one = Frame(self.window, width=430, height=37)
        frame_one['borderwidth'] = 2
        frame_one['relief'] = 'sunken'
        frame_one.place(x=10, y=5)

        button1 = tk.Button(self.window, text='upload image', bg='#e0e0e0', fg='black',
                            font=('sans 11'), command=self.upload_img).place(x=15, y=10)
        button1 = tk.Button(self.window, text='upload xml', bg='#e0e0e0', fg='black',
                            font=('sans 11'), command=self.upload_xml).place(x=125, y=10)
        button2 = tk.Button(self.window, text='start annotation', bg='#e0e0e0', fg='black',
                            font=('sans 11'), command=self.parse_tree).place(x=220, y=10)
        button3 = tk.Button(self.window, text='open image', bg='#e0e0e0', fg='black',
                            font=('sans 11'), command=self.open_img).place(x=345, y=10)

        frame_two = Frame(self.window, width=230, height=37)
        frame_two['borderwidth'] = 2
        frame_two['relief'] = 'sunken'
        frame_two.place(x=460, y=5)

        button2 = tk.Button(self.window, text='prev', bg='#bdbdbd', fg='black',
                            font=('sans 11'), command=self.prev_img).place(x=470, y=10)
        button3 = tk.Button(self.window, text='next', bg='#bdbdbd', fg='black',
                            font=('sans 11'), command=self.next_img).place(x=525, y=10)
        button3 = tk.Button(self.window, text='masking view', bg='#bdbdbd', fg='black',
                            font=('sans 11'), command=self.masked_img).place(x=580, y=10)

        # frame for image view
        frame_img1 = Frame(self.window, width=680, height=388)
        frame_img1['borderwidth'] = 2
        frame_img1['relief'] = 'sunken'
        frame_img1.place(x=10, y=43)

        frame_img2 = Frame(self.window, width=680, height=388)
        frame_img2['borderwidth'] = 2
        frame_img2['relief'] = 'sunken'
        frame_img2.place(x=10, y=440)
        self.window.mainloop()


if __name__ == '__main__':
    polygon = Polygon_Proj(root)
    polygon.show_polygon()
    print("done")
