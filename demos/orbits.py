import tkinter as tk
#from tkinter import filedialog
from time import sleep
#from tkinter import Canvas

def graphics_demo(circle_size, circle_position, segment_size, num_segments):


    master = tk.Tk()
    c = tk.Canvas(master, width=600, height=400)
    circle = c.create_oval(300, 300, circle_size, circle_size, fill='yellow')
    c.pack()
    master.mainloop()
    #for i in range(num_segments):
    #    if i%2 == 0:
    #        circle.move(segment_size, 0, track=True)
    #    else:
    #        circle.move(segment_size, 0)
    #    Canvas.update()
    #    sleep(.05)

graphics_demo(10, (100, 100), 5, 20)