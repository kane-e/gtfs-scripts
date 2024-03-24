import sys
import os
import csv
import io
from pathlib import Path

COLOR_RED   = "\033[1;31m"
COLOR_GREEN = "\033[0;32m"
COLOR_RESET = "\033[0;0m"

def convert_files():
    if len(sys.argv) < 2:
        print(COLOR_RED + "No filename provided!" + COLOR_RESET)
        exit()
    filepath = sys.argv[1:4]
    files = [Path(x).name for x in filepath]
    for file in files: 
        if ".txt" not in file:
            print(COLOR_RED + "Input is not a file! Please input txt files." + COLOR_RESET)
            exit()
    for i in filepath: 
        if "runcut.txt" in i:
            runcut_file = i 
            make_new_runcut(runcut_file)
        if "stop_times.txt" in i: 
            stop_times_file = i
            make_new_stop_times(stop_times_file)
        if "trips.txt" in i: 
            trips_file = i
            make_new_trips(trips_file)

def make_new_runcut(runcut_file):
    with open(runcut_file, "rb") as file_raw:
        runcut_txt = io.TextIOWrapper(file_raw)
        csv_file = csv.DictReader(runcut_txt)
        csv_list = list(csv_file)
        if "block_id" not in csv_file.fieldnames:
            print(COLOR_RED + "No block_id column detected. The operation cannot be performed." + COLOR_RESET)
            return
        for row in csv_list:
            if not row["block_id"]:
                print(COLOR_RED + "Missing block_id value(s). The operation cannot be performed." + COLOR_RESET)
                return
        file_name = "runcut_syncro.txt"
        if os.path.exists(file_name):
            print(
                COLOR_RED + "File with name " + file_name + " already exists in directory; cannot create a new one. Move this file and try again." + COLOR_RESET)
            return
        new_file = open(file_name, "w")
        new_csv_writer = csv.DictWriter(new_file, fieldnames=csv_file.fieldnames)
        new_csv_writer.writeheader()
        for row in csv_list:
            row["run_number"] = row["block_id"]
            new_csv_writer.writerow(row)
        new_file.close()
        print(COLOR_GREEN + "Exported " + file_name + " with run_number set to block_id." + COLOR_RESET)

def make_new_stop_times(stop_times_file):
    with open(stop_times_file, "rb") as file_raw:
        stop_times_txt = io.TextIOWrapper(file_raw)
        csv_file = csv.DictReader(stop_times_txt)
        csv_list = list(csv_file)
        if "stop_sequence" not in csv_file.fieldnames:
            print(COLOR_RED + "No stop_sequence column detected. The operation cannot be performed." + COLOR_RESET)
            return
        for row in csv_list:
            if not row["stop_sequence"]:
                print(COLOR_RED + "Input file missing stop_sequence value(s). The operation cannot be performed." + COLOR_RESET)
                return
        for row in csv_list:
            if row["stop_sequence"] <= "0":
                print(COLOR_RED + 'Non-positive value detected in the stop_sequence column. Operation cannot be performed.'+ COLOR_RESET)
                return
        file_name = "stop_times_syncro.txt"
        if os.path.exists(file_name):
            print(COLOR_RED + "File with name " + file_name + " already exists in directory; cannot create a new one. Move this file and try again." + COLOR_RESET)
            return
        new_file = open(file_name, "w")
        new_csv_writer = csv.DictWriter(new_file, fieldnames=csv_file.fieldnames)
        new_csv_writer.writeheader()
        for row in csv_list:
            row["stop_sequence"] = int(row["stop_sequence"]) - 1
            new_csv_writer.writerow(row)
        new_file.close()
        print(COLOR_GREEN + "Exported " + file_name + " with stop_sequence reduced by 1." + COLOR_RESET)

def make_new_trips(trips_file):
    with open(trips_file, "rb") as file_raw:
        trips_txt = io.TextIOWrapper(file_raw)
        csv_file = csv.DictReader(trips_txt)
        csv_list = list(csv_file)
        if "trip_short_name" not in csv_file.fieldnames:
                print(COLOR_RED + "No trip_short_name column detected. The operation cannot be performed." + COLOR_RESET)
                return
        for row in csv_list:
            if not row["trip_short_name"]:
                print(COLOR_RED + "Input file missing trips_short_name value(s). Operation was completed, but ensure this is expected before proceeding." + COLOR_RESET)
                break
        file_name = "trips_syncro.txt"
        if os.path.exists(file_name):
            print(COLOR_RED + "File with name " + file_name + " already exists in directory; cannot create a new one. Move this file and try again." + COLOR_RESET)
            return
        new_file = open(file_name, "w")
        new_csv_writer = csv.DictWriter(new_file, fieldnames=csv_file.fieldnames)
        new_csv_writer.writeheader()
        for row in csv_list:
            row["trip_short_name"] = ""
            new_csv_writer.writerow(row)
        new_file.close()
        print(COLOR_GREEN + "Exported " + file_name + " with trip short names removed." + COLOR_RESET)

if __name__ == "__main__":
    convert_files()
