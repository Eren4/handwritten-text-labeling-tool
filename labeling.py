import cv2
import numpy as np
import time
import tkinter as tk
from PIL import ImageTk, Image
import os

# THIS PROGRAM DOESN'T CONTAIN THE TRANSFORM FUNCTION

def process_img(img):
  processed_img = cv2.resize(img, None, fx=1.6, fy=1.6, interpolation=cv2.INTER_CUBIC)
  processed_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  processed_img = cv2.adaptiveThreshold(processed_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 17, 15)
  return processed_img

def thresholding(image):
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY_INV) # ret, thresh = cv2.threshold(img_gray, 80, 255, cv2.THRESH_BINARY_INV)
    return thresh

def check_dir(dir_name):
    if os.path.exists(dir_name) == False:
        os.mkdir(dir_name)

# create the necessary folders if they don't exist
check_dir("words")
check_dir("lines")

# Get the filename of the form from the user
input_filename = input("Enter the filename of the handwritten form: ")
splitted = input_filename.split(".")
image_filename = splitted[0] # if input_filename was form001.jpg, image_filename will be form001

# process the image into more readable form
try:
    img = cv2.imread(input_filename)
    img = process_img(img)
except:
    print("An exception occurred.")
    time.sleep(7)
    exit()

img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

h, w, c = img.shape

# resizing the image
if w > 1000:
    new_w = 1000
    ar = w/h # aspect ratio
    new_h = int(new_w/ar)

    img = cv2.resize(img, (new_w, new_h), interpolation = cv2.INTER_AREA)
    
thresh_img = thresholding(img)

# apply dilation for detecting the lines
kernel = np.ones((3, 85), np.uint8)
dilated = cv2.dilate(thresh_img, kernel, iterations=1)

(contours, hierarchy) = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
sorted_contours_lines = sorted(contours, key = lambda ctr : cv2.boundingRect(ctr)[1]) # (x, y, w, h)

img2 = img.copy()
lines_list = []

# surround each line with bounding boxes and add them to the lines list
for ctr in sorted_contours_lines:
    x, y, w, h = cv2.boundingRect(ctr)
    if(w < 100): # preventing wrongly detected parts
        continue
    cv2.rectangle(img2, (x, y), (x+w, y+h), (40, 100, 250), 2)
    lines_list.append([x, y, x+w, y+h])

# saving each detected line to the lines/ folder
check_dir("lines/" + image_filename)
saving_counter = 0
for line in lines_list:
    roi = img[line[1]:line[3], line[0]:line[2]] # roi will be the box of the line
    saving_counter += 1
    line_file_name = image_filename + "-" + str(saving_counter) + ".png"
    line_file_location = "lines/" + image_filename + "/" + line_file_name
    cv2.imwrite(line_file_location, roi)

# detecting the words in each line
kernel = np.ones((3, 15), np.uint8)
words_list = []
line_counter = 0
print("Please check the opened window and write the corresponding words as an input below.")

check_dir("words/" + image_filename)
with open("turkish_words.txt", 'a', encoding="UTF-8") as file:
    for line in lines_list:
        roi_line = img[line[1]:line[3], line[0]:line[2]]
        line_counter += 1
        line_file_name = image_filename + "-" + str(line_counter)

        thresh_line = thresholding(roi_line)
        dilated_line = cv2.dilate(thresh_line, kernel, iterations=1)

        (contours, hierarchy) = cv2.findContours(dilated_line.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        sorted_contours_words = sorted(contours, key = lambda ctr : cv2.boundingRect(ctr)[0]) # (x, y, w, h)

        roi_line2 = roi_line.copy()
        word_counter = 0
        for ctr in sorted_contours_words:
            x, y, w, h = cv2.boundingRect(ctr)

            if cv2.contourArea(ctr) < 325: # preventing wrongly detected parts
                continue

            cv2.rectangle(roi_line2, (x, y), (x+w, y+h), (40, 100, 250), 1)
            words_list.append([x, y, x+w, y+h])

            # Saving each word as a png
            my_word = [x+1, y+1, x+w-1, y+h-1]
            my_word_roi = roi_line2[my_word[1]:my_word[3], my_word[0]:my_word[2]]
            # my_word_roi = cv2.resize(my_word_roi, (150, 40)) # uncomment this line if you want to save the words in the same size
            word_counter += 1
            word_file_name = line_file_name + "-" + str(word_counter) + ".png"
            word_file_location = "words/" + image_filename + "/" + word_file_name
            cv2.imwrite(word_file_location, my_word_roi)

            # open a window to show the word
            root = tk.Tk()
            root.title(word_file_name)
            root.geometry("400x100+300+50")

            frame = tk.Frame(root, width=400, height=100)
            frame.grid(row=0, column=0, sticky="NW")

            tk_word_label = ImageTk.PhotoImage(Image.open(word_file_location))
            tk_my_label = tk.Label(root, image=tk_word_label)
            tk_my_label.place(relx=0.5, rely=0.5, anchor="center")

            # Labeling each word to the txt file
            status_input = input("Is " + word_file_name + " segmented correctly? [y/n]: ")
            status = "ok"
            while(status_input != "y" and status_input != "n" and status_input != ""):
                print("Please type y or n for answering")
                status_input = input("Is " + word_file_name + " segmented correctly? [y/n]: ")
                
            if(status_input == "n"):
                status = "err"
            label = input("Enter the label of " + word_file_name + ": ")
            row = [word_file_location, status, label]
            row = " ".join(row)
            file.write(row + "\n")
            try:
                root.destroy()
            except:
                print("Please do not close the window.")


# automatically labeling the lines from the words txt file
words = open("turkish_words.txt", "r", encoding="UTF-8").readlines()
line_status_label = []
filename_list = []

for line in words:

    if line.startswith("#"):
        continue
    
    line_split = line.split(" ")
    
    if(line_split[0].startswith(("words/" + image_filename).rstrip(".jpg"))):
        word_correctness = line_split[1]
        file_location = line_split[0]
        label = line_split[-1].rstrip('\n')
        filename = file_location.split("/")[2]
        filename_list.append(filename)
        line_number = filename.split("-")[1]
        line_status_label.append([line_number, word_correctness, label])

# create a list to determine how many lines are there
number_of_lines = []
for i in range(len(line_status_label)):
    number_of_lines.append(line_status_label[i][0])

number_of_lines = list(dict.fromkeys(number_of_lines)) # remove duplicates

# generating the line by adding the words together
full_sentence = ''
prev_line = 1
sentence_list = []
element_counter = 0
status_list = []
for element in line_status_label:
    line_number = int(element[0])
    label = element[-1]
    word_status = element[1]

    if(line_number != prev_line):
        full_sentence = full_sentence.rstrip(" ")
        if("err" in status_list):
            sentence_list.append(["err", full_sentence])
            status_list = []
        else:
            sentence_list.append(["ok", full_sentence])
            status_list = []
        full_sentence = ''
    
    if(word_status == "err"):
        status_list.append(word_status)
    
    full_sentence += label + " "
    prev_line = line_number
    element_counter += 1

    if(element_counter == len(line_status_label)):
        full_sentence = full_sentence.rstrip(" ")
        if("err" in status_list):
            sentence_list.append(["err", full_sentence])
            status_list = []
        else:
            sentence_list.append(["ok", full_sentence])
            status_list = []
        break

# create a list of file locations
file_location_list = []
for element in filename_list:
    split = element.split("-")
    line_name = split[0] + "-" + split[1] + ".png"
    line_location = "lines/" + image_filename + "/" + line_name
    file_location_list.append(line_location)

file_location_list = list(dict.fromkeys(file_location_list)) # remove duplicates

# concatenate line path, status and label together for appending to the lines txt file
concatenated = []
for i in range(len(file_location_list)):
    sentence = sentence_list[i][1].replace(" ", "|")
    sentence_status = sentence_list[i][0]
    concatenated.append([file_location_list[i], sentence_status, sentence])

# append the lines to the lines txt file
with open("turkish_lines.txt", "a", encoding="UTF-8") as file:
    for element in concatenated:
        element = " ".join(element)
        file.write(element + "\n")

print("Labeling successfully completed. Please check turkish_words.txt and turkish_lines.txt")
time.sleep(7)