import json
import pandas as pd
import glob


tracking = []

for file in glob.glob('./*.json'):
    with open(file, 'r') as f:
        track = json.load(f)

    for key in track.keys():
        row = {}
        row['Serial Number'] = file.replace('.\\', '').split('.')[0]
        row['Task'] = key
        row['Time Taken'] = track[key]['endTime'] - track[key]['startTime']
        row['Attempts'] = track[key]['attempts']
        tracking.append(row)

tracking_df = pd.DataFrame(tracking, columns=['Serial Number', 'Task', 'Time Taken', 'Attempts'])
tracking_df.to_csv('tracking.csv', index=False)