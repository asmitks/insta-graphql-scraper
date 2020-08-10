Instagram Graphql Scraper
=================
[![PyPI](https://img.shields.io/pypi/v/instagram-scraper.svg)](https://pypi.python.org/pypi/instagram-scraper)

instagram-graphql-scraper is a command-line application written in Python that scrapes posts and complete metadata(caption, image-link, description, time-stamp, location), from instagram's explore location page. The novelty lies in the option to provide min and max date, hence giving an option to scrape old posts as well.

Installation
-------
To install insta-graphql--scraper:
```bash
$ pip install insta-graphql-scraper

```
To update insta-graphql-scraper:
```bash
$ pip install insta-graphql-scraper --upgrade
```

## Usage

```bash
$ scrape [-h] [--dir DIR] --max MAX_DATE --min MIN_DATE --location LOCATION
                  [--restore-cursor] [--log-level LOG_LEVEL]
```

### Example
 1. Standard: `python scraper.py --max "2020/07/15" --min "2020/06/15" --location "New-York-City"`
 2. Custom directory: `python scraper.py --dir "./data" --max "2020/07/15" --min "2020/06/15" --location "New-York-City
 " --restore-cursor`
 3. Log debug messages: `python scraper.py --max "2020/07/15" --min "2020/06/15" --location "New-York-City" -- log-level
  10`
 4. Restore from last saved post: `python scraper.py --max "2020/07/15" --min "2020/06/15" --location "New-York-City" --restore-cursor`
