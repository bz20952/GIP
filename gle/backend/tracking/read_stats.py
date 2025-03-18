import json

with open('test.json', 'r') as f:
    data = json.load(f)

for key in data.keys():
    print('Task ' + key)
    print('Time taken: ' + str(data[key]['endTime'] - data[key]['startTime']) + 's')
    print('Attempts: ' + str(data[key]['attempts']))
    print('\n')