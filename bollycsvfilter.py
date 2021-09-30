#!/usr/bin/python2 -tt

import csv
import json
import sys
from sys import argv
from imdbpie import Imdb


def display(inp):
	for line in inp:
		text = ""
		for key in line:
			text += "{0:<}:{1:<},   ".format(key, str(line[key]))
		print text


def process(fileName):
	output = []
	f = open(fileName, 'rb')
	reader = csv.DictReader(f)
	imdb = Imdb()
	count = 1
	for line in reader:
		temp = dict()
		temp['movie'] = line['Title'].strip().lower()[1:-1]
		sys.stdout.write('Processing %s  (Count=%d)  -----------------------------------\r' % (temp['movie'], count))
		count += 1
		if not temp['movie']:
			continue
		try:
			m_id = imdb.search_for_title(temp['movie'])
			m_id = m_id[0]['imdb_id']
			title = imdb.get_title_by_id(m_id)
			sys.stdout.flush()
		except:
			print 'Skipping %s' % temp['movie']
			continue
		if not m_id:
			continue
		temp['id'] = m_id
		temp['ratings'] = title.rating
		temp['year'] = title.year
		if line['Director']:
			temp['directors'] = map(str.strip, map(str.lower, line['Director'].split(',')))
		else:
			continue
		if line['Genre']:
			temp['genres'] = map(str.strip, map(str.lower, line['Genre'].split(',')))
		else:
			continue
		if line['Cast']:
			temp['actors'] = map(str.strip, map(str.lower, line['Cast'].split(',')))
		else:
			continue
		output.append(temp)
	return output


def main():
	output = []
	for arg in argv[1:]:
		temp = process(arg)
		output.extend(temp)
	# display(output)
	# print json.dumps(output)
	json.dump(output, open('data/bollydataset.json', 'wb'))
	# gen_output = set()
	# for movie in output:
	# 	gen_output.update(movie['genres'])
	# print gen_output


if __name__ == '__main__':
	main()
