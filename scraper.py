import argparse
import codecs
import json
import logging
import sys
from pathlib import Path

import backoff
import requests

import dateToId

logging.basicConfig(level=logging.DEBUG)
METRO = json.load(open("./metros.json"))
PATH = './data/'
BASE_URL = "https://www.instagram.com/explore/locations/{location_id}/{location_name}/?__a=1&max_id={max_id}"
MAX_TRIES = 11


@backoff.on_exception(wait_gen=backoff.fibo, max_tries=MAX_TRIES,
                      exception=(requests.exceptions.HTTPError, requests.exceptions.ConnectionError))
def pull_json(location_name, end_cursor):
	try:
		URL = BASE_URL.format(location_name=location_name, location_id=METRO[location_name],
		                      max_id=end_cursor)
		r = requests.get(url=URL)
		if r.status_code == 200:
			data = r.json()['graphql']['location']['edge_location_to_media']
			return data
		else:
			return None
	except:
		return None


def save_jsonl(data, dst='./'):
	"""Saves the data to a jsonl file."""
	path = Path(dst)
	assert isinstance(data, list)
	if path.exists():
		f = codecs.open(dst, "ab", 'utf-32')
	else:
		path.parent.mkdir(parents=True, exist_ok=True)
		f = codecs.open(dst, 'wb', 'utf-32')
	f.writelines("%s\n" % json.dumps(s) for s in data)


def scrape(date1, date2, location, restore_cursor=None):
	try:
		maxid1 = dateToId.run(date1)
		maxid2 = dateToId.run(date2)
	except:
		logging.error("error in date format, make sure no following zeroes example: 2020/7/15")
		sys.exit(1)

	end_cursor = maxid1 if restore_cursor is None else restore_cursor
	logging.debug("end_cursor: ", end_cursor)

	while end_cursor and end_cursor > maxid2:
		data = pull_json(location, end_cursor)
		filename = f"{PATH}/{location}_{date1.replace('/', '-')}_{date2.replace('/', '-')}.jsonl"
		save_jsonl(data['edges'], filename)
		end_cursor = data['page_info']['end_cursor']
		open(PATH + 'cursor.txt', "w").write(str(end_cursor))


def main_old(argv):
	assert len(argv) == 3, 'USAGE: python3 scraper.py <max_date> <min_date> <location>'
	date1 = argv[0]
	date2 = argv[1]
	location = argv[2]

	try:
		maxid1 = dateToId.run(date1)
		maxid2 = dateToId.run(date2)
	except:
		logging.error("error in date format, make sure no following zeroes example: 2020/7/15")
		return

	assert location in METRO, 'Location not available in metros.json'
	scrape(maxid1, maxid2, location)


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("--max", nargs=1, required=True)
	parser.add_argument("--min", nargs=1, required=True)
	parser.add_argument("--location", nargs=1, required=True)
	parser.add_argument('--restore-cursor', action='store_true', default=False)

	args = parser.parse_args()
	print(args)

	assert args.location[0] in METRO, 'Location not available in metros.json'

	if args.restore_cursor:
		logging.warning(f"--max {args.max} will be ignored. Scraping as far back as {args.min}")
		maxid1 = open(PATH + 'cursor.txt', "r").read()
	else:
		logging.info(f"Scraping between dates {args.min[0]} and {args.max[0]}")

	scrape(args.max[0], args.min[0], args.location[0])


def test():
	scrape("2020/07/16", "2020/07/15", "New-York-City")


if __name__ == "__main__":
	main()
# test()
