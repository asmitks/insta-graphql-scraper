## Usage

```
python scraper.py [-h] [--dir DIR] --max MAX_DATE --min MIN_DATE --location LOCATION
                  [--restore-cursor] [--log-level LOG_LEVEL]
```

### Example
 1. Standard: `python scraper.py --max "2020/07/15" --min "2020/06/15" --location "New-York-City"`
 2. Custom directory: `python scraper.py --dir "./data" --max "2020/07/15" --min "2020/06/15" --location "New-York-City
 " --restore-cursor`
 3. Log debug messages: `python scraper.py --max "2020/07/15" --min "2020/06/15" --location "New-York-City" -- log-level
  10`
 4. Restore from last saved post: `python scraper.py --max "2020/07/15" --min "2020/06/15" --location "New-York-City" --restore-cursor`
