### handwritten-text-labeling-tool  
# labeling.py  
This script performs line and word segmentation on a handwritten form and labels each word and line into txt files.  
  
When the script is opened, it will ask the user for the handwritten filename (with its extension such as jpg or png).  
  
Then it will create lines and words folder where the segmented lines and words will be stored.  
  
For each word, a small window will appear so that the user can see what is written in there.  
  
If there is a problem in the word segmentation, the user will answer n to the question.  
  
If it is correctly segmented and the word is readable, the user can either press the enter key or type y.  
  
Then, the user will enter the label of the word.  
  
After labeling all words, each line and word will be stored into the mentioned folders, and two txt files which contain the labels of the lines and words will be created.
  
# label-comparator.py  
This script compares the label parts of two words.txt files and tells the user if there is a mismatch in them.  
The mismatched lines are exported into label_errors.txt  
  
# renaming.py  
This program renames all the files in the current working directory into form001, form002, form003...  
Please use this script with caution because there is no turning back after renaming your files.
