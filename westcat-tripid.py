import sys
import os
import csv
import io
import zipfile
import re

COLOR_RED   = "\033[1;31m"
COLOR_GREEN = "\033[0;32m"
COLOR_RESET = "\033[0;0m"

def convert_file():
    if len(sys.argv) < 2:
        print(COLOR_RED + "No file provided!" + COLOR_RESET)
        exit()
    filepath = sys.argv[1]
    file_type = os.path.splitext(filepath)[1]
    if not not ".zip" in file_type:
        print(COLOR_RED + "Invalid input. Ensure input is a .zip file." + COLOR_RESET)
        exit()
    gtfs_zipped = zipfile.ZipFile(filepath)
    files_with_tripid = ["frequencies.txt", "stop_times.txt", "trips.txt", "runcut.txt"]
    for file in files_with_tripid: 
        make_new_file(file, gtfs_zipped)       
    
def make_new_file(file, gtfs_zipped):
    with gtfs_zipped.open(file, "r") as file_raw:
        trips_txt = io.TextIOWrapper(file_raw)
        csv_file = csv.DictReader(trips_txt)
        csv_list = list(csv_file)
        file_name = file
        if os.path.exists(file_name):
            print(COLOR_RED + "File with name " + file_name + " already exists in directory; cannot create a new one. Move this file and try again." + COLOR_RESET)
            return
        new_file = open(file_name, "w")
        new_csv_writer = csv.DictWriter(new_file, fieldnames=csv_file.fieldnames)
        new_csv_writer.writeheader()
        for row in csv_list:
            if "trip_id" in csv_file.fieldnames:
                default_trip_id = row["trip_id"]
                row["trip_id"] = re.sub("[^0-9]+", "", default_trip_id)
                new_csv_writer.writerow(row)
            if "start_trip_id" in csv_file.fieldnames:
                default_start_id = row["start_trip_id"]
                default_end_id = row["end_trip_id"]
                row["start_trip_id"] = re.sub("[^0-9]+", "", default_start_id)
                row["end_trip_id"] = re.sub("[^0-9]+", "", default_end_id)
                new_csv_writer.writerow(row)
        new_file.close()
        print(COLOR_GREEN + "Exported " + file_name + " with updated trip_id values." + COLOR_RESET)

if __name__ == "__main__":
    convert_file()
