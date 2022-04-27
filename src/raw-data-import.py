import requests

url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/'
r = requests.get(url, allow_redirects=True)

download_location ='../data/raw'

wget.download(url, download_location)
