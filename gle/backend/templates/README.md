# Templates
All the JSON template files in this folder show what information the API recieves (requestFormat.json) and returns (responseFormat.json). The values stated in the JSON files are placeholders. All API endpoints should follow these formats.

## File naming
The API assumes a current file naming convention of:

"[excitation type in CAPS]\_[sampling frequency (kHz)]\_[shaker position index].csv"

The shaker position indices are as follows:
* 0 = 0
* 1 = l/4
* 2 = l/2
* 3 = 3l/4
* 4 = l

This file naming is required for the API to read the correct data file.

## Column naming
The column naming convention of the data files is as shown in 'dataFormat.csv'.