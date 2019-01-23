# filename_convert.py
#
# Iterate over a directory and process its filenames into a text file


import os

directory = "./images/fighter_icons"
char_list = []

fighter_file = "fighters.txt"
file = open(fighter_file, 'w')

for filename in os.listdir(directory):
    split_file = filename.split(".")
    if split_file[0].find("_") == -1:
        # char_list.append(split_file[0].capitalize())
        file.write(split_file[0].capitalize() + "\n")
    else:
        split_name = split_file[0].split("_")
        cap_name = ""
        for word in split_name:
            cap_name += word.capitalize() + " "
        # char_list.append(cap_name.rstrip())
        file.write(cap_name.rstrip() + "\n")


file.close()

