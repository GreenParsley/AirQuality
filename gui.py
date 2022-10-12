from tkinter import *
from PIL import Image, ImageTk

root = Tk()
root.title("AirQuality")
#root.geometry('1024x768')
width= root.winfo_screenwidth()
height= root.winfo_screenheight()
# setting window size
root.geometry("%dx%d" % (width, height))
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

minWidth = 50
maxWidth = 200
currentWidth = minWidth  # Increasing width of the frame
extended = False


def show():
    global currentWidth, extended
    currentWidth = currentWidth + 15
    repeat = root.after(5, show)  # Repeat for every 5 ms
    frame.config(width=currentWidth)  # Change width to new width
    if currentWidth >= maxWidth:  # If width is greater than maximum width grame is expended
        extended = True
        root.after_cancel(repeat)  # Stop repeating
        fill()


def hide():
    global currentWidth, extended
    currentWidth = currentWidth - 15
    repeat = root.after(5, hide)  # Repeat
    frame.config(width=currentWidth)  # Change the width to new width
    if currentWidth <= minWidth:  # If it is back to normal width frame is not extended
        extended = False
        root.after_cancel(repeat)  # Stop repeating
        fill()


def fill():
    if extended:  # If the frame is exanded show text and remove image
        homePage.config(text='Home page', image='', font=(0, 20))
        readFile.config(text='Read files', image='', font=(0, 20))
        exportData.config(text='Export data', image='', font=(0, 20))
        analizeData.config(text='Analize data', image='', font=(0, 20))
        chartData.config(text='Chart', image='', font=(0, 20))
    else:
        # Show image again
        homePage.config(image=home, font=(0, 20))
        readFile.config(image=file, font=(0, 20))
        exportData.config(image=export, font=(0, 20))
        analizeData.config(image=analize, font=(0, 20))
        chartData.config(image=chart, font=(0, 20))

def openHomePage(widget):
    #widget.pack()
    widget.grid_remove()

def closeHomePage(widget):
    #widget.pack_forget()
    widget.grid()

# Home page
frameMainPage = Frame(root, bg="pink")
frameMainPage.grid(row=0, column=1, sticky="NSEW")
mainPage = Label(frameMainPage, text="Welcome to the AirQuality app", font=(0,50), background="yellow", anchor=CENTER)
mainPage.grid(row=0, column=0, sticky="NSEW")

# Define image in menu and resize it
home = ImageTk.PhotoImage(Image.open('home.png').resize((40, 40), Image.ANTIALIAS))
file = ImageTk.PhotoImage(Image.open('file.png').resize((40, 40), Image.ANTIALIAS))
export = ImageTk.PhotoImage(Image.open('export.png').resize((40, 40), Image.ANTIALIAS))
analize = ImageTk.PhotoImage(Image.open('analize.png').resize((40, 40), Image.ANTIALIAS))
chart = ImageTk.PhotoImage(Image.open('chart.png').resize((40, 40), Image.ANTIALIAS))

root.update()  # For the width to get updated

frame = Frame(root, bg='LightSkyBlue1', width=50, height=root.winfo_height())
frame.grid(row=0, column=0)

# Make the buttons with the icons to be shown
homePage = Button(frame, image=home, bg='LightSkyBlue1', relief='flat', command=openHomePage(frameMainPage))
readFile = Button(frame, image=file, bg='LightSkyBlue1', relief='flat', command=closeHomePage(frameMainPage))
exportData = Button(frame, image=export, bg='LightSkyBlue1', relief='flat')
analizeData = Button(frame, image=analize, bg='LightSkyBlue1', relief='flat')
chartData = Button(frame, image=chart, bg='LightSkyBlue1', relief='flat')

# Put on the frame
homePage.grid(row=0, column=0, pady=10)
readFile.grid(row=1, column=0, pady=10)
exportData.grid(row=2, column=0, pady=10)
analizeData.grid(row=3, column=0, pady=10)
chartData.grid(row=4, column=0, pady=10)

# Bind to the frame, enter or leave
frame.bind('<Enter>', lambda e: show())
frame.bind('<Leave>', lambda e: hide())
frame.grid_propagate(False)

root.mainloop()
