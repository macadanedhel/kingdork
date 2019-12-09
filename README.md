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
  --document, -doc      search documents
  --markup, -mkp        search markup language
  --code, -code         search code
  --video, -vdo         search video
  --locationdata, -loc  search location data
  --picture, -pic       search picture
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
--- 
Example... if we want any documents about something :

```  python ./kingdork.py -n 10 -q "security incidents report 2019 filetype:pdf " -l english -csv -log 2>/dev/null ```

You may found in the output directory a file with the csve data, 20191209103108_google_search.csv, yyyymmddhhmmss_google_search.csv

> link,title,description,date
> https://www.ccn-cert.cni.es/informes/informes-ccn-cert-publicos/4041-ccn-cert-ia-13-19-threats-and-trends-report-executive-summary/file.html,Cyber threats and Trends 2019 - CCN-CERT - CNI,12 sept. 2019 - 3Figure source: Verizon: 2018 Data Breach Investigations Report. 8 .... .europa.eu/publications/annual-report-telecom-security-incidents-2017 ...,12 sept. 2019
> https://pages.riskbasedsecurity.com/hubfs/Reports/2019/2019%20MidYear%20Data%20Breach%20QuickView%20Report.pdf,2019 MidYear QuickView Data Breach Report - Risk Based ...,"the trend observed in the Q1 2019 report. ... remains the number one breach type for number of incidents, ... joined Risk Based Security in 2013 where she is.",
> https://www.nttsecurity.com/docs/librariesprovider3/resources/2019-gtir/2019_gtir_report_2019_uea_v2.pdf,Global Threat Intelligence Report - NTT Security,"In the 2019 GTIR, we also include details on some of the innovative research NTT ... services and incident response engagements, as well as vulnerability data.",
> https://www.accenture.com/_acnmedia/pdf-107/accenture-security-cyber.pdf,2019 Cyber Threatscape Report I Accenture,The Accenture Security iDefense Threat Intelligence Services team has observed a distinct and ... These incidents remain dangerous indicators for the future of .... The 2019 Cyber Threatscape report has discovered five factors that are.,
> https://www.isc2.org/-/media/ISC2/Landing-Pages/2019-Cloud-Security-Report-ISC2.ashx?la=en&hash=06133FF277FCCFF720FC8B96DF505CA66A7CE565,2019 ISC2 Cloud Security Report,2019 CLOUD SECURITY REPORT One in four organizations (28%) confirmed they experienced a cloud security incident in the past 12 months. This rise in observed cloud security incidents (compared to last year's survey) further serves to support the increased security concerns related to adoption of cloud computing.,
> https://www.aon.com/getmedia/4c27b255-c1d0-412f-b861-34c5cc14e604/Aon_2019-Cyber-Security-Risk-Report.aspx,2019 Cyber Security Risk Report - Aon,"2019 Cyber Security Risk Report. Aon's Cyber .... priority only after a cyber incident has occurred . To better .... breach via a third party, but only 35% rate their.",
> https://www.securindex.com/downloads/8b9f94c46a70c60b229b04609c07acff.pdf,X-Force Threat Intelligence Index2019 - Securindex,"X-Force Threat Intelligence Index 2019 ... monitored security clients, incident response services, ... Before we delve into the details of our report, below are.",
> https://www.enisa.europa.eu/publications/annual-report-telecom-security-incidents-2018/at_download/fullReport,annual report telecom security incidents 2018 - enisa - europa ...,ANNUAL REPORT TELECOM SECURITY INCIDENTS 2018. May 2019. 1. ABOUT ENISA. The European Union Agency for Network and Information Security ...,
> https://www.imperva.com/resources/reports/CyberEdge-2019-CDR-Report-v1.1.pdf,2019 Cyberthreat Defense Report - Imperva,Security Posture by IT Domain . .... Security Management and Operations Deployment Status . ...... executive-level reporting and data sharing for both incident.,

And in the log directory, yyyymmd_kingdork.log

```
kingdork - INFO - Starting kingdork at 2019-12-09 10:30:49.973025...
kingdork - INFO - count : 0
kingdork - INFO - Getting data from URL: https://www.google.com/search?q=security incidents report 2019 filetype:pdf &lr=lang_en
kingdork - INFO - Writting data in: tmp/20191209_security incidents report 2019 filetype:pdf &lr=lang_en_qjiayfox.html
kingdork - INFO - count : 1
kingdork - INFO - Getting data from URL: https://www.google.com/search?q=security+incidents+report+2019+filetype:pdf&lr=lang_en&tbs=lr:lang_1en&ei=ShTuXd_7MYfU-gTb7YOQDw&start=10&sa=N&ved=2ahUKEwjfyIrpoKjmAhUHqp4KHdv2APIQ8NMDegQICxBJ
kingdork - INFO - Writting data in: tmp/20191209_security incidents report 2019 filetype:pdf &lr=lang_en_jlpfimru.html

[...]

kingdork - INFO - Writting data in: tmp/20191209_security incidents report 2019 filetype:pdf &lr=lang_en_zqdrbega.html
kingdork - INFO - Openning file  tmp/20191209_security incidents report 2019 filetype:pdf &lr=lang_en_qjiayfox.html
kingdork - INFO - Aproximadamente 10.800.000 resultados (0,40 segundos) 
kingdork - INFO - Openning file  tmp/20191209_security incidents report 2019 filetype:pdf &lr=lang_en_jlpfimru.html

[...]

kingdork - INFO - Writing data in output/20191209103108_google_search.csv
kingdork - INFO - tmp/20191209_security incidents report 2019 filetype:pdf &lr=lang_en_qjiayfox.html deleted !!!
kingdork - INFO - tmp/20191209_security incidents report 2019 filetype:pdf &lr=lang_en_jlpfimru.html deleted !!!
kingdork - INFO - tmp/20191209_security incidents report 2019 filetype:pdf &lr=lang_en_aosqfcln.html deleted !!!

[...]

kingdork - INFO - Finished. Elapsed time 0:00:18.300802
```

With the options: 
- document 
- markup 
- code 
- video
- location 
- picture 

will download the next extensions: 

|option|extensions to download|
|------|----------------------|
|document | pdf,ps,xls,xlsx,ppt,pptx,doc,docx,odp,ods,odt,rtf,hwp,txt,tex,text|
|Markup | html,htm,wml,wap,xml,yml,yaml|
|code | bas,c,cc,cpp,cxx,h,hpp,cs,java,pl,py|
|video| mpg,avi,swf,webm,mkv,flv,vobmpg,mp2,mpeg,mpe,mpv,mov,qt,wmv,rm,rmvb,m4v,3gp,f4v,f4p,f4a,f4b|
|location | kml,kmz,gpx|
|picture| svg,jpg,jpeg,gif,png,tif,tiff,eps,ai,psd,epsai,indd,raw|

```
2019-12-09 22:28:03,294 - kingdork - INFO - download_data - Document to download : [accenture-2019-cost-of-cybercrime-study-final.pdf], filetype :(pdf)
2019-12-09 22:28:03,294 - kingdork - INFO - download_data - Document to download : [security-report-2019.pdf], filetype :(pdf)
2019-12-09 22:28:03,294 - kingdork - INFO - download_data - Document to download : [EN-Cybersicherheit_Bericht_2019.pdf], filetype :(pdf)
2019-12-09 22:28:03,294 - kingdork - INFO - download_data - Document to download : [2019-Cloud-Security-Report-ISC2.ashx?la=en&hash=06133FF277FCCFF720FC8B96DF505CA66A7CE565], filetype :(ashx?la=en&hash=06133FF277FCCFF720FC8B96DF505CA66A7CE565)
2019-12-09 22:28:06,701 - kingdork - INFO - download_data - File output/doc/EN-Cybersicherheit_Bericht_2019.pdf downloaded
```
---

## To Do
[CSE: list](https://developers.google.com/custom-search/v1/cse/list)

[Request Format](https://support.google.com/gsa/answer/6329265#4134d4ec-c7f1-4eff-ae65-b171e689ca5a)

[Google Advanced Search](https://www.google.com/advanced_search)

[XML API reference appendices](https://developers.google.com/custom-search/docs/xml_results_appendices#countryCollections)
## License

pa ti