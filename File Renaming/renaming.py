import os
import time

def main():
    file_list = os.listdir(".")
    splitted_list = []

    for file in file_list:
        splitted_file = file.split(".")

        if splitted_file[1] == "py":
            file_list.remove(file)
            continue

        splitted_list.append(splitted_file[0])

    renamed_list = []
    form_name = "form"
    one_digit = "00"
    two_digit = "0"
    counter = 1

    for element in splitted_list:
        if len(str(counter)) == 1: # if it is single digit
            form_number = one_digit + str(counter) + ".jpg"
            form_name += form_number
            renamed_list.append(form_name)
        elif len(str(counter)) == 2: # if it is two digit
            form_number = two_digit + str(counter) + ".jpg"
            form_name += form_number
            renamed_list.append(form_name)
        else: # three digit
            form_number = str(counter) + ".jpg"
            form_name += form_number
            renamed_list.append(form_name)
        counter += 1
        form_number = ""
        form_name = "form"

    for i in range(len(file_list)):
        os.rename(os.path.join(".", file_list[i]), os.path.join(".", renamed_list[i]))

    print("Successfully renamed the files in the current directory as formxxx.")
    time.sleep(7)

answer = input("WARNING\nALL THE FILES IN YOUR CURRENT FOLDER WILL BE RENAMED.\nDo you wish to proceed? [y/n]: ")
if(answer == "y" or answer == "Y"):
    main()
else:
    exit()