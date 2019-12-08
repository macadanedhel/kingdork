# Kindork

Una versión rapidita para hacer búsquedas en google para la prueba de concepto

## Installation

Pues te lo bajas y lo normal. Fichero de requirements.txt y tan felices

```bash
pip install -r requirements.txt
```

## Usage

```python
usage: python kingdork [options]

Another dorking tool. This is only a proof of concept to develop an a right
tool. Just a hobby

optional arguments:
  -h, --help            show this help message and exit
  --verbose, -v         Verbose
  --config CONFIG, -c CONFIG
                        Config file
  --numpages NUMPAGES, -n NUMPAGES
                        number of pages to manage
  --language LANGUAGE, -l LANGUAGE
                        file with expressions
  --location LOCATION, -o LOCATION
                        location, narrow to a country
  --query QUERY, -q QUERY
                        words to search, with quotes ie: "atletico de madrid"
  --filter, -r          Include omitted results
  --site SITE, -s SITE  Site
  --socialmedia SOCIALMEDIA, -sm SOCIALMEDIA
                        search in social media ie: twitter
  --hashtag HASHTAG, -t HASHTAG
                        search hashtags
  --json, -json         Save data in json format
  --csv, -csv           Save data in CSV format
  --dorkfile DORKFILE, -df DORKFILE
                        file with expressions
  --readfile READFILE, -f READFILE
                        file to check. When something doesn'n work, check the
                        file
  --hour HOUR, -u HOUR  Requests results from past hour
  --day DAY, -d DAY     Requests results from past day
  --week WEEK, -w WEEK  Requests results from past week
  --month MONTH, -m MONTH
                        Requests results from month
  --year YEAR, -y YEAR  Requests results from years

group:
  --initialDate INITIALDATE, -id INITIALDATE
                        Initial date - format YYYY-MM-DD
  --finalDate FINALDATE, -fd FINALDATE
                        Final date - format YYYY-MM-DD

never mind the bollocks, if you don't like this, forget this.
comments>/dev/null

```

## To Do
[CSE: list](https://developers.google.com/custom-search/v1/cse/list)

[Request Format](https://support.google.com/gsa/answer/6329265#4134d4ec-c7f1-4eff-ae65-b171e689ca5a)

[Google Advanced Search](https://www.google.com/advanced_search)

[XML API reference appendices](https://developers.google.com/custom-search/docs/xml_results_appendices#countryCollections)
## License

pa ti