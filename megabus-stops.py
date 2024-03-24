import sys
import os
import csv
import io
import zipfile

COLOR_RED   = "\033[1;31m"
COLOR_GREEN = "\033[0;32m"
COLOR_RESET = "\033[0;0m"

def convert_file():
    if len(sys.argv) < 2:
        print(COLOR_RED + "No file provided!" + COLOR_RESET)
        exit()
    filepath = sys.argv[1]
    file_type = os.path.splitext(filepath)[1]
    if not ".zip" in file_type:
        print(COLOR_RED + "Invalid input. Ensure input is a zip file." + COLOR_RESET)
        exit()
    gtfs_zipped = zipfile.ZipFile(filepath)
    find_difference(gtfs_zipped)

def find_difference(gtfs_zipped):
    with gtfs_zipped.open("stop_times.txt", "r") as file_raw:
        txt = io.TextIOWrapper(file_raw)
        csv_file = csv.DictReader(txt)
        csv_list = list(csv_file)
        stop_times_stop_ids = set()
        for row in csv_list:
            stop_id = row["stop_id"]
            stop_times_stop_ids.add(stop_id)
    with gtfs_zipped.open("stops.txt", "r") as file_raw:
        txt = io.TextIOWrapper(file_raw)
        csv_file = csv.DictReader(txt)
        csv_list = list(csv_file)
        stops_stop_ids = set()
        for row in csv_list:
            stop_id = row["stop_id"]
            stops_stop_ids.add(stop_id)
    difference = stops_stop_ids.difference(stop_times_stop_ids)
    make_new_file(gtfs_zipped, difference)

def make_new_file(gtfs_zipped, difference):
    with gtfs_zipped.open("stops.txt", "r") as file_raw:
        txt = io.TextIOWrapper(file_raw)
        csv_file = csv.DictReader(txt)
        csv_list = list(csv_file)
        file_name = "stops.txt"
        if os.path.exists(file_name):
            print(COLOR_RED + "File with name " + file_name + " already exists in directory; cannot create a new one. Move this file and try again." + COLOR_RESET)
            return
        new_file = open(file_name, "w")
        new_csv_writer = csv.DictWriter(new_file, fieldnames=csv_file.fieldnames)
        new_csv_writer.writeheader()
        for row in csv_list:
                if row["stop_id"] not in difference or row["location_type"] == "1" :
                    new_csv_writer.writerow(row)      
        new_file.close()
        print(COLOR_GREEN + "Exported " + file_name + " with updated stop_id values." + COLOR_RESET)

if __name__ == "__main__":
    convert_file()

