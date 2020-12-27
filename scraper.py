import argparse
import codecs
import json
import logging
import sys
from pathlib import Path

import backoff
import requests
from tqdm import tqdm

import dateToId


BASE_URL = "https://www.instagram.com/explore/locations/{location_id}/?__a=1&max_id={max_id}"
MAX_TRIES = 11


@backoff.on_exception(wait_gen=backoff.fibo, max_tries=MAX_TRIES,
                      exception=(requests.exceptions.HTTPError, requests.exceptions.ConnectionError))
def pull_json(location_name, end_cursor):
	URL = BASE_URL.format(location_id=METRO[location_name], max_id=end_cursor)
	logging.debug(URL)
	r = requests.get(url=URL, headers = {'User-agent': 'your bot 0.1'})
	if r.status_code == 200:
		data = r.json()['graphql']['location']['edge_location_to_media']
		return data
	else:
		raise requests.exceptions.HTTPError


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
	logging.debug(f"end_cursor: {end_cursor}")

	pbar = tqdm(unit='post')
	while end_cursor and end_cursor > maxid2:
		data = pull_json(location, end_cursor)
		if data:
			filename = f"{PATH}/{location}_{date1.replace('/', '-')}_{date2.replace('/', '-')}"
			save_jsonl(data['edges'], filename + '.jsonl')
			end_cursor = data['page_info']['end_cursor']
			open(f"{filename}_CURSOR.txt", "w").write(str(end_cursor))
			pbar.update(len(data['edges']))
		else:
			logging.warning(f"No data found at end_cursor: {end_cursor}")
	else:
		pbar.close()


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("--dir", nargs=1, default=['./data'])
	parser.add_argument("--max", nargs=1, required=True)
	parser.add_argument("--min", nargs=1, required=True)
	parser.add_argument("--location", nargs=1, required=True)
	parser.add_argument('--restore-cursor', action='store_true', default=False)
	parser.add_argument('--log-level', type=int, default=20)

	args = parser.parse_args()
	global METRO
	global PATH
	global log
	PATH = args.dir[0]
	METRO = json.load(open("./metros.json", 'r'))
	logging.basicConfig(level=args.log_level)
	log = logging.getLogger(__name__)

	assert args.location[0] in METRO, 'Location not available in metros.json'

	if args.restore_cursor:
		logging.warning(f"--max {args.max[0]} will be ignored. Scraping as far back as {args.min[0]}")
		filename = f"{PATH}/{args.location[0]}_{args.max[0].replace('/', '-')}_{args.min[0].replace('/', '-')}"
		maxid1 = open(f"{filename}_CURSOR.txt", "r").read()
	else:
		maxid1 = None
		logging.info(f"Scraping between dates {args.min[0]} and {args.max[0]}")

	logging.info(f"PATH: {PATH}")
	scrape(args.max[0], args.min[0], args.location[0], maxid1)


def test():
	global METRO
	global PATH
	global log
	PATH = "./data"
	METRO = json.load(open("./metros.json", 'r'))
	logging.basicConfig(level=10)
	log = logging.getLogger(__name__)
	scrape("2020/07/16", "2020/07/15", "Memphis")


if __name__ == "__main__":
	main()
# 
