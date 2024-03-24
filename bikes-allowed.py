import sys
import os
import csv
import io

COLOR_RED   = "\033[1;31m"
COLOR_GREEN = "\033[0;32m"
COLOR_RESET = "\033[0;0m"

def convert_file():
    if len(sys.argv) < 2:
        print(COLOR_RED + "No file provided!" + COLOR_RESET)
        exit()
    filepath = sys.argv[1]
    file_type = os.path.splitext(filepath)[1]
    if not os.path.isfile(filepath) or not ".txt" in file_type:
        print(COLOR_RED + "Input is not valid! Please input trips.txt." + COLOR_RESET)
        exit()
    make_new_file(filepath)        
    
def make_new_file(filepath):
    with open(filepath, "rb") as file_raw:
        trips_txt = io.TextIOWrapper(file_raw)
        csv_file = csv.DictReader(trips_txt)
        csv_list = list(csv_file)
        if "bikes_allowed" not in csv_file.fieldnames:
            print(COLOR_RED + "No bikes_allowed column detected. The operation cannot be performed." + COLOR_RESET)
            return
        if all(row["bikes_allowed"] == "1" for row in csv_list): 
            print(COLOR_RED + "Values for bikes_allowed are already set to 1. Exiting operation." + COLOR_RESET)
            return
        file_name = "trips_bikes_allowed.txt"
        if os.path.exists(file_name):
            print(COLOR_RED + "File with name " + file_name + " already exists in directory; cannot create a new one. Move this file and try again." + COLOR_RESET)
            return
        new_file = open(file_name, "w")
        new_csv_writer = csv.DictWriter(new_file, fieldnames=csv_file.fieldnames)
        new_csv_writer.writeheader()
        for row in csv_list:
            row["bikes_allowed"] = "1"
            new_csv_writer.writerow(row)
        new_file.close()
        print(COLOR_GREEN + "Exported " + file_name + " with all bikes_allowed values set to 1." + COLOR_RESET)

if __name__ == "__main__":
    convert_file()
