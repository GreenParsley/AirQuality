from tkinter import *
from PIL import Image, ImageTk

root = Tk()
root.title("AirQuality")
#root.geometry('1024x768')
width= root.winfo_screenwidth()
height= root.winfo_screenheight()
#setting tkinter window size
root.geometry("%dx%d" % (width, height))
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

minWidth = 50  # Minimum width of the frame
maxWidth = 200  # Maximum width of the frame
currentWidth = minWidth  # Increasing width of the frame
extended = False  # Check if it is completely exanded


def show():
    global currentWidth, extended
    currentWidth = currentWidth + 15  # Increase the width by 15
    repeat = root.after(5, show)  # Repeat this func every 5 ms
    frame.config(width=currentWidth)  # Change the width to new increase width
    if currentWidth >= maxWidth:  # If width is greater than maximum width
        extended = True  # Frame is expended
        root.after_cancel(repeat)  # Stop repeating the func
        fill()


def hide():
    global currentWidth, extended
    currentWidth = currentWidth - 15 # Reduce the width by 15
    repeat = root.after(5, hide)  # Call this func every 5 ms
    frame.config(width=currentWidth)  # Change the width to new reduced width
    if currentWidth <= minWidth:  # If it is back to normal width
        extended = False  # Frame is not extended
        root.after_cancel(repeat)  # Stop repeating the func
        fill()


def fill():
    if extended:  # If the frame is exanded
        # Show a text, and remove the image
        homePage.config(text='Home page', image='', font=(0, 20))
        readFile.config(text='Read files', image='', font=(0, 20))
        exportData.config(text='Export data', image='', font=(0, 20))
        analizeData.config(text='Analize data', image='', font=(0, 20))
        chartData.config(text='Chart', image='', font=(0, 20))
    else:
        # Bring the image back
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

# Define the icons to be shown and resize it
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

# Put them on the frame
homePage.grid(row=0, column=0, pady=10)
readFile.grid(row=1, column=0, pady=10)
exportData.grid(row=2, column=0, pady=10)
analizeData.grid(row=3, column=0, pady=10)
chartData.grid(row=4, column=0, pady=10)



# Bind to the frame, if entered or left
frame.bind('<Enter>', lambda e: show())
frame.bind('<Leave>', lambda e: hide())

# So that it does not depend on the widgets inside the frame
frame.grid_propagate(False)

root.mainloop()
