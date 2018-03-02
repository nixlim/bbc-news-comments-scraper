# bbc-news-comments-scraper
A simple python script to scrape comments from one or many BBC News articles. This was tested to collect the many thousands of Brexit related discorse posted on the BBC News website.

## How to use
1. Go to a BBC news article with comments you're interested in, and view the source of the webpage. Alternateively, in Chrome, right-click on the 'View Comments' button and select 'Inspect'.
For example: http://www.bbc.co.uk/news/uk-politics-eu-referendum-36306681

2. Look within the HTML and for the string 'forumId=__CPS__' (without the Single Quotes). After '__CPS__' there will be a number, copy this number. For example '__CPS__43250035', then copy '43250035' 

3. Edit the 'articles' list in the python scraper code, add the relevant Article title and number as required. For example:
```
articles = {'This is an article':2891312 , 'This is another article', 123123}
```

4. Save, and then run the python script. If no database exists, this will create an Sqlite database, and then populate a table with the comments.
```
python3 ./scraper.py
```

## Requirements
The following python libraries are required to be installed:
- sqlite3
- requests
- re

These should come standard with most python installations however.


