import time

def remove_comments(lines):
    updated_lines = []
    for line in lines:
        if(line.startswith("#")):
            continue
        updated_lines.append(line)
        
    return updated_lines

def create_label_list(lines):
    label_list = []
    lines = remove_comments(lines)
    for line in lines:
        splitted_line = line.split(" ")
        label = splitted_line[-1].rstrip("\n")
        label_list.append(label)

    return label_list

def check_validity(lines, file_input):
    if(lines[0].startswith("#") != True):
        print("ERROR - " + file_input + " is not a valid label file")
        time.sleep(7)
        exit()

def check_file(file_input):
    try:
        with open(file_input, "r", encoding="UTF-8") as file:
            lines = file.readlines()
            return lines
    except FileNotFoundError:
        print("ERROR - " + file_input + " could not be found")
        time.sleep(7)
        exit()

file_input1 = input("Please enter the first label file: ")
file_input2 = input("Please enter the second label file: ")

lines1 = check_file(file_input1)
lines2 = check_file(file_input2)

check_validity(lines1, file_input1)
check_validity(lines2, file_input2)

label_list1 = create_label_list(lines1)
label_list2 = create_label_list(lines2)

lines1 = remove_comments(lines1)
lines2 = remove_comments(lines2)

concatenated = []
for i in range(len(label_list1)):
    concatenated.append([label_list1[i], label_list2[i]])

errors = []
for i in range(len(concatenated)):
    if concatenated[i][0] != concatenated[i][1]:
        errors.append([lines1[i].rstrip("\n"), lines2[i].rstrip("\n")])
        print("Error in:")
        print(lines1[i] + "" + lines2[i])

with open("label_errors.txt", "w", encoding="UTF-8") as error_file:
    error_file.write(file_input1 + "\n" + file_input2 + "\n\n")
    for i in range(len(errors)):
        for j in range(2):
            error_file.write(errors[i][j] + "\n")
        error_file.write("\n")

if(len(errors) == 0):
    print("No errors found!")
else:
    print("Please check label_errors.txt")

time.sleep(10)