from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter.filedialog import asksaveasfilename
from tkinter import messagebox
import pyautogui
w,h = pyautogui.size()
class Paint:
    DEFAULTCOLOR = "black"
    DEFAULTPENSIZE = 5.0
    
    def __init__(self): 
        self.screen = Tk()
        self.screen.title("Paint App")
        self.screen.geometry(f"{w}x{h}")
        self.screen.config(background="white")

        self.menuBar = Menu(self.screen)
        self.file = Menu(self.menuBar, tearoff=0)
        self.file.add_command(label="New", command=self.clearCanvas)
        self.file.add_command(label="Save", command=self.saveImage)
        self.file.add_separator()
        self.file.add_command(label="Exit", command=self.screen.quit)
        self.menuBar.add_cascade(label="File", menu=self.file)

        self.screen.config(menu=self.menuBar)

        #self.toolbar = Frame(self.screen, bg="lightgray", width = w, height = h)
        #self.toolbar.grid(sticky = "nsew", row = 0, column = 0)

        Button(self.screen, text="Pen", width=10, command=self.usePen).grid(row = 1, column = 1, padx = 20)
        Button(self.screen, text="Brush", width=10, command=self.useBrush).grid(row = 1, column = 2, padx = 20)
        Button(self.screen, text="Eraser", width=10, command=self.useEraser).grid(row = 1, column = 3, padx = 20)
        Button(self.screen, text="Color", width=10, command=self.chooseColor).grid(row = 1, column = 4, padx = 20)
        Button(self.screen, text="Canvas Color", width=12, command=self.chooseCanvasColor).grid(row = 1, column = 5, padx = 20)
        Button(self.screen, text="Clear", width=10, command=self.clearCanvas).grid(row = 1, column = 6, padx = 20)

        self.scaler = Scale(self.screen, from_=1, to=20, orient="horizontal", label="Size")
        self.scaler.set(5)
        self.scaler.grid(row= 1, column = 7, padx = 20)

        self.canvas = Canvas(self.screen, bg="white", width=w, height = h-50)
        self.canvas.grid(columnspan=11, sticky="nsew")

        self.setup()

        self.screen.mainloop()
        
    def saveImage(self):
        self.screen.update()

        x = self.canvas.winfo_rootx()
        y = self.canvas.winfo_rooty()
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        
        filePath = asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png"), ("JPG Image", "*.jpg")]
        )

        if not filePath:
            messagebox.showwarning("Save Cancelled", "No file selected.")
            return
        
        screenshot = pyautogui.screenshot(region=(x, y, w, h))
        screenshot.save(filePath)

        messagebox.showinfo("Saved", "Your image has been saved successfully!")

    def setup(self):
        self.oldx, self.oldy = None, None
        self.lineWidth = self.scaler.get()
        self.color = self.DEFAULTCOLOR
        self.eraserUse = False

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

    def usePen(self):
        self.eraserUse = False

    def useBrush(self):
        self.eraserUse = False

    def useEraser(self):
        self.eraserUse = True

    def chooseColor(self):
        new_color = askcolor(color=self.color)[1]
        if new_color:
            self.color = new_color
            self.eraserUse = False

    def chooseCanvasColor(self):
        new_bg = askcolor(color=self.canvas["bg"])[1]
        if new_bg:
            self.canvas.config(bg=new_bg)

    def clearCanvas(self):
        self.canvas.delete("all")

    def paint(self, event):
        self.lineWidth = self.scaler.get()
        paintColor = "white" if self.eraserUse else self.color

        if self.oldx and self.oldy:
            self.canvas.create_line(
                self.oldx, self.oldy, event.x, event.y,
                width=self.lineWidth,
                fill=paintColor,
                capstyle="round",
                smooth=True,
                joinstyle="round",
                splinesteps=36
            )
        self.oldx, self.oldy = event.x, event.y
        
    def reset(self, event):
        self.oldx, self.oldy = None, None

if __name__ == "__main__":
    Paint()