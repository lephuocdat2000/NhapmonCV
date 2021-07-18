# import cv2
# import numpy as np
# from matplotlib import pyplot as plt
# from sklearn.cluster import KMeans
# from sklearn.preprocessing import StandardScaler
# from numpy import asarray
# from PIL import ImageFilter, ImageTk
import PIL
import math
from tkinter import *
from tkinter import ttk
from tkinter import filedialog, Text
from Source import *
from PIL import Image
from tkinter import filedialog

root = Tk()
root.title("Remove background with chroma key")
root.config(bg="skyblue")
root.geometry("1200x700")
root.resizable(0, 0)

i = 0
tab_Panel = ttk.Notebook(root)
s = ttk.Style()
s.configure('tFrame.TFrame', background='pink')
bgcolor ="skyblue"
thresholdv = 0
thresholdw = 0
H_thresh = IntVar()
H_thresh.set(60)
S_thresh = IntVar()
S_thresh.set(245)
lpadx = 20
lpady = 5
bwidth=15
stopcode=0
def Image_to_Dislay(img):
    dislay = cv2.resize(img, (500, 250))
    dislay = cv2.cvtColor(dislay, cv2.COLOR_BGR2RGB)
    dislay = PIL.Image.fromarray(dislay)
    dislay = ImageTk.PhotoImage(dislay)
    return dislay
def Image_to_Background(img):
    dislay = cv2.resize(img, (1200, 700))
    dislay = cv2.cvtColor(dislay, cv2.COLOR_BGR2RGB)
    dislay = PIL.Image.fromarray(dislay)
    dislay = ImageTk.PhotoImage(dislay)
    return dislay
background_frame = Image_to_Background(cv2.imread("Background/background.jpg"))
holder_chroma_img = Image_to_Dislay(cv2.imread("Image_holder/Place_holder_img.jpg"))
holder_chroma_vid = Image_to_Dislay(cv2.imread("Image_holder/Place_holder_video.jpg"))
holder_webcam = Image_to_Dislay(cv2.imread("Image_holder/Place_holder_webcam.jpg"))
holder_background_img = Image_to_Dislay(cv2.imread("Image_holder/Place_holder_background.jpg"))
holder_result = Image_to_Dislay(cv2.imread("Image_holder/Place_holder_result.jpg"))
holder_novideo = Image_to_Dislay(cv2.imread("Image_holder/Place_holder_novideo.jpg"))

# Button Function from tab_img_img
def choose_File_img():
    global img
    global img1
    global label_img
    global cf1_Button_img
    global cl1_Button_img

    f = filedialog.askopenfile(initialdir="/", title="Select File",
                             filetypes=(("image", "*.jpg"), ("image", "*.png")))
    img = cv2.imread(f.name)
    img1 = Image_to_Dislay(img)
    label_img.grid_forget()
    label_img = Label(iFrame1, image=img1)
    label_img.grid(row=0, column=0,columnspan=2, padx=lpadx, pady=lpady)
    cf1_Button_img = Button(iFrame1, text="Choose file", command=lambda: choose_File_img(), width=bwidth)
    cf1_Button_img.grid(row=1, column=0)
    cl1_Button_img = Button(iFrame1, text="Clear", command=lambda: clear_img(), width=bwidth)
    cl1_Button_img.grid(row=1, column=1)
def clear_img():
    global label_img
    global cf1_Button_img
    global cl1_Button_img
    label_img.grid_forget()
    label_img = Label(iFrame1, image=holder_chroma_img)
    label_img.grid(row=0, column=0, columnspan=2, padx=lpadx, pady=lpady)
    cf1_Button_img = Button(iFrame1, text="Choose file", command=lambda: choose_File_img(), width=bwidth)
    cf1_Button_img.grid(row=1, column=0)
    cl1_Button_img = Button(iFrame1, text="Clear", command=lambda: clear_img(), width=bwidth)
    cl1_Button_img.grid(row=1, column=1)
def choose_File_background():
    global background
    global img2
    global label_background
    global cf2_Button_img
    global cl2_Button_img
    f = filedialog.askopenfile(initialdir="/", title="Select File",
                               filetypes=(("image", "*.jpg"), ("image", "*.png")))
    background = cv2.imread(f.name)
    img2 = Image_to_Dislay(background)
    label_background.grid_forget()
    label_background = Label(iFrame2, image=img2)
    label_background.grid(row=0, column=0, columnspan=2, padx=lpadx, pady=lpady)
    cf2_Button_img = Button(iFrame2, text="Choose file", command=lambda: choose_File_background(), width=bwidth)
    cf2_Button_img.grid(row=1, column=0)
    cl2_Button_img = Button(iFrame2, text="Clear", command=lambda: clear_background(), width=bwidth)
    cl2_Button_img.grid(row=1, column=1)
def clear_background():
    global label_background
    global cf2_Button_img
    global cl2_Button_img
    label_background.grid_forget()
    label_background = Label(iFrame2, image=holder_background_img)
    label_background.grid(row=0, column=0, columnspan=2, padx=lpadx, pady=lpady)
    cf2_Button_img = Button(iFrame2, text="Choose file", command=lambda: choose_File_background(), width=bwidth)
    cf2_Button_img.grid(row=1, column=0)
    cl2_Button_img = Button(iFrame2, text="Clear", command=lambda: clear_background(), width=bwidth)
    cl2_Button_img.grid(row=1, column=1)
def submit():
    global img, background
    global label_result, sm_Button, clr_Button
    global res
    global upper_green_img, lower_green_img
    global H_thresh, S_thresh
    lower_green_img, upper_green_img = Get_threshold(img, H_thresh.get(), S_thresh.get())
    res = Remove_background(img=img, background=background, upper=upper_green_img, lower=lower_green_img)
    cv2.imwrite('bgp.png', res)
    res = cv2.resize(res, (500, 250))
    res = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)
    res = Image.fromarray(np.uint8(res))
    res = ImageTk.PhotoImage(res)
    label_result.grid_forget()
    label_result = Label(iFrame3, image=res)
    label_result.grid(row=0, column=0, columnspan=2, padx=lpadx, pady=lpady)
    sm_Button = Button(iFrame3, text="Submit", command=lambda: submit(), width=bwidth)
    sm_Button.grid(row=1, column=0)
    clr_Button = Button(iFrame3, text="Clear", command=lambda: clear_result(), width=bwidth)
    clr_Button.grid(row=1, column=1)
def clear_result():
    global label_result
    global sm_Button
    global clr_Button
    label_result.grid_forget()
    label_result = Label(iFrame3, image=holder_result)
    label_result.grid(row=0, column=0, columnspan=2, padx=20, pady=5)
    sm_Button = Button(iFrame3, text="Submit", command=lambda: submit(), width=bwidth)
    sm_Button.grid(row=1, column=0)
    clr_Button = Button(iFrame3, text="Clear", command=lambda: clear_result(), width=bwidth)
    clr_Button.grid(row=1, column=1)

#Button Function from tab_video_img
def show_frame():
    global vbackground
    global thresholdv
    global upper_green, lower_green
    global H_thresh, S_thresh
    global stopcode, out
    if stopcode==0:
        ret, frame = chromavideo.read()
        if ret:
            if thresholdv==0:
                lower_green, upper_green = Get_threshold(frame, H_thresh.get(), S_thresh.get())
                thresholdv = 1
            res = Remove_background(img=frame, background=vbackground, lower=lower_green, upper=upper_green)
            out.write(res)
            res = cv2.resize(res, (500, 250))
            res = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)
            res = Image.fromarray(np.uint8(res))
            frame = cv2.resize(frame, (500, 250))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = Image.fromarray(frame)
            restk = ImageTk.PhotoImage(res)
            imgtk = ImageTk.PhotoImage(frame)
            label_video.imgtk = imgtk
            label_video.configure(image=imgtk)
            labelv_result.imgtk = restk
            labelv_result.configure(image=restk)
            tab_video_img.after(1, show_frame)
        else:
            stopcode=1
    else:
        clear_result_video()
        clear_video()
def set_stopcode():
    global stopcode
    if stopcode==1:
        clear_video()
        clear_result_video()
    stopcode=1
def choose_File_video():
    global filename
    global frame
    global vid
    global label_video
    global upper_green, lower_green
    global cf1_Button_video
    global cl1_Button_video
    global threshold
    thresholdv = 0
    filename = filedialog.askopenfilename()
    chroma_video = cv2.VideoCapture(filename)
    if(chroma_video.isOpened()==False):
        label_video.grid_forget()
        label_video = Label(vFrame1, image=holder_novideo)
        label_video.grid(row=0, column=0, columnspan=2, padx=lpadx, pady=lpady)
        cf1_Button_video = Button(vFrame1, text="Choose file", command=lambda: choose_File_video(), width=bwidth)
        cf1_Button_video.grid(row=1, column=0)
        cl1_Button_video = Button(vFrame1, text="Clear", command=lambda: clear_video(), width=bwidth)
        cl1_Button_video.grid(row=1, column=1)
    else:
        ret, frame = chroma_video.read()
        frame = cv2.resize(frame, (500, 250))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = PIL.Image.fromarray(frame)
        frame = ImageTk.PhotoImage(image=frame)
        label_video.grid_forget()
        label_video = Label(vFrame1, image=frame)
        label_video.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        cf1_Button_video = Button(vFrame1, text="Choose file", command=lambda: choose_File_video(), width=bwidth)
        cf1_Button_video.grid(row=1, column=0)
        cl1_Button_video = Button(vFrame1, text="Clear", command=lambda: clear_video(), width=bwidth)
        cl1_Button_video.grid(row=1, column=1)
    chroma_video.release()
def clear_video():
    global label_video
    global cf1_Button_video
    global cl1_Button_video
    global thresholdv
    thresholdv = 0
    label_video.grid_forget()
    label_video = Label(vFrame1, image=holder_chroma_vid)
    label_video.grid(row=0, column=0, columnspan=2, padx=lpadx, pady=lpady)
    cf1_Button_video = Button(vFrame1, text="Choose file", command=lambda: choose_File_video(), width=bwidth)
    cf1_Button_video.grid(row=1, column=0)
    cl1_Button_video = Button(vFrame1, text="Clear", command=lambda: set_stopcode(), width=bwidth)
    cl1_Button_video.grid(row=1, column=1)
def choose_File_background_video():
    global vbackground
    global img3
    global labelv_background
    global cf2_Button_video
    global cl2_Button_video
    f = filedialog.askopenfile(initialdir="/", title="Select File",
                               filetypes=(("image", "*.jpg"), ("image", "*.png")))
    vbackground = cv2.imread(f.name)
    img3 = cv2.resize(vbackground, (500, 250))
    img3 = cv2.cvtColor(img3, cv2.COLOR_BGR2RGB)
    img3 = PIL.Image.fromarray(img3)
    img3 = ImageTk.PhotoImage(image=img3)
    labelv_background.grid_forget()
    labelv_background = Label(vFrame2, image=img3)
    labelv_background.grid(row=0, column=0, columnspan=2, padx=lpadx, pady=lpady)
    cf2_Button_img = Button(vFrame2, text="Choose file", command=lambda: choose_File_background_video(), width=bwidth)
    cf2_Button_img.grid(row=1, column=0)
    cl2_Button_img = Button(vFrame2, text="Clear", command=lambda: clear_background_video(), width=bwidth)
    cl2_Button_img.grid(row=1, column=1)
def clear_background_video():
    global labelv_background
    global cf2_Button_video
    global cl2_Button_video

    labelv_background.grid_forget()
    labelv_background = Label(vFrame2, image=holder_background_img)
    labelv_background.grid(row=0, column=0, columnspan=2, padx=lpadx, pady=lpady)
    cf2_Button_video = Button(vFrame2, text="Choose file", command=lambda: choose_File_background_video())
    cf2_Button_video.grid(row=1, column=0)
    cl2_Button_video = Button(vFrame2, text="Clear", command=lambda: set_stopcode())
    cl2_Button_video.grid(row=1, column=1)
def submit_video():
    global label_video
    global chromavideo
    global thresholdv
    global stopcode
    global out
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('out.avi', fourcc, 20.0, (1280, 720))
    stopcode = 0
    thresholdv = 0
    chromavideo = cv2.VideoCapture(filename)
    show_frame()
    out.release()
def clear_result_video():
    global labelv_result
    global sm_Button_video
    global clr_Button_video

    labelv_result.grid_forget()
    labelv_result = Label(vFrame3, image=holder_result)
    labelv_result.grid(row=0, column=0, columnspan=2, padx=lpadx, pady=lpady)
    sm_Button_video = Button(vFrame3, text="Submit", command=lambda: submit_video(), width=bwidth)
    sm_Button_video.grid(row=1, column=0)
    clr_Button_video = Button(vFrame3, text="Clear", command=lambda: set_stopcode(), width=bwidth)
    clr_Button_video.grid(row=1, column=1)

#Button Function from tab_webcam_img
def show_webcam():
    global wbackground
    global lower_green_webcam, upper_green_webcam
    global thresholdw
    global H_thresh, S_thresh
    ret, frame = webcam.read()
    if ret:
        frame = cv2.flip(frame, 1)
        frame1 = cv2.resize(frame, (500,250))
        frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
        frame1 = Image.fromarray(frame1)
        imgtk = ImageTk.PhotoImage(image=frame1)
        label_webcam.imgtk = imgtk
        label_webcam.configure(image=imgtk)
        if i == 1:
            if thresholdw == 0:
                lower_green_webcam, upper_green_webcam = Get_threshold(frame, H_thresh.get(), S_thresh.get())
                thresholdw = 1
            res = Remove_background(img=frame, background=wbackground, upper=upper_green_webcam, lower=lower_green_webcam)
            res = cv2.resize(res, (500, 250))
            res = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)
            res = Image.fromarray(np.uint8(res))
            restk = ImageTk.PhotoImage(res)
            labelw_result.imgtk = restk
            labelw_result.configure(image=restk)
        tab_webcam_img.after(10, show_webcam)
def enable_Webcam():
    global webcam
    webcam = cv2.VideoCapture(0)
    show_webcam()
def disable_Webcam():
    global label_webcam
    global labelw_result
    global webcam
    global cf1_Button_webcam
    global cl1_Button_webcam
    global sm_Button_webcam
    global i
    i = 0
    webcam.release()
    # clear webcam input
    label_webcam.grid_forget()
    label_webcam = Label(wFrame1, image=holder_webcam)
    label_webcam.grid(row=0, column=0, columnspan=2, padx=lpadx, pady=lpady)
    cf1_Button_webcam = Button(wFrame1, text="Enable webcam", command=lambda: enable_Webcam(), width=bwidth)
    cf1_Button_webcam.grid(row=1, column=0)
    cl1_Button_webcam = Button(wFrame1, text="Disable webcam", command=lambda: disable_Webcam(), width=bwidth)
    cl1_Button_webcam.grid(row=1, column=1)

def choose_File_background_webcam():
    global wbackground
    global img4
    global labelw_background
    global cf2_Button_webcam
    global cl2_Button_webcam
    f = filedialog.askopenfile(initialdir="/", title="Select File",
                               filetypes=(("image", "*.jpg"), ("image", "*.png")))
    wbackground = cv2.imread(f.name)
    img4 = cv2.resize(wbackground, (500, 250))
    img4 = cv2.cvtColor(img4, cv2.COLOR_BGR2RGB)
    img4 = PIL.Image.fromarray(img4)
    img4 = ImageTk.PhotoImage(image=img4)
    labelw_background.grid_forget()
    labelw_background = Label(wFrame2, image=img4)
    labelw_background.grid(row=0, column=0, columnspan=2, padx=lpadx, pady=lpady)
    cf2_Button_webcam = Button(wFrame2, text="Choose file", command=lambda: choose_File_background_webcam(), width=bwidth)
    cf2_Button_webcam.grid(row=1, column=0)
    cl2_Button_webcam = Button(wFrame2, text="Clear", command=lambda: clear_background_webcam(), width=bwidth)
    cl2_Button_webcam.grid(row=1, column=1)
def clear_background_webcam():
    global labelw_background
    global cf2_Button_webcam
    global cl2_Button_webcam
    labelw_background.grid_forget()
    labelw_background = Label(wFrame2, image=holder_background_img)
    labelw_background.grid(row=0, column=0, columnspan=2, padx=lpadx, pady=lpady)
    cf2_Button_webcam = Button(wFrame2, text="Choose file", command=lambda: choose_File_background_webcam(),width=bwidth)
    cf2_Button_webcam.grid(row=1, column=0)
    cl2_Button_webcam = Button(wFrame2, text="Clear", command=lambda: clear_background_webcam(), width=bwidth)
    cl2_Button_webcam.grid(row=1, column=1)
def submit_webcam():
    global webcam
    global i
    global thresholdw
    i = 1
    thresholdw = 0

#########################################

tab_img_img = ttk.Frame(tab_Panel, style="tFrame.TFrame")
background_label1 = Label(tab_img_img, image=background_frame)
background_label1.place(x=0, y=0, relwidth=1, relheight=1)
#Frame chromakey image : iFrame1
iFrame1 = Frame(tab_img_img, width=550, height=300, bg=bgcolor)
iFrame1.grid(row=0, column=0, padx=25, pady=15)
iFrame1.grid_propagate(0)

label_img = Label(iFrame1, image=holder_chroma_img)
label_img.grid(row=0, column=0, columnspan=2, padx=lpadx, pady=lpady)
cf1_Button_img = Button(iFrame1, text="Choose file", command=lambda: choose_File_img(), width=bwidth)
cf1_Button_img.grid(row=1, column=0)
cl1_Button_img = Button(iFrame1, text="Clear", command=lambda: clear_img(), width=bwidth)
cl1_Button_img.grid(row=1, column=1)


#Frame background image: iFrame2
iFrame2 = Frame(tab_img_img, width=550, height=300, bg=bgcolor)
iFrame2.grid(row=1, column=0, padx=25, pady=15)
iFrame2.grid_propagate(0)
label_background = Label(iFrame2, image=holder_background_img)
label_background.grid(row=0, column=0, columnspan=2, padx=lpadx, pady=lpady)
cf2_Button_img = Button(iFrame2, text="Choose file", command=lambda: choose_File_background(), width=bwidth)
cf2_Button_img.grid(row=1, column=0)
cl2_Button_img = Button(iFrame2, text="Clear", command=lambda: clear_background(), width=bwidth)
cl2_Button_img.grid(row=1, column=1)


#Frame result : iFrame3
iFrame3 = Frame(tab_img_img, width=550, height=550, bg=bgcolor)
iFrame3.grid(row=0, column=1, rowspan=2, padx=25, pady=15)
iFrame3.grid_propagate(0)
label_result = Label(iFrame3, image=holder_result)
label_result.grid(row=0, column=0, columnspan=2, padx=lpadx, pady=lpady)
sm_Button = Button(iFrame3, text="Submit", command=lambda: submit(), width=bwidth)
sm_Button.grid(row=1, column=0, pady = 10)
clr_Button = Button(iFrame3, text="Clear", command=lambda: clear_result(), width=bwidth)
clr_Button.grid(row=1, column=1, pady =10)
scale_H_img = Scale(iFrame3, variable=H_thresh, from_=0, to=179, orient=HORIZONTAL, length=400, label ="Adjust H threshold")
scale_H_img.grid(row=2, column=0, padx=20, pady=15, columnspan=2)
scale_S_img = Scale(iFrame3, variable=S_thresh, from_=0, to=255, orient=HORIZONTAL, length=400, label="Adjust S threshold")
scale_S_img.grid(row=3, column=0, padx=20, pady=15, columnspan=2)


tab_video_img = ttk.Frame(tab_Panel, style="tFrame.TFrame")
background_label2 = Label(tab_video_img, image=background_frame)
background_label2.place(x=0, y=0, relwidth=1, relheight=1)
#Frame chromakey image : vFrame1
vFrame1 = Frame(tab_video_img, width=550, height=300, bg=bgcolor)
vFrame1.grid(row=0, column=0, padx=25, pady=15)
vFrame1.grid_propagate(0)
label_video = Label(vFrame1, image=holder_chroma_vid)
label_video.grid(row=0, column=0, columnspan=2, padx=lpadx, pady=lpady)
cf1_Button_video = Button(vFrame1, text="Choose file", command=lambda: choose_File_video(), width=bwidth)
cf1_Button_video.grid(row=1, column=0)
cl1_Button_video = Button(vFrame1, text="Clear", command=lambda: set_stopcode(), width=bwidth)
cl1_Button_video.grid(row=1, column=1)

#Frame background image: vFrame2
vFrame2 = Frame(tab_video_img, width=550, height=300, bg=bgcolor)
vFrame2.grid(row=1, column=0, padx=25, pady=15)
vFrame2.grid_propagate(0)
labelv_background = Label(vFrame2, image=holder_background_img)
labelv_background.grid(row=0, column=0, columnspan=2, padx=lpadx, pady=lpady)
cf2_Button_video = Button(vFrame2, text="Choose file", command=lambda: choose_File_background_video(), width=bwidth)
cf2_Button_video.grid(row=1, column = 0)
cl2_Button_video = Button(vFrame2, text="Clear", command=lambda: clear_background_video(), width=bwidth)
cl2_Button_video.grid(row=1, column=1)


#Frame result : vFrame3
vFrame3 = Frame(tab_video_img, width=550, height=550, bg=bgcolor)
vFrame3.grid(row=0, column=1, rowspan=2, padx=25, pady=15)
vFrame3.grid_propagate(0)
labelv_result = Label(vFrame3, image=holder_result)
labelv_result.grid(row=0, column=0, columnspan=2, padx=lpadx, pady=lpady)
sm_Button_video = Button(vFrame3, text="Submit", command=lambda: submit_video(), width=bwidth)
sm_Button_video.grid(row=1, column=0, pady=15)
clr_Button_video = Button(vFrame3, text="Clear", command=lambda: set_stopcode(), width=bwidth)
clr_Button_video.grid(row=1, column=1, pady=15)
scale_H_vid = Scale(vFrame3, variable=H_thresh, from_=0, to=179, orient=HORIZONTAL, length=400, label ="Adjust H threshold")
scale_H_vid.grid(row=2, column=0, padx=20, pady=15, columnspan=2)
scale_S_vid = Scale(vFrame3, variable=S_thresh, from_=0, to=255, orient=HORIZONTAL, length=400, label="Adjust S threshold")
scale_S_vid.grid(row=3, column=0, padx=20, pady=15, columnspan=2)


tab_webcam_img = ttk.Frame(tab_Panel, style="tFrame.TFrame")
background_label3 = Label(tab_webcam_img, image=background_frame)
background_label3.place(x=0, y=0, relwidth=1, relheight=1)
#Frame chromakey webcam : wFrame1
wFrame1 = Frame(tab_webcam_img, width=550, height=300, bg="skyblue")
wFrame1.grid(row=0, column=0, padx=25, pady=15)
wFrame1.grid_propagate(0)
label_webcam = Label(wFrame1, image=holder_webcam)
label_webcam.grid(row=0, column=0, columnspan=2, padx=lpadx, pady=lpady)
cf1_Button_webcam = Button(wFrame1, text="Enable webcam", command=lambda: enable_Webcam(), width=bwidth)
cf1_Button_webcam.grid(row=1, column=0)
cl1_Button_webcam = Button(wFrame1, text="Disable webcam", command=lambda: disable_Webcam(), width=bwidth)
cl1_Button_webcam.grid(row=1, column=1)


#Frame background image: wFrame2
wFrame2 = Frame(tab_webcam_img, width=550, height=300, bg=bgcolor)
wFrame2.grid(row=1, column=0, padx=25, pady=15)
wFrame2.grid_propagate(0)
labelw_background = Label(wFrame2, image=holder_background_img)
labelw_background.grid(row=0, column=0, columnspan=2, padx=lpadx, pady=lpady)
cf2_Button_webcam = Button(wFrame2, text="Choose file", command=lambda: choose_File_background_webcam(), width=bwidth)
cf2_Button_webcam.grid(row=1, column = 0)
cl2_Button_webcam = Button(wFrame2, text="Clear", command=lambda: clear_background_webcam(), width=bwidth)
cl2_Button_webcam.grid(row=1, column = 1)


#Frame result : wFrame3
wFrame3 = Frame(tab_webcam_img, width=550, height=550, bg=bgcolor)
wFrame3.grid(row=0, column=1, rowspan=2, padx=25, pady=15)
wFrame3.grid_propagate(0)
labelw_result = Label(wFrame3, image=holder_result)
labelw_result.grid(row=0, column=0, columnspan=2, padx=lpadx, pady=lpady)
sm_Button_webcam = Button(wFrame3, text="Submit", command=lambda: submit_webcam(), width=bwidth)
sm_Button_webcam.grid(row=1, column=0, columnspan=2 , pady=15)
scale_H_web = Scale(wFrame3, variable=H_thresh, from_=0, to=179, orient=HORIZONTAL, length=400, label ="Adjust H threshold")
scale_H_web.grid(row=2, column=0, padx=20, pady=15, columnspan=2)
scale_S_web = Scale(wFrame3, variable=S_thresh, from_=0, to=255, orient=HORIZONTAL, length=400, label="Adjust S threshold")
scale_S_web.grid(row=3, column=0, padx=20, pady=15, columnspan=2)

tab_Panel.add(tab_img_img, text='Image and image')
tab_Panel.add(tab_video_img, text='Video and image')
tab_Panel.add(tab_webcam_img, text='Webcam and image')
tab_Panel.pack(expand=1, fill="both")

root.mainloop()

