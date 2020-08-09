# Instagram Time ID converter

import datetime


def get_location() -> str:
	return input(
		'Enter the URL of the location (for example: https://www.instagram.com/explore/locations/95099702/mgm-grand-las-vegas/)')


def get_date() -> str:
	return input('Enter the date in this form: 1999/7/27... (leave no zeros in front of single digit months/days)')


def date_str_2_dateobj(date: str) -> datetime.datetime:
	d_list = date.split("/")
	return datetime.datetime(int(d_list[0]), int(d_list[1]), int(d_list[2]), 23, 59, 59)


def date_2_unix(date_obj: datetime.date) -> int:
	unixdate = date_obj - datetime.datetime(1970, 1, 1)
	mstime = int(unixdate.total_seconds() * 1000.0)
	insta_epoch = mstime - 1314220021300
	return insta_epoch


def binary_decimal_convert(bindec: tuple) -> int:
	#     print(bin(bindec[1]))
	if bindec[0]:
		return int(bin(bindec[1])[2:])
	else:
		return int(bindec[1], 2)


def binary_lengthen(binary: int) -> int:
	zeroes = 41 - len(str(binary))
	six_fourbit = ('0' * zeroes) + str(binary) + ('0' * 23)
	return six_fourbit


def run(date):
	#     location_url = get_location()
	unix_time = date_2_unix(date_str_2_dateobj(date))
	newbin = binary_decimal_convert((True, unix_time))
	longbin = binary_lengthen(newbin)
	final_num = binary_decimal_convert((False, longbin))
	return str(final_num)
