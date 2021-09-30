#!/usr/bin/python2 -tt

import csv
import re
import json
from sys import argv


def getDirect(line):
	cols = ['dir_link', 'dir_link/_text', 'dir_link/_title', 'credit_link_1', 'credit_link_1/_text', 'credit_link_1/_title', 'credit_value_2',
			'credit_value_3', 'credit_link_2', 'credit_link_2/_text', 'credit_link_3', 'credit_link_3/_text','credit_link_3/_title',
 			'credit_value_4', 'credit_link_4', 'credit_link_4/_text', 'credit_link_4/_title', 'genre_content', 'genre_links',
 			'genre_links/_text', 'genre_links/_title']
	director = []
	actors = []
	genres = []
	for i in range(len(cols)):
		col = cols[i]
		if col not in line:
			continue
		if not line[col]:
			continue
		line[col] = line[col].strip()
		if line[col].startswith('http:'):
			continue
		if line[col].startswith('With') or line[col].startswith(','):
			break
		if line[col].startswith('Dir'):
			match = re.match(r'^Dir:\s*(.*)\s+With:.*', line[col])
			if match:
				director = match.group(1).strip().split(';')
				break
			else:
				continue
		director = line[col].strip().split(';')
		break
	director = map(str.lower, director)
	for i in range(i + 1, len(cols)):
		col = cols[i]
		if col not in line:
			continue
		if not line[col]:
			continue
		line[col] = line[col].strip()
		if line[col].find('|') > -1:
			break
		if line[col].find(r'/genre/') > -1:
			if actors:
				actors.pop()
			i -= 1
			break
		if line[col].startswith('http:'):
			continue
		if line[col].startswith('With:'):
			continue
		if line[col].startswith(','):
			continue
		if line[col]:
			if line[col].find(';') > -1:
				for actor in line[col].split(';'):
					if actor.lower() not in director:
						actors.append(actor.strip())
			else:
				actors.append(line[col].lower())
	actors = map(str.lower, actors)
	if line[cols[i]]:
		genres = [val.strip().lower() for val in line[cols[i]].split('|') if val and not val.startswith('http:') and val.find('/') == -1]
	for direct in director[:]:
		if direct.isdigit():
			director.remove(direct)
		if direct.find(':') > -1:
			director.remove(direct)
	for actor in actors[:]:
		if actor.isdigit():
			actors.remove(actor)
		if actor.find(':') > -1:
			actors.remove(actor)
	return director, actors, genres


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
	prev = dict()
	for line in reader:
		if prev == line:
			continue
		else:
			prev = line
		temp = dict()
		link = line['image_link']
		if not link:
			continue
		temp['id'] = re.match(r'http://www\.imdb\.com/title/(\w+)', link).group(1).strip()
		temp['movie'] = line['title_link/_text'].strip().lower()
		if not temp['movie']:
			continue
		if 'value_number' in line:
			if line['value_number'] != '':
				temp['ratings'] = line['value_number']
			else:
				continue
		elif 'value' in line:
			if line['value'] != '':
				temp['ratings'] = line['value']
			else:
				continue
		else:
			continue
		if not line['yeartype_number'].strip():
			continue
		year = line['yeartype_number'].strip().strip('(').strip(')')
		if not year.isdigit():
			continue
		temp['year'] = int(year)
		temp['directors'], temp['actors'], temp['genres'] = getDirect(line)
		if not temp['directors']:
			continue
		if not temp['genres']:
			continue
		if not temp['actors']:
			continue
		if temp['ratings'] == '-':
			temp['ratings'] = -1
		elif len(temp['ratings']) > 4:
			continue
		else:
			temp['ratings'] = float(temp['ratings'])
		l = temp['actors'][:]
		l.extend(temp['genres'])
		l.extend(temp['directors'])
		if temp['movie'] in l:
			continue
		output.append(temp)
	return output


def main():
	output = []
	for arg in argv[1:]:
		temp = process(arg)
		output.extend(temp)
	# display(output)
	json.dump(output, open('hollydataset.json', 'wb'))


if __name__ == '__main__':
	main()