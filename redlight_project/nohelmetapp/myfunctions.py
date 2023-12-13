from ultralytics import YOLO
import cv2
import cvzone
import math
import datetime
import numpy as np  
import pandas as pd

# modelv8_1 = YOLO("helmet1.pt")
# modelv8_2 = YOLO("helmet2.pt")

classNames1 = ["helmet", "null", "plate","rider"]
classNames2 = ["helmet", "license_plate", "motorcyclist"]

# def img_classify(frame):

# 	check = 0
# 	break_loop = False

# 	results1 = modelv8_1(frame, stream=True)
# 	for r in results1:
# 		boxes = r.boxes
# 		for box in boxes:
# 			cls = box.cls[0]
# 			conf = math.ceil((box.conf[0] * 100)) / 100
# 			if classNames1[int(cls)] == 'helmet' and conf>=0.4:
# 				check += 1
# 				break_loop = True
# 				break

# 		if break_loop:
# 			break

# 	break_loop = False

# 	results2 = modelv8_2(frame, stream=True)

# 	for r in results2:
# 		boxes = r.boxes
# 		for box in boxes:
# 			cls = box.cls[0]
# 			conf = math.ceil((box.conf[0] * 100)) / 100
# 			if classNames2[int(cls)] == 'helmet' and conf>=0.4:
# 				check += 1
# 				break_loop = True
# 				break

# 		if break_loop:
# 			break

# 	if check == 2 or check ==1:
# 		return [True, 0]
	
# 	else:
# 		return [False, 0]


def inside_box(big_box, small_box):
	x1 = small_box[0] - big_box[0]
	y1 = small_box[1] - big_box[1]
	x2 = big_box[2] - small_box[2]
	y2 = big_box[3] - small_box[3]
	return not bool(min([x1, y1, x2, y2, 0]))

def img_classify(rider,helmetlist,nohelmetlist):

    check = 0
    helmetcheck = False
    nohelmetcheck = False

    for hl in helmetlist:
        if inside_box(rider,hl):
            check += 1
            helmetcheck = True
            break
    
    for nhl in nohelmetlist:
        if inside_box(rider,nhl):
            nohelmetcheck = True
            check += 1
            break

    if (helmetcheck and nohelmetcheck) or helmetcheck:
        return [True, 0]

    if nohelmetcheck:
        return [False, 1]

    else:
        return [True, 0]


# Function to compare current time with stored timestamp and add rows to nohelmet_data

def extract_and_add_rows(df, target_df):
    for index, row in df[df['helmet'] == False].iterrows():
        id_to_add = row['ID']
        
        if id_to_add in target_df['ID'].values:
            target_index = target_df.index[target_df['ID'] == id_to_add][0]
            target_df.at[target_index, 'Rider'] = row['Rider']
            
            if pd.isnull(target_df.at[target_index, 'number_plate']):
                target_df.at[target_index, 'number_plate'] = row['number_plate']
        else:
            row_to_add = pd.DataFrame([[row['Rider'], row['number_plate'], row['ID']]], columns=['Rider', 'number_plate', 'ID'])
            target_df = target_df.append(row_to_add, ignore_index=True)
    
    return target_df