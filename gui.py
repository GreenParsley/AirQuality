from tkinter import *
from PIL import Image, ImageTk

import airquality_database
from interface.chart_page import ChartPage
from interface.file_page import FilePage
from interface.home_page import HomePage

db = airquality_database.AirQuality()
db.Create()
root = Tk()
root.title("AirQuality")
#root.geometry('1024x768')
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
# setting window size
root.geometry("%dx%d" % (width, height))
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

minWidth = 50
maxWidth = 200
currentWidth = minWidth  # Increasing width of the frame
extended = False
lastPage = None

def show():
    global currentWidth, extended
    currentWidth = currentWidth + 15
    repeat = root.after(5, show)  # Repeat for every 5 ms
    frame.config(width=currentWidth)  # Change width to new width
    if currentWidth >= maxWidth:  # If width is greater than maximum width frame is expended
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
        analyzeData.config(text='Analyze data', image='', font=(0, 20))
        chartData.config(text='Chart', image='', font=(0, 20))
    else:
        # Show image again
        homePage.config(image=home, font=(0, 20))
        readFile.config(image=file, font=(0, 20))
        exportData.config(image=export, font=(0, 20))
        analyzeData.config(image=analyze, font=(0, 20))
        chartData.config(image=chart, font=(0, 20))

def showPage(page):
    global lastPage
    if lastPage is not None:
        lastPage.hide()
    lastPage = page.show()

page1 = HomePage(root)
page2 = FilePage(root, db)
page3 = ChartPage(root, db)

# Define image in menu and resize it
home = ImageTk.PhotoImage(Image.open('home.png').resize((40, 40), Image.ANTIALIAS))
file = ImageTk.PhotoImage(Image.open('file.png').resize((40, 40), Image.ANTIALIAS))
export = ImageTk.PhotoImage(Image.open('export.png').resize((40, 40), Image.ANTIALIAS))
analyze = ImageTk.PhotoImage(Image.open('analyze.png').resize((40, 40), Image.ANTIALIAS))
chart = ImageTk.PhotoImage(Image.open('chart.png').resize((40, 40), Image.ANTIALIAS))

root.update()  # For the width to get updated

frame = Frame(root, bg='LightSkyBlue2', width=50, height=root.winfo_height())
frame.grid(row=0, column=0)

# Make the buttons with the icons to be shown
homePage = Button(frame, image=home, bg='LightSkyBlue2', relief='flat', command=lambda: showPage(page1))
readFile = Button(frame, image=file, bg='LightSkyBlue2', relief='flat', command=lambda: showPage(page2))
exportData = Button(frame, image=export, bg='LightSkyBlue2', relief='flat')
analyzeData = Button(frame, image=analyze, bg='LightSkyBlue2', relief='flat')
chartData = Button(frame, image=chart, bg='LightSkyBlue2', relief='flat', command=lambda: showPage(page3))

# Put on the frame
homePage.grid(row=0, column=0, pady=15)
readFile.grid(row=1, column=0, pady=15)
exportData.grid(row=2, column=0, pady=15)
analyzeData.grid(row=3, column=0, pady=15)
chartData.grid(row=4, column=0, pady=15)

# Bind to the frame, enter or leave
frame.bind('<Enter>', lambda e: show())
frame.bind('<Leave>', lambda e: hide())
frame.grid_propagate(False)

root.mainloop()
