# PlexExportCSV
This script connects to your local Plex Media server and exports metadata from your libraries to a CSV file.<br />
This file can be imported to Excel or Google sheets to inspect the information about your library files. 

Currently works for your movie libraries. TV shows coming soon.

Made possible by the great work of the guys at [Python-PlexAPI](https://python-plexapi.readthedocs.io/en/latest/index.html)

Created by creativeWaltz and mleo40
 
## Requirements
### Python 3
   * [MacOS](https://installpython3.com/mac/)
   * [Windows](https://installpython3.com/windows/)
   * [Linux](https://installpython3.com/linux/)  
   * [Chromebook](https://installpython3.com/chromebook/)
   
### Python-PlexAPI
[plexapi](https://python-plexapi.readthedocs.io/en/latest/index.html)
 ```
 pip3 install plexapi
 ```
### Plex Media Server
You'll need a running [Plex](https://www.plex.tv) server on your local network.


## Usage:
### Create config file
Create/Edit the file ```plexExportCSV_config.py```.Add the following lines and save.
```
PLEX_URL="http://192.168.0.2:32400"
PLEX_TOKEN="xxxxxxxxxxxxxxxxxxxx"
```
### How to get your token
1. Go to your Plex server and select one of your Film libraries. Select the three dots on any film and select 'Get Info'
![1-get-info](https://user-images.githubusercontent.com/71404312/111868394-9049d680-8971-11eb-97a1-04d060c6f8fb.jpg)

2. Select 'View XML' in the bottom left corner
![2-view-xml](https://user-images.githubusercontent.com/71404312/111868420-a22b7980-8971-11eb-85a0-8e73c3f8d5d4.jpg)

3. A new page will open. Click on the URL and navigate to the end. You will find your Authentication token.
![3-get-token](https://user-images.githubusercontent.com/71404312/111868774-ba9c9380-8973-11eb-9aa8-af47071d2269.jpg)

4. Add the authentication token to the ```plexExportCSV_config.py``` you created.

### Running the script
1. Ensure ```plexExportCSV.py``` and ```plexExportCSV_config.py``` are in the same directory/folder
2. Run ```plexExportCSV.py``` with the command ```$ python3 plexExportCSV_config.py```
3. You can find the file in the same directory/folder as the scipt

### Limitations
The script currently assumes that each of your movie files has only one video file in the container. Not an issue for mp4's I believe but possibly for mkvs.




