import argparse
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import time

zaycev_net_find = "http://zaycev.net/search.html?query_search="
zaycev_net = "http://zaycev.net"

def get_track_list_from_file(filename):
	track_file = open(filename, 'r')
	track_list = [];
	for temp_string in track_file:
		temp_string = temp_string.replace('-', '')
		i = temp_string.find('.')
		if i != -1:
			temp_string = temp_string[i + 1:]
			temp_string = temp_string.strip()
			temp_string = ' '.join(temp_string.split())
			track_list.append(temp_string)
		else:
			print("Parsing file error - can't find . in track name")
			return

	return track_list


def create_url(track):
	url = zaycev_net_find
	temp_list = track.split()
	for temp_string in temp_list:
		url = url + '+' + urllib.parse.quote(temp_string.encode('utf-8'))
	return url


def get_mp3_link_from_page(url):
	response = urllib.request.urlopen(url)
	soup = BeautifulSoup(response)
	mp3_links = soup.find_all('a', {"class": "audiotrack-button__label track-geo__button track-geo__link"})
	if (len(mp3_links) > 0):
		return mp3_links[0]["href"]

	return


def download_track_list(track_list):
	out_file = open("not_found.txt", 'w')
	mp3_file = open("found.txt", 'w')
	for track in track_list:
		find_url = create_url(track)
		response = urllib.request.urlopen(find_url)
		soup = BeautifulSoup(response)
		track_links = soup.findAll('a', {"class": "musicset-track__download-link track-geo__control"})

		if (len(track_links) > 0):
			mp3_link = get_mp3_link_from_page(zaycev_net + track_links[0]["href"])
			if (mp3_link == None):
				out_file.write(track + '\n')
			else:
				mp3_file.write(mp3_link + '\n')
				time.sleep(5)
				try:
					urllib.request.urlretrieve(mp3_link, track + '.mp3')
				except:
					out_file.write(track + '\n')
				time.sleep(1)
		else:
			out_file.write(track + '\n')

	out_file.close()
	mp3_file.close()

def download_from_file(filename):
	list = get_track_list_from_file(filename)
	if (list == None):
		return
	download_track_list(list)


if __name__ == '__main__':
	print("Starting...")
	parser = argparse.ArgumentParser()
	parser.add_argument("--file", help="path to file with tracks")
	args = parser.parse_args()
	if args.file:
		print("Downloading tracks from file " + args.file)

	download_from_file(args.file)