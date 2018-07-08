import urllib.request
import ssl
import re
import os, shutil
from PIL import Image
import urllib.request
import numpy as np
import string 
import os
import platform


set_wallpaper = {
    'Windows': lambda new_wallpaper_path: exit(),
    'Linux': lambda new_wallpaper_path: os.system(f'gsettings set org.gnome.desktop.background picture-uri file://{new_wallpaper_path}'),
    'Darwin': lambda new_wallpaper_path: os.system(f'osascript -e \'tell application "Finder" to set desktop picture to POSIX file"{new_wallpaper_path}"\'')
}

config_path = {
    'Linux': '~/.wallpaper_boi',
    'Darwin': '~/.wallpaper_boi'
}

# Load config from ~/.wallpaper_boi
if platform.system() not in config_path.keys():
    print(f'{platform.system()} is not currently supported')
    exit()

with open(os.path.expanduser(config_path[platform.system()]),'r') as config:
	configs = { line.split(':')[0]:line.split(':')[1] for line in config.read().split('\n') if ':' in line }

image_types = configs['supported_image_types'].split(',')
supported_sites =  configs['supported_image_domains'].split(',')
target_subreddit = configs['target_subreddit']
wallpaper_folder = os.path.expanduser(configs['wallpaper_folder'])


# Remove old images from wallpaper directory
for the_file in os.listdir(wallpaper_folder):
	file_path = os.path.join(wallpaper_folder, the_file)
	try:
		if os.path.isfile(file_path):
			os.unlink(file_path)
	except Exception as e:
		print(e)


# Load image urls from configured subreddit
ssl._create_default_https_context = ssl._create_unverified_context

image_regex = f'https://({"|".join(supported_sites)})(.*?)({"|".join(image_types)})'
reddit_url = f"http://www.reddit.com/r/{target_subreddit}/"
result = re.finditer(image_regex, str(urllib.request.urlopen(reddit_url).read()))

urls = [url.group(0) for url in result]
print(urls)
new_wallpaper_path = ""

# Try downloading the top rated links, save to configured folder
for URL in urls:
	try:
		with urllib.request.urlopen(URL) as url:
			random_name = "".join(np.random.choice(list(string.ascii_lowercase), 10))
			image_type = URL.split(".")[-1]
			new_wallpaper_path = f'{wallpaper_folder}/{random_name}.{image_type}'
			with open(new_wallpaper_path, 'wb') as f:
				f.write(url.read())
		print(f'Attempting w/ {URL}')
		break
	except Exception as e:
		print(e)

# Set the wallpaper
set_wallpaper[platform.system()](new_wallpaper_path)
