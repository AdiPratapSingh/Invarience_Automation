from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
import cv2
import time

class App:
    def __init__(self,video_source=0):
        self.name = "Camera"
        self.window = Tk()
        self.window.title(self.name)
        self.window.resizable(0,0)
        self.video_source = video_source

        self.vid = Camera(self.video_source)
        self.label = Label(self.window,text=self.name,font=15).pack(side=TOP,fill=BOTH)
        self.canvas = Canvas(self.window,width = self.vid.width,height = self.vid.height)
        self.canvas.pack()

        self.btn_snapshot = Button(self.window, text="Snapshot", width = 30, command=self.snapshot)
        self.btn_snapshot.pack(anchor=CENTER, expand=True)
        self.update()

        # loop
        self.window.mainloop()

    def snapshot(self):
        check, frame = self.vid.snapshot()
        if check:
            image = "item-" + time.strftime("%H-%M-%S-%d-%m") + ".jpg"
            cv2.imwrite(image, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            msg = Label(self.window, text = 'image saved' + image ).place(x=430,y=510)

    def update(self):
        isTrue, frame = self.vid.snapshot()

        if isTrue:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = NW)

        self.window.after(15, self.update)



class Camera:
    def __init__(self, video_source=0):
        self.vid = cv2.VideoCapture(video_source)
    
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def snapshot(self):
        if self.vid.isOpened():
            isTrue, frame = self.vid.read()
            if isTrue:
                return (isTrue, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (isTrue,NONE)
        else:
            return (isTrue,NONE)
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

if __name__ == '__main__':
    App()