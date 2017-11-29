# screengrabber
Using a CSV file with website links, this script grabs a screenshot of each site, adds title and website url and posts it all to WordPress

### Requirements
This has so far only been tested on Windows 7 with Python 3.5 - some modifications might need to take place in order for this to work on other systems.

- Screengrabber requires [Python](https://python.org/) v3+ to run.
- This script also uses [chromedriver.exe](https://sites.google.com/a/chromium.org/chromedriver/home) to run

Screengrabber also uses a few different dependencies:
```sh
pip install selenium
pip install python-wordpress-xmlrpc
pip install pillow
```

### Installation
1. Simply clone screengrabber.py and save it in a folder of your choosing. 
2. Then create a subfolder in the directory called "img"
3. Download [chromedriver.exe](https://sites.google.com/a/chromium.org/chromedriver/home) and place in root folder where screengrabber.py also exists
4. Configure details in screengrabber.py

### Configuration
To configure screengrabber.py line 8 and line 18 needs to modified.

1. First you need to setup your WordPress URL, USERNAME and PASSWORD on line 8:
```
wp = Client('http://localhost/wordpress/xmlrpc.php', 'USERNAME', 'PASSWORD')
```

2. Then go to line 18 and change:
```
    # CHANGE THIS VARIABLE TO YOUR CORRECT SYSTEM FOLDER BUT DONT CHANGE THE LAST BIT
    imagelocation = "C:/CHANGE/THIS/PATH/img/%s.jpg" %idx
```
Important: Do not change the last bit containing `%s.jpg" %idx`

3. All done! Run the script by using your command line or create a .BAT file
```
python screengrabber.py
```
