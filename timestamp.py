import os
import datetime
import csv
import time

def write_timestamp(timestamp_file):
    #write timstamp file
    with open(timestamp_file, 'w') as file:
        file.write(str(current_date)) 

def flush_data():
    #remove the content of SUBS.csv
    with open('SUBS.csv', mode='r', newline='') as file:
        rows = list(csv.reader(file, delimiter=';', quotechar='"'))
    with open('SUBS.csv', mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=';', quotechar='"')
        for row in rows:
            last_comment_date = datetime.datetime.strptime(row[2],"%Y-%m-%d").date()
            if (current_date-last_comment_date).days < 7:
                writer.writerow(row)
    
def read_timestamp(file_timestamp):
    #open the file, read the last update date
    with open(file_timestamp, 'r') as file:
        last_update_date = file.readline().strip()
        date_from_file = datetime.datetime.strptime(last_update_date,"%Y-%m-%d").date()
        
        #determine the difference
        difference = (current_date-date_from_file).days
        print("Days since last data removal:", difference)
        
        #select the right mode
        if difference >= 14:
            update = True
        else:
            update = False   
    
    return update

def check_record_exists(channel_id, display):
    #check if channelID already exists
    exists = False
    try:
        with open('SUBS.CSV', 'r') as file:
            reader = csv.reader(file, delimiter=';', quotechar='"')
            for row in reader:  
                if channel_id in row:
                    exists = True    
                    break      
    except FileNotFoundError:
        print()
        if display == True:
            print("CSV file will be created shortly...")

    return exists

current_date = datetime.date.today()