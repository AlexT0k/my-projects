import math
import tkinter as tk
import time
#the packages we'll need

def animation_cycle():
    move_second_hand(seconds_step)
    move_minute_hand(seconds_step)
    move_hour_hand(seconds_step)

    # calculate new sleep_time
    sleep_time_ms = int(seconds_period*seconds_step*1000/360) # sleep time sets the hands update frequency depending on set periond and step
    canv.after(sleep_time_ms, animation_cycle)  # call itself after sleep_time

def validate_step(): # step value validation
    global seconds_step
    try:
        newval = int(entry1.get())
    except ValueError:
        newval = seconds_step
    if newval>0 and newval<31: # if step is bigger than 0 and lower than 31 it sutisfyies the conditions else it keeps the old value
        seconds_step = newval
    entry1.delete(0,tk.END)
    entry1.insert(0,seconds_step)

def validate_period(): # period value validation
    global seconds_period
    try:
        newval = int(entry2.get())
    except ValueError:
        newval = seconds_period
    if newval>4 and newval<61: # if step is bigger than 4 and lower than 61 it sutisfyies the conditions else it keeps the old value
        seconds_period = newval
    entry2.delete(0, tk.END)
    entry2.insert(0,seconds_period)

def draw_hand(radius, fill_cl, width, angle, tail=40):
    in_radian = math.radians(angle) # Convert degrees to radians
    x1 = clk_xc - tail * math.sin(in_radian)  # First point x coordinate
    y1 = clk_yc + tail * math.cos(in_radian)  # First point y coordinate
    x2 = clk_xc + radius * math.sin(in_radian)  # Second point x coordinate
    y2 = clk_yc - radius * math.cos(in_radian)  # Second point y coordinate
    return canv.create_line(x1, y1, x2, y2, arrow='last', fill=fill_cl, width=width) #draws a line with a tip on the end, unique width and colour based on two points

def move_second_hand(move_step):
    global position_s, second
    canv.delete(second)  # delete the hand
    second = draw_hand(radius=rs, fill_cl='red', width=2, angle=position_s) #giveing an identifier for a second hand
    if position_s >= 360:  # one rotattion is over if reached 360
        position_s = position_s % 360  # start from zero angle again
    position_s = position_s + move_step  # set second hand step


def move_minute_hand(move_step):
    global position_m, minute
    position_m = position_m + move_step / 60  # set minute hand step 60 times slower than second hand 
    canv.delete(minute)  # delete the previous hand
    minute = draw_hand(radius=rm, fill_cl='green', width=4, angle=position_m) #giveing an identifier for a minute hand
    if position_m >= 360:  # One rotation of 360 degree is over
        position_m = 0


def move_hour_hand(move_step):
    global position_h, hour
    position_h = position_h + move_step / 720  # set hour hand step 720 times slower than second hand
    canv.delete(hour)  # deleting hour hand
    hour = draw_hand(radius=rh, fill_cl='#a83e32', width=6, angle=position_h) #giveing an identifier for a hour hand
    if (position_h >= 360):
        position_h = 0


# Create main window
main_win = tk.Tk()
win_width, win_height = 800, 800
d = str(win_width) + "x" + str(win_height)
# set main window size
main_win.geometry(d)

# create big font for labels, entryes and buttons
font1 = ('Arial', 12, 'bold')

# create frame for  "Animation step" label, entry and button
frame1 = tk.Frame(main_win)
# place frame to main window
frame1.pack(fill=tk.X)
# create label
lbl1 = tk.Label(frame1, text="Second's hand move step (1..30), degrees:", width=0, font=font1)
lbl1.pack(side=tk.LEFT, padx=5, pady=5)
# set basic second step
seconds_step = 6
# create entry 
entry1 = tk.Entry(frame1, font=font1, width=10)
entry1.insert(0,str(seconds_step))
entry1.pack(side=tk.LEFT)
# cerate button
button1 = tk.Button(frame1, text="Submit", command = validate_step)
button1.pack(side=tk.LEFT, pady=5, padx=5)
frame1.update()

# repeat for "Hands period"
frame2 = tk.Frame(main_win)
frame2.pack(fill=tk.X)
lbl2 = tk.Label(frame2, text="Hands period (5..60), seconds:", width=0, font=font1)
lbl2.pack(side=tk.LEFT, padx=5, pady=5)
seconds_period = 60
entry2 = tk.Entry(frame2, font=font1, width=10)
entry2.insert(0,str(seconds_period))
entry2.pack(side=tk.LEFT)
button2 = tk.Button(frame2, text="Submit", command = validate_period)
button2.pack(side=tk.LEFT, pady=5, padx=5)
frame2.update()

# create third frame and put it on main window
frame3 = tk.Frame(main_win)
frame3.pack(fill=tk.BOTH, expand=True)
# create and place canvas on frame3
canv = tk.Canvas(frame3, bg='white')
canv.pack(fill=tk.BOTH, expand=True,padx=5, pady=5)
frame3.update()

# calculate canvas size
c_width = canv.winfo_width()
c_height = canv.winfo_height()

# set clock diameter, as 85% from minimum size value
clk_diam = min(c_width, c_height)*0.85
# calculate clock center coordinates
clk_xc = c_width/2 # clock center x
clk_yc =  (c_height-clk_diam)/2 + clk_diam/2 # clock center y

# calculate coordinates of the top left and bottom right points - for clock frame
clk_x0 = clk_xc - clk_diam/2
clk_y0 = (c_height-clk_diam)/2
clk_x1 = clk_x0 + clk_diam
clk_y1 = clk_y0 + clk_diam
# draw clock frame line
dial = canv.create_oval(clk_x0, clk_y0, clk_x1, clk_y1, width=5, outline='#008080')

mark_r = clk_diam/2-20  # radius for dial marks for one minute
nummark_r = clk_diam / 2 - 90  # radius for hour numbers  after the marks

rs = clk_diam/2-60  # length of second hand
rm = clk_diam/2-60  # length of minute hand
rh = clk_diam/2-90  # lenght of hour hand

position_s = int(time.strftime('%S')) * 6  # local second
position_m = int(time.strftime('%M')) * 6  # local minutes
position_h = int(time.strftime('%I')) * 30 + 30 * position_m / 360 # 12-hour format
if position_h == 360:
    position_h = 0  # adjusting 12 O'clock to 0

h = iter(['12', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11'])

# Marking on the dial - 6 degrees per mark
for i in range(0, 60):
    in_radian = math.radians(i*6)

    if (i % 5) == 0:
        # every 5th mark is hour mark
        ratio = 0.85  # Long marks
        mark_width = 4
        x = clk_xc + nummark_r * math.sin(in_radian)  # x coordinate to add hour number
        y = clk_yc - nummark_r * math.cos(in_radian)  # y coordinate to add hour number
        canv.create_text(x, y, fill='#000080', font="Times 30  bold", text=next(h))  # number added
    else:
        # minutes mark
        ratio = 0.9  # small marks
        mark_width = 2

    # draw mark line
    x1 = clk_xc + ratio * mark_r * math.sin(in_radian)
    y1 = clk_yc - ratio * mark_r * math.cos(in_radian)
    x2 = clk_xc + mark_r * math.sin(in_radian)
    y2 = clk_yc - mark_r * math.cos(in_radian)
    canv.create_line(x1, y1, x2, y2, width=mark_width) 

# creating variables for hands IDs
second = 0
minute = 0
hour = 0

animation_cycle() # main cycle start
main_win.mainloop() # main event loop
