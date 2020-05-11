#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functions import functions
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

class googleSearch(object):

    def __init__(self):
        self.functions = functions.Functions()
        self.excludes = ["webcache.googleusercontent.com","support.google.com","policies.google.com"]

    def search_pages(self,string,count):
        links_founds = []
        string = str(string)
        number = 0
        for i in range(1,count+1):
            link = "https://www.google.com.ar/search?q="+string+"&start="+str(number)
            content = self.functions.http_get(link)
            try:
                soup = BeautifulSoup(content.decode("utf-8", "ignore"),"html.parser")
                links = soup.findAll("a",attrs={"ping":re.compile("^/url")})
                if links:
                    for link in links:
                        link = link["href"]
                        split_url = urlparse(link)
                        host_url = split_url.netloc
                        if not host_url in str(self.excludes):
                            links_founds.append(link)
                number = number + 10
            except:
                raise
        return links_founds

    def send_first_result(self,string):
        result = ""
        links_founds = []
        string = str(string)
        link = "https://www.google.com/search?q="+string+"&start=0"
        content = self.functions.http_get(link)
        try:
            soup = BeautifulSoup(content.decode("utf-8", "ignore"),"html.parser")
            links = soup.findAll("a",attrs={"ping":re.compile("^/url")})
            if links:
               for link in links:
                   link = link["href"]
                   split_url = urlparse(link)
                   host_url = split_url.netloc
                   if not host_url in str(self.excludes):
                       links_founds.append(link)
        except:
            pass

        if links_founds:
            result = links_founds[0]

        return result