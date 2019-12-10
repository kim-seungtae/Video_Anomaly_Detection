import pandas as pd
import numpy as np
import datetime as dt
import math
import re
import struct
import subprocess
import sys
import os
import boto3
class exportDrivingRecords:
    def __init__(self):
        pass
    def set_driving_record_of_event(self, file_name):

        event_video_file = open(file_name, "rb")
        driving_record_of_event_df = self.set_driving_record(event_video_file, file_name)
        return driving_record_of_event_df

    def set_driving_record(self, mp4_file, file_name):
        accident_df = pd.DataFrame(columns = ["path", "created_at", "imaged_at", "x", "y", "z", "x'", "y'", "z'", "impulse", "speed", "vector", "lat", "lng"])
        before_data = b''
        imaged_at = 0
        before_x = 0.0
        before_y = 0.0
        before_z = 0.0
        for data in mp4_file.readlines():
            gps_compile = re.compile(b'(\$GPRMC((,[^,]*){12})\*[0-9A-F]{2})')
            gps_matches = gps_compile.findall(data)
            data = before_data + data

            before_data = b''
            if len(gps_matches) >= 1:
                gps_row = gps_matches[0][0]
                gps_info = str(gps_matches[0][1])
                gps_info_list = gps_info.split(',')
                created_date = str(gps_info_list[9])[4:] + "-" + str(gps_info_list[9])[2:4] + "-" + str(gps_info_list[9])[:2]
                created_time = str(gps_info_list[1])[:2] + ":" + str(gps_info_list[1])[2:4] + ":" + str(gps_info_list[1])[4:6]
                row_lat = str(gps_info_list[3])
                row_lng = str(gps_info_list[5])
                created_at = "20" + created_date + " " + created_time
                gps_created_at = dt.datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
                if gps_info_list[2] == "A":
                    lat = float(row_lat[:2]) + (float(row_lat[2:]) / 60)
                    lng = float(row_lng[:3]) + (float(row_lng[3:]) / 60)
                    speed = float(gps_info_list[7]) * 1.8
                    vector = float(gps_info_list[8])
                else:
                    lat = 0
                    lng = 0
                    speed = 0
                    vector = 0
                # print(gps_created_at, lat, lng, speed, vector)
                accelation_compile = re.compile(b'(M(.{2})(.{2})(.{2})(.{2})\x00{7})')
                accelation_matches = accelation_compile.findall(data)
                length_accelation_matches = len(accelation_matches)
                if length_accelation_matches >= 1:
                    term_accelation_matches = 1 / length_accelation_matches
                    accelerations = []
                    for i in range(0, length_accelation_matches):
                        accelation_row = accelation_matches[i][0]
                        accelation_created_at = gps_created_at.replace(microsecond = int((i * term_accelation_matches) * 1000000))
                        # x y z: g-sensor X Y Z
                        x = struct.unpack('h', accelation_matches[i][1])
                        y = struct.unpack('h', accelation_matches[i][2])
                        z = struct.unpack('h', accelation_matches[i][3])
                        t = struct.unpack('h', accelation_matches[i][4])
                        sub_df = pd.DataFrame(columns = ["path", "created_at", "imaged_at", "x", "y", "z", "x'", "y'", "z'",
                                                         "impulse", "speed", "vector", "lat", "lng"])
                        sub_df.loc[0, "path"] = file_name
                        sub_df.loc[0, "created_at"] = accelation_created_at
                        sub_df.loc[0, "imaged_at"] = imaged_at
                        sub_df.loc[0, "lat"] = lat
                        sub_df.loc[0, "lng"] = lng
                        sub_df.loc[0, "speed"] = speed
                        sub_df.loc[0, "vector"] = vector
                        sub_df.loc[0, "x"] = x[0]
                        sub_df.loc[0, "y"] = y[0]
                        sub_df.loc[0, "z"] = z[0]
                        sub_df.loc[0, "x'"] = x[0] - before_x
                        sub_df.loc[0, "y'"] = y[0] - before_y
                        sub_df.loc[0, "z'"] = z[0] - before_z
                        sub_df.loc[0, "impulse"] = math.sqrt(math.pow(x[0] - before_x, 2) + math.pow(y[0] - before_y, 2) + math.pow(z[0] - before_z, 2))
                        # print(math.sqrt(math.pow(x[0] - before_x, 2) + math.pow(y[0] - before_y, 2) + math.pow(z[0] - before_z, 2)))
                        accident_df = accident_df.append(sub_df)
                        imaged_at += 0.05
                        before_x = x[0]
                        before_y = y[0]
                        before_z = z[0]
                else:
                    pass
            else:
                before_data = data
        return accident_df


a=exportDrivingRecords()
name="10하7040_20191117_111926_N_1_앞 20초만 사고영상"
(a.set_driving_record_of_event(name+'.mp4')).to_csv(name + ".csv")




