import os, re
import logging
import argparse
import datetime
import configparser
import requests
from requests.adapters import TimeoutSauce
import urllib
import random
import string
import json
import csv
import pprint
import base64
import copy

from bs4 import BeautifulSoup

__author__ = 'mac'
__version__ = '1.0.1'
NAME = 'kingdork'
_GLOBAL_NAME = 'google_search'
_DATETIME = datetime.datetime.now().strftime("%Y%m%d")
configfile = 'conf/config.ini'
_JSON='json'
_CSV='csv'
_SCREEN = 'screen'
_SEARCH_EXTENSION = '_search'
REQUESTS_TIMEOUT_SECONDS = float(4)


logger = logging.getLogger(NAME)
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s')

ch.setFormatter(formatter)

logger.addHandler(ch)


# -----------------------------------------------------------------------------------------------------------------------
class data_found:
    def __init__(self, name=None, _type = None):
        if not name is None:
            self.NAME = name
        else:
            self.NAME = _GLOBAL_NAME
        self.current = 0
        self._struct = None
        if  _type is None:
            self.CLASS = 'WEB'
            self._keys = ['link','title', 'description','date']
            self._struct = {
                'link': '',
                'title': '',
                'description': '',
                'date': '',
                'file': ''
            }
            self.data = {
                'number': 0,
                0: self._struct
            }

        else:
            self.CLASS = 'API'
            self.keytype = {
                'strings' : ['kind', 'title', 'htmlTitle', 'link', 'displayLink', 'snippet', 'htmlSnippet', 'cacheId', 'mime',
                      'formattedUrl', 'htmlFormattedUrl', 'fileFormat'],
                'objects' : ['labels', 'pagemap', 'labels', 'image']
            }

            self._keys = self.keytype['strings'] + self.keytype['objects']
            self._struct = {
                    'kind': '',
                    'title': '',
                    'htmlTitle': '',
                    'link': '',
                    'displayLink': '',
                    'snippet': '',
                    'htmlSnippet': '',
                    'cacheId': '',
                    'mime': '',
                    'formattedUrl': '',
                    'htmlFormattedUrl' : '',
                    'fileFormat' : '',
                    'labels': '',
                    'pagemap': '',
                    'image': ''
                }
            self.data = {
                'number': 0,
                0: self._struct
            }


        self.next_page = None

    def _plus(self):
        self.current += 1
        self.data['number']=self.current
        self.data[self.current] = copy.copy(self._struct)

    def _changeClass (self, type):
        self=self.__init__(self.NAME,type)

    def add_data(self, _link=None, _title=None, _description=None, _date=None, _file=None, _item=None):
        if _link is None and _title is None  and _description is None  and _date is None  and _file is None  and not _item is None:
            if self.CLASS == 'WEB':
                self.data[self.current]=_item
            else:
                for key in self.keys():
                    if key in self.keytype['strings']:
                        try:
                            self.data[self.current][key]=_item[key]
                        except:
                            pass
                    else:
                        try:
                            self.data[self.current][key] = str(_item[key])
                        except:
                            pass
        else:
            if self.CLASS == 'WEB':
                self.data[self.current] = {
                    'link': _link,
                    'title': _title,
                    'description': _description,
                    'date': _date,
                    'file': _file
                }
            else:
                print ("Not implemented yet O_o")
                print (_item)
                exit(0)
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
        try:
            res =  _div.find('div', attrs={'class': 'appbar'}).text
        except:
            res=""
        if len(res)<=0:
            res = None
        return res

    def print(self):
        for i in range(0, self.current):
            aux = self.show(i)
            for key in aux.keys():
                print ("\t[{0}]:{1}".format(key,aux[key]))
            print ("\n")
            #print("Data [{0}]\n\tTitle: {1}\n\tlink: {2}\n\tdescription: {3}\n\tdate: {4}\n\tfile: {5}".format(
            #    i, aux['title'], aux['link'], aux['description'], aux['date'], aux['file']
            #))
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
            # [2] webcache
            link =  _content.find('div',{'class','r'}).find_all('a')[0]['href']
            if link == '#' :
                link = _content.find('div', {'class', 'r'}).find_all('a')[3]['href']
            title =  _content.find('div',{'class','r'}).h3.text
            # ---- Parte inferior
            description = _content.find('div', {'class', 's'}).text
            date = (_content.find('div',{'class','s'}).find('span','f').text).split(' - ')[0]
        except:
            pass
        return link, title, description, date

    def div_DATA(self, _div, file = None):
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
            self.add_data(link, title, description, date, file)

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

    def keys (self, _type=None):
        if _type is None:
            return self._keys
        elif _type in ['objects','strings'] and self.CLASS == 'API':
            print (self.keytype[_type])
            return self.keytype[_type]
        else:
            return None

    def data_found (self):
        _data= []
        for i in range(0, self.current):
            _data.append(self.show(i))
        return _data
# -----------------------------------------------------------------------------------------------------------------------
def returnExpresion (_list)->str:
    return  "("+'|'.join(map(str,_list))+")"

def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.sample(letters, stringLength))

def string2search(words:str):
    query = urllib.parse.quote_plus(words)

def checkroute(route:str, create=False):
    if os.path.exists(route):
        return True
    elif create:
        os.mkdir(route)
        return True
    else:
        return False

# def connection (_conn, _url):
#     ua = {
#         'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'}
#     try:
#         res = _conn.get(_url, headers=ua)
#     except HTTPError as http_err:
#         print(f'HTTP error occurred: {http_err}')
#         exit(0)
#     except Exception as err:
#         print(f'Other error occurred: {err}')
#         exit(0)
#     except URLError as err:
#         print(f'URL Error: {err}')
#         exit(0)

def config(file=None):
    class CustomTimeout(TimeoutSauce):
        def __init__(self, *args, **kwargs):
            if kwargs["connect"] is None:
                kwargs["connect"] = REQUESTS_TIMEOUT_SECONDS
            if kwargs["read"] is None:
                kwargs["read"] = REQUESTS_TIMEOUT_SECONDS
            super().__init__(*args, **kwargs)

    _configdata = {}
    if file is None:
        file = configfile
    if checkroute(file, False):
        Config = configparser.ConfigParser()
        Config.read(file)
        for i in Config.sections():
            _configdata[i] = dict(Config.items(i))
    else:
        logger.error('File {0} not found'.format(file))
        exit(-1)
    for i in _configdata['extensions']:
        _configdata['extensions'][i]=_configdata['extensions'][i].split(',')
    for i in _configdata['data_downloaded']:
        if _configdata['data_downloaded'][i]=='False':
            _configdata['data_downloaded'][i]=False
        else:
            _configdata['data_downloaded'][i]=True

    for i in ['data','tmp', 'conf', 'log']:
        checkroute (_configdata['path'][i],True)

    _configdata['ENGINE'] = _configdata['search_engine']['google'] + _configdata['search_engine']['google_search']
    _configdata['CURRENT_ENGINES'] = _configdata['search_engine']['engines'].split(',')
    REQUESTS_TIMEOUT_SECONDS = float(_configdata['connection']['timeout'])
    requests.adapters.TimeoutSauce = CustomTimeout
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
    parser.add_argument('--engine', "-e", type=str, help='Engine to use')
    #parser.add_argument('--key', "-k", action='store_true', help='use the key')

    parser.add_argument('--document', "-doc", action='store_true', help='search documents')
    parser.add_argument('--markup', "-mkp", action='store_true', help='search markup language')
    parser.add_argument('--code', "-code", action='store_true', help='search code')
    parser.add_argument('--video', "-vdo", action='store_true', help='search video')
    parser.add_argument('--locationdata', "-loc", action='store_true', help='search location data')
    parser.add_argument('--picture', "-pic", action='store_true', help='search picture')

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

    if args.engine:
        if args.engine in _config['CURRENT_ENGINES']:
            aux = "" + args.engine + _SEARCH_EXTENSION
            _config['ENGINE'] = _config['search_engine'][args.engine] + _config['search_engine'][aux]
            if args.engine  == 'google_api':
                if 'key' in _config['identity'] and 'cx' in _config['identity']  :
                    _config['ENGINE'] += "key=" + _config['identity']['key'] + "&cx=" + _config['identity']['cx'] + "&q="
                else:
                    logger.error("key or cx not exists")
                    print("key or cx not exits")
                    exit(0)
        else:
            logger.error("engine :{} not implemented")
            print (_config['CURRENT_ENGINES'])
            exit (0)

    if args.query:
        _config['search_string'] =  args.query
    else:
        _config['search_string'] = 'test'

    if args.logging:
        if checkroute(_config['path']['log'],True):
            logger.info("Path ok : {0}".format(_config['path']['log']))

        name= _config['path']['log'] +"/{0}_{1}.log".format(_DATETIME, NAME)
        logging.basicConfig(filename=name, filemode='a', format='%(name)s - %(levelname)s - %(message)s')

    if args.config:
        logger.info("Getting data from configuration file {0}".format(args.config))

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

    if args.readfile :
        if len(args.readfile.split(" ")) > 1:
            for file in args.readfile.split(" "):
                if not os.path.exists(file):
                    logger.error('File {0} not found'.format(args.readfile))
                    exit(0)
            _config['FILE'] = args.readfile
        elif not os.path.exists(args.readfile):
            logger.error('File {0} not found'.format(args.readfile))
            exit(0)
        else:
            _config['FILE'] = args.readfile

    if args.json :
        _config['OUTPUT'] = _JSON
    elif args.csv :
        _config['OUTPUT'] = _CSV
    else:
        _config['OUTPUT'] = _SCREEN

    if args.stdout :
        _config['OUTPUT_AUX'] = True
    else:
        _config['OUTPUT_AUX'] = False

    if args.document:
        if checkroute(_config['path']['data']+"/"+_config['path']['document'], True):
            logger.info("Path ok : {0}".format(_config['path']['data']+"/"+_config['path']['document']))
        _config['search_string'] += " "+ returnExpresion (_config['extensions']['document'])
        _config['data_downloaded']['document']=True
    if args.markup:
        if checkroute(_config['path']['data']+"/"+_config['path']['markup'], True):
            logger.info("Path ok : {0}".format(_config['path']['data']+"/"+_config['path']['markup']))
        _config['search_string'] += " "+ returnExpresion(_config['extensions']['markup'])
        _config['data_downloaded']['markup'] = True
    if args.code:
        if checkroute(_config['path']['data']+"/"+_config['path']['code'], True):
            logger.info("Path ok : {0}".format(_config['path']['data']+"/"+_config['path']['code']))
        _config['search_string'] += " "+ returnExpresion(_config['extensions']['code'])
        _config['data_downloaded']['code'] = True
    if args.video:
        if checkroute(_config['path']['data']+"/"+_config['path']['video'], True):
            logger.info("Path ok : {0}".format(_config['path']['data']+"/"+_config['path']['video']))
        _config['search_string'] += " "+ returnExpresion(_config['extensions']['video'])
        _config['data_downloaded']['video'] = True
    if args.locationdata:
        if checkroute(_config['path']['data']+"/"+_config['path']['location'], True):
            logger.info("Path ok : {0}".format(_config['path']['data']+"/"+_config['path']['location']))
        _config['search_string'] += " "+ returnExpresion(_config['extensions']['location'])
        _config['data_downloaded']['location'] = True
    if args.picture:
        if checkroute(_config['path']['data']+"/"+_config['path']['picture'], True):
            logger.info("Path ok : {0}".format(_config['path']['data']+"/"+_config['path']['picture']))
        _config['search_string'] += " "+ returnExpresion(_config['extensions']['picture'])
        _config['data_downloaded']['picture'] = True


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

    if args.dorkfile and os.path.exists(args.dorkfile):
        _config['dorkfile'] = args.dorkfile
        _url = _config['ENGINE']
    elif args.dorkfile:
        logger.error('File {0} not found'.format(args.dorkfile))
        exit (0)

    if args.dontdelete :
        _config['DELETE'] = False
    else:
        _config['DELETE'] = True

    _url = _config['ENGINE'] + _config['search_string']

    return _config, _url

def dork(_config, _url):

    logger.info('Getting data from URL: {0}'.format(_url))

    ua = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'}
    #response = _conn.get(_url, headers=ua)
    response = requests.get(_url, headers=ua)
    if _config['VERBOSE']:
        mgmt_response(response.headers)
    aux = "/{0}_{1}_{2}.html".format(_DATETIME, base64.b64encode( _config['search_string'].encode()).decode("utf-8") , randomString())
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
    if _url is None:
        try:
            logger.error(html.find(id="infoDiv").text)
            _url = False
        except:
            pass
    else:
        _url = re.sub("/search\?q=","",_url)
    if _config['VERBOSE']:
        logger.debug('obtained URL: {0}'.format(_url))
        logger.debug('data saved in file: {0}'.format(name))
    return _url, name

def dork_api(_config, _url, count):

    logger.info('Getting data from URL: {0}'.format(_url))

    ua = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'}
    #response = _conn.get(_url, headers=ua)
    response = requests.get(_url, headers=ua)
    if _config['VERBOSE']:
        mgmt_response(response.headers)
    aux = "/{0}_{1}_{2}.json".format(_DATETIME, base64.b64encode( _config['search_string'].encode()).decode("utf-8") , randomString())
    try :
        aux = re.sub('/','',aux)
    except:
        pass
    name = _config['path']['tmp'] + "/"+ aux
    logger.info('Writting data in: {0}'.format(name))
    open(name, 'wb').write(response.content)
    json_data = json.loads(response.text)

    cd = data_found()
    if 'queries' in json_data.keys():
        if 'nextPage' in json_data['queries'].keys():
            cd.next_page= count*json_data['queries']['nextPage'][0]['count']
        else:
            cd.next_page = 0
    elif 'error' in json_data.keys():
            logger.error(' {0}'.format(json_data))
            print("\n\n{0}\n\n".format(json_data))
            exit(0)

    #_url = _url + "&start=" + str(cd.next_page)
    # if _url is None:
    #     try:
    #         logger.error(response.text)
    #         _url = False
    #     except:
    #         pass
    # if _config['VERBOSE']:
    #     logger.debug('obtained URL: {0}'.format(_url))
    #     logger.debug('data saved in file: {0}'.format(name))
    return _config['search_string'], name

def files2open(filename, _encoding='ISO-8859-1'):
    type=filename.split('.')[len(filename.split('.'))-1]
    if type in ['csv']:
        doc=  csv.DictReader(open(filename, mode='r'))
    else :
        f = open(filename, 'r', encoding=_encoding)
        doc = f.read()
        f.close()
    return doc, type

def showfiles(_config, files):
    if _config['ENGINE'] == 'https://www.google.com/search?q=':
        cd = data_found()
    else:
        cd = data_found(None, 'API')
    if _config['VERBOSE']:
        logger.debug("Files: {0}".format(str(files)))
    for file in files:
        if _config['VERBOSE']:
            logger.debug("Extracting data from: {0}".format(file))
        doc, type =  files2open(file)
        if type == "html":
            html = BeautifulSoup(doc, "html.parser")
            found = cd.items_found(html)
            if found:
                logger.info(found)
            resultado = cd.div_SECTION(html)
            for k in resultado:
                cd.div_DATA(k,file)
        elif type == "json":
            json_data = json.loads(doc)
            if 'kind' in json_data.keys():
                if _config['VERBOSE']:
                    logger.debug("url.template: {0}".format(
                        json_data['url']['template']))
                    logger.debug("queries.request.totalResults: {0}".format(
                        json_data['queries']['request'][0]['totalResults']))
                    logger.debug("queries.request.outputEncoding: {0}".format(
                        json_data['queries']['request'][0]['outputEncoding']))
                    logger.debug("queries.request.safe: {0}".format(
                        json_data['queries']['request'][0]['safe']))
                    logger.debug("context.title: {0}".format(
                        json_data['context']['title']))
                    logger.debug("searchInformation.totalResults: {0}".format(
                        json_data['searchInformation']['totalResults']))

            for item in json_data['items']:
                cd.add_data(None, None, None,None,None,item)

    file=manageoutput(_config, cd)
    return file

def loop(_config, _url, loop=1):
    cont = 0
    files = []
    if checkroute(_config['path']['tmp'], True):
        logger.info("Path ok : {0}".format(_config['path']['tmp']))
    while cont < loop:
        logger.info('count : {0}'.format(cont))
        cont += 1
        #_aux, _file = dork(_config, _url, conn)
        _aux = ""
        if _config['ENGINE'] == _config['search_engine']['google']+_config['search_engine']['google_search']:
            _aux, _file = dork(_config, _url)
        else:
            _aux, _file = dork_api(_config, _url, cont)
        if _aux is None:
            logger.info('Next page not found.')
            cont+=loop
        elif not _aux:
             exit (0)
        else:
            _url = _config['ENGINE'] + _aux + "&start=" + "{0}".format(10*cont)
            if _config['VERBOSE']:
                logger.debug('URL returned: {0}'.format(_url))
                logger.debug('filename returned: {0}'.format(_file))
        files.append(_file)
    return files

def deletefiles (files):
    for i in files:
        os.remove(i)
        logger.info('{0} deleted !!!'.format(i))

def downloaded_data (_config, file):
    for extension in _config['extensions']:
        if _config['VERBOSE']:
            logger.debug("Checking extension 4 download: {0}".format(extension))
        if _config['data_downloaded'][extension]:
            if _config['VERBOSE']:
                logger.debug("Checking extension {0} in {1}".format(extension, file))
            download_data(_config, extension, file)

def download_data (_config, _key, name):
    _conn = requests.session()
    if _config['VERBOSE']:
        logger.debug("Getting data from {0}".format(name))
    if os.path.exists(name):
        doc, type = files2open(name)
    else:
        logger.error ('File {0} not found'.format(name))
    if type in 'csv':
        for i in doc:
            if _config['VERBOSE']:
                logger.debug ("Downloading data from {0}".format(i['link']))
            filename=i['link'].split('/')[len(i['link'].split('/'))-1]
            try:
                type=filename.split('.')[len(filename.split('.'))-1]
            except:
                type=filename
            logger.info ("Document to download : [{0}], filetype :({1})".format(filename,type))
            _DONWLOAD=_config['path']['data']+"/"
            if type in _config['extensions'][_key]:
                _DONWLOAD+=_config['path'][_key]
                if checkroute(_DONWLOAD, True) and _config['VERBOSE']:
                        logger.debug("Path {0} OK".format(_DONWLOAD))
                _aux=_DONWLOAD+"/"+filename
                if not os.path.exists(_aux):
                    ua = {
                        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'}
                    #response = _conn.get(i['link'], headers=ua)
                    try:
                        response = requests.get(i['link'], headers=ua)
                    except Exception as ex:
                        logger.error("Error accessing {0}: {1}".format(i['link'],str(ex)))


                    if _config['VERBOSE']:
                        mgmt_response(response.headers)
                    logger.info("File {0} downloaded".format(_aux))
                    open(_aux, 'wb').write(response.content)
                    logger.info("File {0} saved !!!".format(_aux))
                else:
                    if _config['VERBOSE']:
                        logger.debug("File {0} exists yet !!!!".format(_aux))
            else:
                ua = {
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'}
                #response = _conn.get(i['link'], headers=ua)
                try:
                    response = requests.get(i['link'], headers=ua)
                except Exception as ex:
                    logger.error("Error accessing {0}: {1}".format(i['link'], str(ex)))

                if _config['VERBOSE']:
                    mgmt_response(response.headers)
                #logger.info("File {0} downloaded".format(_aux))
                type = response.headers['Content-Type'].split('/')[len(response.headers['Content-Type'].split('/'))-1]
                if type in _config['extensions'][_key]:
                    _DONWLOAD += _config['path'][_key]
                    _aux = _DONWLOAD + "/" + re.sub('"','',re.sub('=+','=',response.headers['Content-Disposition']).split('=')[1])
                    open(_aux, 'wb').write(response.content)
                    logger.info("File {0} saved !!!".format(_aux))
                else:
                    logger.error("type: {0} not in {1}".format(type,_config['extensions'][_key] ))

def manageoutput (_config, _data):
    name = ""
    def filename (_config) :
        _TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        return _TIMESTAMP+"_"+_GLOBAL_NAME
    if _config['OUTPUT'] == _SCREEN:
        if _config['VERBOSE']:
            logger.debug('screen output')
        _data.print()
    else:
        if checkroute(_config['path']['data'],True):
            logger.info("Path ok : {0}".format(_config['path']['data']))

        name = _config['path']['data']+"/"+filename(_config)
        if _config['OUTPUT'] == _JSON:
            name+=".json"
            if _config['VERBOSE']:
                logger.debug('screen output')
            logger.info('Writing data in {0}'.format(name))
            with open(name, 'w', encoding='utf8') as json_file:
                json.dump(_data.data, json_file, ensure_ascii=False)
            if _config['OUTPUT_AUX']:
                print(json.dumps(_data.data))
        elif _config['OUTPUT'] == _CSV:
            name+=".csv"
            logger.info('Writing data in {0}'.format(name))
            if _config['VERBOSE']:
                logger.debug('Keys found:{0}'.format(str(_data.keys())))
            csv_file = csv.writer(open(name, 'w'), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_file.writerow(_data.keys())
            if _config['OUTPUT_AUX']:
                print(_data.keys())
            for i in range(0, _data.current):
                aux = _data.show(i)
                _csv_data = []
                for key in  _data.keys():
                    try:
                        _csv_data.append(aux[key])
                    except:
                        _csv_data.append("")
                csv_file.writerow(_csv_data)
                if _config['OUTPUT_AUX']:
                    print(_csv_data)
    return name

def mgmt_response (headers):
    for i in headers:
        logger.debug ("[{0}]: {1}".format(i,headers[i]))

if __name__ == "__main__":
    dt = datetime.datetime.now()
    _config, _url = options()
    logger.info('Starting {0} at {1}...'.format(NAME, dt))
    #if _config['VERBOSE']:
    #    logger.debug('config: {0}'.format(_config))
    if 'FILE' in _config:
        # Para leer archivos
        if _config['VERBOSE']:
            logger.debug('Reading: {0}'.format([_config['FILE']]))
        aux=[]
        if len(_config['FILE'].split(" ")) > 1:
            aux = _config['FILE'].split(" ")
        else:
            aux.append(_config['FILE'])
        file=showfiles(_config, aux)
        downloaded_data(_config, file)
    elif 'dorkfile' in  _config:
        # archivo con expresiones
        doc, type = files2open (_config['dorkfile'],'utf-8')
        linecount=0
        name=_config['dorkfile'].split("/")[len(_config['dorkfile'].split("/"))-1]
        print (doc)
        for i in doc.split('\n'):
            str = i
            _aux = _url + i
            logger.info('URL to check: {0}'.format(_aux))
            _config['search_string']="{0}_line_{1}".format( name,linecount)
            linecount+=1
            files = loop(_config, _aux, _config['numpages'])
        file=showfiles(_config, files)
        downloaded_data(_config, file)
        if _config['DELETE']:
            deletefiles(files)
    else:
        files = loop(_config, _url, _config['numpages'])
        file=showfiles(_config, files)
        downloaded_data(_config, file)
        if _config['DELETE']:
            deletefiles(files)
    dt = datetime.datetime.now() - dt
    logger.info('Finished. Elapsed time {0}'.format(dt))

