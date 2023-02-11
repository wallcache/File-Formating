import os

file_location = ''
directory = os.fsencode(file_location)

file_name_list = []

for file in os.listdir(directory):
    file = str(file)
    file_name_list.append(file)

file_name_list.sort(reverse=True)

file_name_list_amended = []

for i in file_name_list:
    file_name_list_amended.append(i[2:-1])

paths_to_remove = []

for file_names in file_name_list_amended:
    if '(1)' in file_names or '(2)' in file_names:
        paths_to_remove.append(f'/{file_names}')
    

for j in paths_to_remove:
    os.remove(j)

########################## DUPES REMOVED, NOW TO USE WHATSAPP DATE TIME TO DATE PHOTOS

from datetime import datetime
import os
import re
import piexif

def absoluteFilePaths(directory):
	for dirpath,_,filenames in os.walk(directory):
		for f in filenames:
			fullPath = os.path.abspath(os.path.join(dirpath, f))
			if re.match(r"^IMG-\d\d\d\d\d\d\d\d-WA\d\d\d\d.*", f) and not re.match(r"^IMG-\d\d\d\d\d\d\d\d-WA\d\d\d\d-ANIMATION.gif", f):
				print(f+" Matched")
				match = re.search("^IMG-(\d\d\d\d)(\d\d)(\d\d)-WA\d\d\d\d.*", f)
				year = match.group(1)
				month= match.group(2)
				day = match.group(3)
				exif_dict = piexif.load(fullPath)
				#Update DateTimeOriginal
				exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = datetime(int(year), int(month), int(day), 4, 0, 0).strftime("%Y:%m:%d %H:%M:%S")
				#Update DateTimeDigitized				
				exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = datetime(int(year), int(month), int(day), 4, 0, 0).strftime("%Y:%m:%d %H:%M:%S")
				#Update DateTime
				exif_dict['0th'][piexif.ImageIFD.DateTime] = datetime(int(year), int(month), int(day), 4, 0, 0).strftime("%Y:%m:%d %H:%M:%S")
				exif_bytes = piexif.dump(exif_dict)
				piexif.insert(exif_bytes, fullPath)
				print("############################")


absoluteFilePaths("")