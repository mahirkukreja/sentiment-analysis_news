Sentiment Analyis of news from Hindu via vader.

News from the last five days was crawled from four cities and vader was used for implementing sentiment analysis. If we get more data, we can try applying something like word2vec to try and understand the kind of words that are generally closer to each other in the vector space and we can use them to form clusters which might make sentiment classification easier. If we get labelled data, that'll be best.

Packages needed:
Selenium,pyvirtualdisplay,xvfb,urllib2,bs4,pickle,re,pandas,time,vader,chromedriver,datetime,os

Change the paths in my script based on where you download them in your system.

Then type python untrodden.py inside the same folder in terminal. It'll take about an hour to run and the output will be saved in the file output.csv.
