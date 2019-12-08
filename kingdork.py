import os, re
import logging
import argparse
import datetime
import configparser
import requests
import urllib
import random
import string
import json
import csv
import pprint

from bs4 import BeautifulSoup

__author__ = 'mac'
__version__ = '1.0.0'
NAME = 'kingdork'
_GLOBAL_NAME = 'google_search'
_DATETIME = datetime.datetime.now().strftime("%Y%m%d")
configfile = 'conf/config.ini'
_JSON='json'
_CSV='csv'
_SCREEN = 'screen'
google_base = 'https://www.google.com'
google_search = '/search?q='

logger = logging.getLogger(NAME)
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s')

ch.setFormatter(formatter)

logger.addHandler(ch)


# -----------------------------------------------------------------------------------------------------------------------
class data_found:
    def __init__(self, name=None):
        if not name is None:
            self.NAME = name
        else:
            self.NAME = _GLOBAL_NAME
        self.current = 0
        self.data = {
            'number': 0,
            0: {
                'link': '',
                'title': '',
                'description': '',
                'date': ''
            }
        }
        self.next_page = None

    def _plus(self):
        self.current += 1

    def add_data(self, _link=None, _title=None, _description=None, _date=None):
        self.data[self.current] = {
            'link': _link,
            'title': _title,
            'description': _description,
            'date': _date
        }
        self._plus()

    def show(self, number=False):
        if number is False:
            number = self.last()
        if not number is False:
            return self.data[number]
        else:
            return None

    def last(self):
        if self.current == 0:
            return False
        else:
            return self.current - 1

    def items_found (self, _div):
        res =  _div.find('div', attrs={'class': 'appbar'}).text
        if len(res)<=0:
            res = None
        return res

    def print(self):
        for i in range(0, self.current):
            aux = self.show(i)
            print("Data [{0}]\n\tTitle: {1}\n\tlink: {2}\n\tdescription: {3}\n\tdate: {4}".format(
                i, aux['title'], aux['link'], aux['description'], aux['date']
            ))
        #print("Next page: {0}".format(self.next_page))

    def div_DATA_V1 (self, _content):
        link = ''
        title = ''
        description = ''
        date = ''
        try:
            # ---- Parte superior
            link = re.sub('^/url\?q=', '', _content[0].find('a', href=True)['href']).split('&')[0]
            title = _content[0].find('div', attrs={'class': 'BNeawe'}).get_text()
            # ---- Parte inferior
            description = _content[1].find('div', attrs={'class': 'BNeawe'}).get_text()
            if _content[1].find('span', 'r0bn4c rQMQod'):
                res2 = _content[1].find_all('span', 'r0bn4c rQMQod')
                date = res2[0].text
        except:
            pass
        return link, title, description, date

    def div_DATA_V2(self, _content):
        link = ''
        title = ''
        description = ''
        date = ''
        try:
            # ---- Parte superior
            link =  _content.find('div',{'class','r'}).find_all('a')[2]['href']
            title =  _content.find('div',{'class','r'}).h3.text
            # ---- Parte inferior
            description = _content.find('div', {'class', 's'}).text
            date = (_content.find('div',{'class','s'}).find('span','f').text).split(' - ')[0]
        except:
            pass
        return link, title, description, date

    def div_DATA(self, _div):
        link = ''
        title = ''
        description = ''
        date = ''
        content = _div.find_all('div', attrs={'class': 'kCrYT'})
        if len(content) == 2:
            link, title, description, date = self.div_DATA_V1(content)
        else :
            link, title, description, date = self.div_DATA_V2(_div)
        if link != '' or title != '' or description != '':
            self.add_data(link, title, description, date)

    def div_SECTION (self, result):
        resultado = result.find_all('div', attrs={'class': 'ZINbbc'})
        if len(resultado)==0:
            resultado = result.find_all('div', attrs={'class': 'g'})
        return resultado

    def select_next_page(self, result):
        try :
            self.next_page = result.find('div', attrs={'class': 'ZINbbc xpd O9g5cc uUPGi BmP5tf'}).a['href']
        except:
            try:
                self.next_page = result.find('a', attrs={'class': 'pn'})['href']
            except:
                self.next_page = None

    def keys (self):
        return ['link','title', 'description','date']

    def data_found (self):
        _data= []
        for i in range(0, self.current):
            _data.append(self.show(i))
        return _data
# -----------------------------------------------------------------------------------------------------------------------
def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.sample(letters, stringLength))

def string2search(words):
    query = urllib.parse.quote_plus(words)

def config(file=None):
    _configdata = {}
    if file is None:
        file = configfile
    if os.path.exists(file):
        Config = configparser.ConfigParser()
        Config.read(file)
        for i in Config.sections():
            _configdata[i] = dict(Config.items(i))
    else:
        logger.error('File {0} not found'.format(file))
    return _configdata

def options():
    _config = config()
    parser = argparse.ArgumentParser(
        prog=NAME,
        usage="python %(prog)s [options]",
        description='Another dorking tool. This is only a proof of concept to develop an a right tool. Just a hobby',
        epilog='never mind the bollocks, if you don\'t like this, forget this. comments>/dev/null'
    )


    parser.add_argument('--verbose', "-v", action='store_true', help='Verbose')
    parser.add_argument('--logging', '-log', action='store_true', help='logging activity')
    parser.add_argument('--config', "-c", type=str, help='Config file')
    parser.add_argument('--numpages', "-n", type=int, help='number of pages to manage', default=1)
    parser.add_argument('--language', "-l", type=str, help='file with expressions')
    parser.add_argument('--location', "-o", type=str, help='location, narrow to a country')
    parser.add_argument('--query', "-q", type=str, help='words to search, with quotes ie: "atletico de madrid"')
    parser.add_argument('--filter', "-r", action='store_true', help='Include omitted results')
    parser.add_argument('--site', "-s", type=str, help='Site')
    parser.add_argument('--socialmedia', "-sm", type=str, help='search in social media ie: twitter')
    parser.add_argument('--hashtag', "-t", type=str, help='search hashtags')
    parser.add_argument('--dontdelete', "-dd", action='store_true', help='keep tmp files, to use with --readfile')
    parser.add_argument('--stdout', "-stdout", action='store_true', help='shows json or csv output in stdout')


    group1 = parser.add_mutually_exclusive_group()
    group1.add_argument('--json', '-json', action='store_true', help='Save data in json format')
    group1.add_argument('--csv', '-csv', action='store_true', help='Save data in CSV format')

    group2 = parser.add_mutually_exclusive_group()
    group2.add_argument('--dorkfile', "-df", type=str, help='file with expressions')
    group2.add_argument('--readfile', "-f", type=str, help='file to check. When something doesn\'n work, check the file')

    group3 = parser.add_argument_group('group')
    group3.add_argument('--initialDate', "-id", type=datetime.date.fromisoformat,
                        help='Initial date  - format YYYY-MM-DD')
    group3.add_argument('--finalDate', "-fd", type=datetime.date.fromisoformat,
                        help='Final date  - format YYYY-MM-DD')

    group4 = parser.add_mutually_exclusive_group()
    group4.add_argument('--hour', "-u", action='store_true', help='Requests results from past hour')
    group4.add_argument('--day', "-d", action='store_true', help='Requests results from past day')
    group4.add_argument('--week', "-w", action='store_true', help='Requests results from past week')
    group4.add_argument('--month', "-m", action='store_true', help='Requests results from past month')
    group4.add_argument('--year', "-y", action='store_true', help='Requests results from past year')

    args = parser.parse_args()
    if args.logging:
        if not os.path.exists(_config['path']['log']):
            os.mkdir(_config['path']['log'])
        name= _config['path']['log'] +"/{0}_{1}.log".format(_DATETIME, NAME)
        logging.basicConfig(filename=name, filemode='a', format='%(name)s - %(levelname)s - %(message)s')

    if args.config:
        logger.info("Getting data from configuration file {0}".format(args.config))
        _config = config(args.config)
    if args.numpages :
        _config['numpages'] = args.numpages
    else:
        _config['numpages'] = 1
    if args.verbose:
        _config['VERBOSE'] = args.verbose
        logger.setLevel(logging.DEBUG)
        ch.setLevel(logging.DEBUG)
    else:
        _config['VERBOSE'] = False
    if args.query:
        _config['search_string'] = args.query
    else:
        _config['search_string'] = 'test'

    if args.readfile and not os.path.exists(args.readfile):
        logger.error('File {0} not found'.format(args.readfile))
    elif args.readfile:
        _config['FILE'] = args.readfile

    if args.json :
        _config['OUTPUT'] = _JSON
    elif args.csv :
        _config['OUTPUT'] = _CSV
    else:
        _config['OUTPUT'] = _SCREEN

    if args.stdout :
        _config['OUTPUT_AUX'] = _SCREEN


    if args.language :
        if args.language in _config['google-lang']:
            _config['search_string']+="&lr="+_config['google-lang'][args.language]
        else :
            logger.error('Language {0} not found'.format(args.language))

    if args.location :
        if args.location in _config['google-location']:
            _config['search_string']+="&cr="+_config['google-location'][args.location]
        else :
            logger.error('Location {0} not found'.format(args.location))
    if args.filter:
        _config['search_string'] += "&filter=0"
    if args.initialDate:
        id=str(args.initialDate).split("-")
        fd=str(args.finalDate).split("-")
        _config['search_string'] += "&tbs=cdr:1,cd_min:" + id[1] + "/" + id[2] + "/" + id[0] + ",cd_max:" + fd[1] + "/" + fd[2] + "/" + fd[0]

    if args.hour:
        _config['search_string'] += "&tbs=qdr:h"
    if args.day:
        _config['search_string'] += "&tbs=qdr:d"
    if args.week:
        _config['search_string'] += "&tbs=qdr:w"
    if args.month:
        _config['search_string'] += "&tbs=qdr:m"
    if args.year:
        _config['search_string'] += "&tbs=qdr:y"
    if args.socialmedia:
        _config['search_string'] += " @" + args.socialmedia
    if args.hashtag:
        _config['search_string'] += " #" + args.socialmedia

    if args.site and args.query:
        _config['search_string'] += " site:"+args.site

    if 'key' in _config['identity'] and _config['identity']['key'] != 'empty':
        _config['search_string'] += "&key=" + _config['identity']['key']
    _url = google_base + google_search + _config['search_string']


    if args.dorkfile and os.path.exists(args.dorkfile):
        _config['dorkfile'] = args.dorkfile
        _url = google_base + google_search
    elif args.dorkfile:
        logger.error('File {0} not found'.format(args.dorkfile))
        exit (0)

    if args.dontdelete :
        _config['DONTDELETE'] = True
    else:
        _config['DONTDELETE'] = False


    return _config, _url

def dork(_config, _url):

    logger.info('Getting data from URL: {0}'.format(_url))

    ua = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'}
    response = requests.get(_url, headers=ua)
    # if _config['VERBOSE']:
    #     logger.debug("Status code: {0} encoding: {1}".format(response['status_code'],response['encoding']))
    aux = "/{0}_{1}_{2}.html".format(_DATETIME, _config['search_string'], randomString())
    try :
        aux = re.sub('/','',aux)
    except:
        pass
    name = _config['path']['tmp'] + "/"+ aux
    logger.info('Writting data in: {0}'.format(name))
    open(name, 'wb').write(response.content)
    html = BeautifulSoup(response.content, "html.parser")
    cd = data_found()
    cd.select_next_page(html)
    _url = cd.next_page
    if _config['VERBOSE']:
        logger.debug('obtained URL: {0}'.format(_url))
        logger.debug('data saved in file: {0}'.format(name))
    return _url, name

def files2open(filename, _encoding='ISO-8859-1'):
    logger.info('Openning file  {0}'.format(filename))
    f = open(filename, 'r', encoding=_encoding)
    doc = f.read()
    f.close()
    return doc

def showfiles(files):
    cd = data_found()
    for i in files:
        doc =  files2open(i)
        html = BeautifulSoup(doc, "html.parser")
        found = cd.items_found(html)
        if found:
            logger.info(found)
        resultado = cd.div_SECTION(html)
        for i in resultado:
            cd.div_DATA(i)
    manageoutput(_config, cd)

def loop(_config, _url, loop=1):
    cont = 0
    files = []
    if not os.path.exists(_config['path']['tmp']):
        os.mkdir(_config['path']['tmp'])
    while cont < loop:
        logger.info('count : {0}'.format(cont))
        cont += 1
        _aux, _file = dork(_config, _url)
        if _aux is None:
            logger.info('Next page not found.')
        else:
            _url = google_base + _aux
            if _config['VERBOSE']:
                logger.debug('URL returned: {0}'.format(_url))
                logger.debug('filename returned: {0}'.format(_file))
        files.append(_file)
    return files

def deletefiles (files):
    for i in files:
        os.remove(i)
        logger.info('{0} deleted !!!'.format(i))

def manageoutput (_config, _data):
    def filename (_config) :
        _TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        return _TIMESTAMP+"_"+_GLOBAL_NAME
    if _config['OUTPUT'] == _SCREEN:
        if _config['VERBOSE']:
            logger.debug('screen output')
        _data.print()
    else:
        if not os.path.exists(_config['path']['data']):
            os.mkdir(_config['path']['data'])
            logger.info('Outout directory created :{0}'.format(config['path']['data']))
        name = _config['path']['data']+"/"+filename(_config)
        if _config['OUTPUT'] == _JSON:
            name+=".json"
            if _config['VERBOSE']:
                logger.debug('screen output')
            logger.info('Writing data in {0}'.format(name))
            with open(name, 'w', encoding='utf8') as json_file:
                json.dump(_data.data, json_file, ensure_ascii=False)
            if _config['OUTPUT_AUX']:
                pprint.pprint(_data.data)
        elif _config['OUTPUT'] == _CSV:
            name+=".csv"
            logger.info('Writing data in {0}'.format(name))
            if _config['VERBOSE']:
                logger.debug('Keys found:{0}'.format(_data.keys()))
            csv_file = csv.writer(open(name, 'w'))
            csv_file.writerow(_data.keys())
            if _config['OUTPUT_AUX']:
                print (_data.keys())
            for row in _data.data_found():
                _csv_data = []
                for key in _data.keys():
                    _csv_data.append(row[key])
                csv_file.writerow(_csv_data)
                if _config['OUTPUT_AUX']:
                    print(_csv_data)

if __name__ == "__main__":
    dt = datetime.datetime.now()
    _config, _url = options()
    logger.info('Starting {0} at {1}...'.format(NAME, dt))
    if _config['VERBOSE']:
        logger.debug('config: {0}'.format(_config))
    if 'FILE' in _config:
        showfiles([_config['FILE']])
    elif 'dorkfile' in  _config:
        doc = files2open (_config['dorkfile'],'utf-8')
        linecount=0
        name=_config['dorkfile'].split("/")[len(_config['dorkfile'].split("/"))-1]
        for i in doc.split('\n'):
            str = i
            _aux = _url + i
            logger.info('URL to check: {0}'.format(_aux))
            _config['search_string']="{0}_line_{1}".format( name,linecount)
            linecount+=1
            files = loop(_config, _aux, _config['numpages'])
        showfiles(files)
        if not _config['DONTDELETE']:
            deletefiles(files)
    else:
        files = loop(_config, _url, _config['numpages'])
        showfiles(files)
        if not _config['DONTDELETE']:
            deletefiles(files)
    dt = datetime.datetime.now() - dt
    logger.info('Finished. Elapsed time {0}'.format(dt))

