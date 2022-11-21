from tkinter import *
from PIL import Image, ImageTk
from database import airquality_database
from interface.analyze_page import AnalyzePage
from interface.chart_page import ChartPage
from interface.file_page import FilePage
from interface.home_page import HomePage

db = airquality_database.AirQuality()
db.Create()
root = Tk()
root.title("AirQuality")
# root.geometry('1024x768')
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
# setting window size
root.geometry("%dx%d" % (width, height))
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

min_width = 50
max_width = 200
current_width = min_width  # Increasing width of the frame
extended = False
last_page = None


def Show():
    global current_width, extended
    current_width = current_width + 15
    repeat = root.after(5, Show)  # Repeat for every 5 ms
    frame.config(width=current_width)  # Change width to new width
    if current_width >= max_width:  # If width is greater than maximum width frame is expended
        extended = True
        root.after_cancel(repeat)  # Stop repeating
        Fill()


def Hide():
    global current_width, extended
    current_width = current_width - 15
    repeat = root.after(5, Hide)  # Repeat
    frame.config(width=current_width)  # Change the width to new width
    if current_width <= min_width:  # If it is back to normal width frame is not extended
        extended = False
        root.after_cancel(repeat)  # Stop repeating
        Fill()


def Fill():
    if extended:  # If the frame is exanded show text and remove image
        home_page.config(text='Home page', image='', font=(0, 20))
        read_file.config(text='Read files', image='', font=(0, 20))
        analyze_data.config(text='Analyze data', image='', font=(0, 20))
        chart_data.config(text='Chart', image='', font=(0, 20))
    else:
        # Show image again
        home_page.config(image=home, font=(0, 20))
        read_file.config(image=file, font=(0, 20))
        analyze_data.config(image=analyze, font=(0, 20))
        chart_data.config(image=chart, font=(0, 20))


def ShowPage(page):
    global last_page
    if last_page is not None:
        last_page.Hide()
    last_page = page.Show()


page1 = HomePage(root)
page2 = FilePage(root, db)
page3 = ChartPage(root, db)
page4 = AnalyzePage(root, db)
ShowPage(page1)

# Define image in menu and resize it
home = ImageTk.PhotoImage(Image.open('./photo/home.png').resize((40, 40), Image.ANTIALIAS))
file = ImageTk.PhotoImage(Image.open('./photo/file.png').resize((40, 40), Image.ANTIALIAS))
analyze = ImageTk.PhotoImage(Image.open('./photo/analyze.png').resize((40, 40), Image.ANTIALIAS))
chart = ImageTk.PhotoImage(Image.open('./photo/chart.png').resize((40, 40), Image.ANTIALIAS))

root.update()  # For the width to get updated

frame = Frame(root, bg='LightSkyBlue2', width=50, height=root.winfo_height())
frame.grid(row=0, column=0)

# Make the buttons with the icons to be shown
home_page = Button(frame, image=home, bg='LightSkyBlue2', relief='flat', command=lambda: ShowPage(page1))
read_file = Button(frame, image=file, bg='LightSkyBlue2', relief='flat', command=lambda: ShowPage(page2))
analyze_data = Button(frame, image=analyze, bg='LightSkyBlue2', relief='flat', command=lambda: ShowPage(page4))
chart_data = Button(frame, image=chart, bg='LightSkyBlue2', relief='flat', command=lambda: ShowPage(page3))

# Put on the frame
home_page.grid(row=0, column=0, pady=15)
read_file.grid(row=1, column=0, pady=15)
analyze_data.grid(row=3, column=0, pady=15)
chart_data.grid(row=4, column=0, pady=15)

# Bind to the frame, enter or leave
frame.bind('<Enter>', lambda e: Show())
frame.bind('<Leave>', lambda e: Hide())
frame.grid_propagate(False)

root.mainloop()
