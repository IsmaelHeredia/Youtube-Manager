#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request,urllib.parse
from io import BytesIO,StringIO
import gzip
import json
import os,re
from unicodedata import normalize

class Functions(object):
                         
    def http_get(self,page):
        html = ""
        try:
            opener = urllib.request.build_opener()
            opener.addheaders = [("User-agent", "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36")]
            resource = opener.open(page,timeout=5)
            html = resource.read()
            resource.close()
        except:
            pass
        return html

    def http_get_gzip(self,page):
        html = ""
        try:
            opener = urllib.request.build_opener()
            opener.add_header = [("Accept-encoding", "gzip")]
            opener.add_header = [("User-agent", "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36")]
            resource = opener.open(page,timeout=5)
            if resource.info().get("Content-Encoding") == "gzip":
                buf = BytesIO(resource.read())
                f = gzip.GzipFile(fileobj=buf)
                html = f.read()
            resource.close()
            html = html.decode("utf-8", "ignore")
        except:
            pass
        return html

    def download(self,link,name):
        try:
            opener = urllib.request.build_opener()
            opener.addheaders = [("User-agent", "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36")]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(link, name)
            return True
        except:
            pass
            return False

    def url_encode(self,text):
        return urllib.parse.quote_plus(text)


    def clean_title_filename(self,fullpath):
        filename = ""
        path = os.path.dirname(fullpath)
        if path != "":
            filename = os.path.basename(fullpath)

        pre, ext = os.path.splitext(filename)
        pre = pre.replace(".","")
        filename = pre + ".mp3"

        filename = re.sub(r'[\\/*?:"<>|]',"",filename)
        filename = filename.replace("(","")
        filename = filename.replace(")","")
        filename = filename.replace("[","")
        filename = filename.replace("]","")

        filename = re.sub(
            r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
            normalize( "NFD", filename), 0, re.I
        )

        filename = normalize( 'NFC', filename)

        if path != "":
            filename = path + "\\" + filename

        return filename