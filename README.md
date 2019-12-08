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
  --logging, -log       logging activity
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
  --dontdelete, -dd     keep tmp files, to use with --readfile
  --stdout, -stdout     shows json or csv output in stdout
  --json, -json         Save data in json format
  --csv, -csv           Save data in CSV format
  --dorkfile DORKFILE, -df DORKFILE
                        file with expressions
  --readfile READFILE, -f READFILE
                        file to check. When something doesn'n work, check the
                        file
  --hour, -u            Requests results from past hour
  --day, -d             Requests results from past day
  --week, -w            Requests results from past week
  --month, -m           Requests results from past month
  --year, -y            Requests results from past year

group:
  --initialDate INITIALDATE, -id INITIALDATE
                        Initial date - format YYYY-MM-DD
  --finalDate FINALDATE, -fd FINALDATE
                        Final date - format YYYY-MM-DD

never mind the bollocks, if you don't like this, forget this.
comments>/dev/null
```

You can use quotes to use complex sentences with google operators, ie:
``` "pass|contraseña|contrasena|username|apikey|token|config|connection|id_rsa|hash+filetype:txt+inurl:(sitio1|sitio2)" ```
and silent the script output redirecting to /dev/null ... if you use json or csv plus stdout, you can use kapow
 

## To Do
[CSE: list](https://developers.google.com/custom-search/v1/cse/list)

[Request Format](https://support.google.com/gsa/answer/6329265#4134d4ec-c7f1-4eff-ae65-b171e689ca5a)

[Google Advanced Search](https://www.google.com/advanced_search)

[XML API reference appendices](https://developers.google.com/custom-search/docs/xml_results_appendices#countryCollections)
## License

pa ti