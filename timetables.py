import sys
import os
import zipfile
import pandas as pd

COLOR_RED   = "\033[1;31m"
COLOR_GREEN = "\033[0;32m"
COLOR_RESET = "\033[0;0m"

def process_input():
    if len(sys.argv) < 2:
        print(COLOR_RED + "No file provided!" + COLOR_RESET)
        exit()
    filepath = sys.argv[1]
    file_type = os.path.splitext(filepath)[1]
    if not ".zip" in file_type:
        print(COLOR_RED + "Invalid input. Ensure input is a zip file." + COLOR_RESET)
        exit()
    gtfs_zipped = zipfile.ZipFile(filepath)
    convert_file(gtfs_zipped)

def convert_file(gtfs_zipped):
    with gtfs_zipped.open("directions.txt", "r") as dx:
        dx_data = pd.read_csv(dx)
    with gtfs_zipped.open("timetables.txt", "r") as tt:
        tt_data = pd.read_csv(tt)
    merged_data = pd.merge(dx_data,tt_data,how="right",on=["route_id","direction_id"]).drop(("direction_label"),axis=1)
    df = pd.DataFrame(merged_data).rename(columns={"direction": "direction_label"})
    file_name = "timetables_new.txt"
    if os.path.exists(file_name):
            print(COLOR_RED + "File with name " + file_name + " already exists in directory; cannot create a new one. Move this file and try again." + COLOR_RESET)
            exit()
    path = os.path.join(file_name)
    with open(path,"a") as f:
        str(df.to_csv("timetables_new.txt", sep=",", index=False))
        f.close()
        print(COLOR_GREEN + "Exported " + file_name + " with updated direction_label values." + COLOR_RESET)


if __name__ == "__main__":
    process_input()

