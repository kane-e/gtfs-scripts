# gtfs-scripts

### scripts for processing GTFS feeds

## syncro-mods

### Purpose
This script performs the following operations that are required for feed compatibility with Syncromatic's Track: <br>
1. Removes all values in the trip_short_name column of trips.txt.<br>
2. Replaces all values in the run_number column with the corresponding values in the block_id column of runcut.txt.<br>
3. Reduces each value in the stop_sequence column of stop_times.txt by 1.

### Usage
Tested with Python 3.9.<br>
```python syncro.py trips.txt runcut.txt stop_times.txt``` <br>
Adjusted files are exported to the current directory as trips_syncro.txt, runcut_syncro.txt, and stop_times_syncro.txt after which the file names can be updated and added to the feed's .zip file to replace the original files. 

## timetables-direction-label

### Purpose
This script references timetables.txt and directions.txt in feed.zip and generates a new timetables.txt with ```direction_label``` values that match the ```direction``` values in directions.txt. This is a solve for the fact that the script Support uses to generates timetables.txt for external GTFS feeds only references the first ```direction_id```:```direction``` pair in directions.txt to create ```direction_label``` values, resulting in incorrect values when there are multiple variations of the ```direction_id```:```direction``` pair.

### Usage
Tested with Python 3.9.<br>
```python3 timetables.py feed.zip``` <br>
Adjusted file is exported to the current directory as timetables_new.txt, after which the file name can be updated and added to the feed's .zip file to replace the original timetables.txt. 

## add-wheelchair-accessible

### Purpose
This script sets all values in the wheelchair_accessible column of trips.txt to 1.

### Usage
Tested with Python 3.9.<br>
```python wheelchair-accessible.py trips.txt``` <br>
Adjusted file is exported to the current directory as trips_wheelchair_accessible.txt, after which the file name can be updated and added to the feed's .zip file to replace the original trips.txt.<br> 
Can be used in conjunction with the add-bikes-allowed script. 

## add-bikes-allowed

### Purpose
This script sets all values in the bike_allowed column of trips.txt to 1.

### Usage
Tested with Python 3.9.<br>
```python bikes-allowed.py trips.txt``` <br>
Adjusted file is exported to the current directory as trips_bikes_allowed.txt, after which the file name can be updated and added to the feed's .zip file to replace the original trips.txt.<br>
Can be used in conjunction with the add-wheelchair-accessible script. 

## westcat-tripid

### Purpose
This script removes all underscores and alpha values from the every instance of trip_id.

### Usage
Tested with Python 3.9.<br>
```python westcat-tripid.py feed.zip```<br>
Adjusted files are exported to the current directory for human review, after which they can be manually added to the feed's .zip file.<br>
Alters trip_ids in trips.txt, runcut.txt, stop_times.txt, and frequencies.txt.<br>

## carta-tripid

### Purpose
This script replaces trip_ids with 6-digit numeric ids starting from the second numerical value of exported trip_id.  

### Usage
Tested with Python 3.9.<br>
```python carta-tripid.py feed.zip```<br>
Adjusted files are exported to the current directory for human review, after which they can be manually added to the feed's .zip file.<br>
Alters trip_ids in trips.txt, runcut.txt, stop_times.txt, and frequencies.txt.<br>
If a trip_id is seen multiple times, the script will stop execution to avoid duplicates. When used with feeds exported from Trillium's GTFS Manager, this could be a sign that the feed contains multiple service periods of the same calendar. 

## megabus-stops

### Purpose
This script removes all stops from stops.txt that are not present stop_times.txt. All stations (which are not present in stops_times.txt) are maintained in the new file.   

### Usage
Tested with Python 3.9.<br>
```python megabus-stops.py feed.zip```<br>
Adjusted stops_txt file is exported to the current directory, after which it can be manually added to the feed's .zip file.<br>

## bcferries-trips

### Purpose
This script produces a new trips.txt file with all block_ids removed and a concated service_id+trip_id for all trips with a trip_short_name.

### Usage
Tested with Python 3.9.<br>
```python bc-trips.py trips.txt```<br>
Adjusted trips.txt file is exported to the current directory for human review, after which it can be used for subsequent post-export modifications.<br>

## remove-trip-short-name

### Purpose
This script removes all values in the trip_short_name column of trips.txt.

### Usage
Tested with Python 3.9.<br>
```python trip-name-remove.py trips.txt``` <br>
Adjusted file is exported to the current directory as trips_syncro.txt, after which the file name can be updated and added to the feed's .zip file to replace the original trips.txt. 

## run-number-to-block-id

### Purpose
This script replaces all values in the run_number column with the corresponding values in the block_id column of runcut.txt.

### Usage
Tested with Python 3.9.<br>
```python run-to-block.py runcut.txt``` <br>
Adjusted file is exported to the current directory as runcut_syncro.txt, after which the file name can be updated and added to the feed's .zip file to replace the original runcut.txt.

## reduce-stop-sequence

### Purpose
This script reduces each value in the stop_sequence column of stop_times.txt by 1.

### Usage
Tested with Python 3.9.<br>
```python stop-sequence-reduce.py stop_times.txt```<br>
Adjusted file is exported to the current directory as stop_times_syncro.txt, after which the file name can be updated and added to the feed's .zip file to replace the original stop_times.txt. 

