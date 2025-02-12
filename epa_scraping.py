import argparse
from urllib.request import urlopen
import re
from bs4 import BeautifulSoup
import os

class Webpage():
    def __init__(self, url):
        self.url = url
        self.bs = None
        self.scrapePage()
    
    def scrapePage(self):
        try:
            page = urlopen(self.url)
            html = page.read().decode('utf-8')
            self.bs = BeautifulSoup(html, "html.parser")
        except Exception as e:
            print(f"{e} occurred while fetching {self.url}")

    def getLinks(self):
        links = []

        if not self.bs:
            print("error, no BeautifulSoup instance")
            return links
        
        for link in self.bs.find_all('a'):
            h = link.get('href')
            if h:
                links.append(h)

        return links
    
    def getPdfs(self):
        pdfLinks = []

        if not self.bs:
            print("error, no BeautifulSoup instance")
            return pdfLinks
        
        for link in self.bs.find_all('a'):
            h = link.get('href')
            if h:
                if ".pdf" in h.lower() and h not in pdfLinks:
                    pdfLinks.append(h)

        return pdfLinks
    
def downloadFile(url, dest):
    try:
        page = urlopen(url)
        with open(dest, 'wb') as f:
            f.write(page.read())
    except Exception as e:
        print(f"{e} occurred while downloading {url}")


def main():
    baseurl = "https://www.epa.gov"

    enforcement = "https://www.epa.gov/enforcement/civil-and-cleanup-enforcement-cases-and-settlements"

    w = Webpage(enforcement)

    links = w.getLinks()
    fullEnforcementUrls = []

    for l in links:
        if l and 'enforcement' in l:
            fullEnforcementUrls.append(f"{baseurl}{l}")

    basedir = "enforcementPdfs/"
    if not os.path.exists(basedir):
        os.makedirs(basedir)

    for l in fullEnforcementUrls:
        #print(f"Fetching html for link {l}")
        if l:
            w = Webpage(l)
            pdf = w.getPdfs()
            pdfDir = l.split("/")
            pdfBaseDir = ""
            if len(pdfDir) > 1:
                pdfDir = pdfDir[-1]
                pdfBaseDir = f"{basedir}{pdfDir}/"
                if not os.path.exists(pdfBaseDir):
                    os.makedirs(pdfBaseDir)

                for p in pdf:
                    filename = p.split("/")
                    if len(filename) > 1:
                        filename = filename[-1]
                        fullFilename = f"{pdfBaseDir}{filename}"
                        if "http://" in p or "https://" in p:
                            fullurl = p
                        else:
                            fullurl = f"{baseurl}{p}"
                        downloadFile(fullurl, fullFilename)


if __name__ == "__main__":
    main()