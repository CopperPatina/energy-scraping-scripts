import sys
import argparse
from urllib.request import urlopen
import urllib
import re
import os
import ssl
# MODULES YOU NEED TO INSTALL:
#   requests
#   bs4
#   urllib3

try:
    import requests
except ImportError:
    sys.exit("""to install, run: pip install requests""")
try:
    from bs4 import BeautifulSoup
except ImportError:
    sys.exit("""to install, run: pip install beautifulsoup4""")
try:
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except ImportError:
    sys.exit("""to install, run: pip install urllib3""")

class Webpage():
    def __init__(self, url):
        self.url = url
        self.bs = None
        self.scrapePage()

    def scrapePage(self):
        try:
            scontext = ssl.SSLContext(ssl.PROTOCOL_TLS)
            scontext.verify_mode = ssl.VerifyMode.CERT_NONE
            page = urlopen(self.url, context=scontext)

            html = page.read().decode('utf-8')
            self.bs = BeautifulSoup(html, "html.parser")
        except urllib.error.HTTPError as e:
            if str(e.code) == '404':
                print(f"Error: Page not found (404) at {self.url}")
                with open(f"/Users/kathryn/EPA/keywordScraping/TheForbiddenWords.txt", 'a') as f:
                    f.write(f"{self.url}\n")
            else:
                print(f"An HTTP error occurred: {e}")
        except Exception as e:
            print(f"{e} occurred while fetching {self.url}")

    def checkKeywords(self, keywords):
        matches = []
        if not self.bs:
            print(f"error, no BeautifulSoup instance for {self.url}")
            return matches
        text = str(self.bs)
        for word in keywords:
            if word in text:
                matches.append(word)
        return matches

    def getLinks(self):
        links = []

        if not self.bs:
            print(f"error, no BeautifulSoup instance for {self.url}")
            return links
        
        for link in self.bs.find_all('a'):
            h = link.get('href')
            if h:
                links.append(h)

        return links

    def getFolders(self):

        folderNames = []

        if not self.bs:
            print("error, no BeautifulSoup instance")
            return folderNames

        for link in self.bs.find_all('a'):
            h = link.get('href')
            if h:
                check_fold = re.compile("^[^.\/]+\/$")
                if check_fold.match(h) and h not in folderNames:
                    folderNames.append(h)
        return folderNames

    def getFiles(self):
        fileNames = []

        if not self.bs:
            print("error, no BeautifulSoup instance")
            return fileNames

        for link in self.bs.find_all('a'):
            h = link.get('href')
            if h:
                check_file = re.compile("^[^.]*\.(csv|pdf|xsl|xlsx|zip|doc|docx)$")
                if check_file.match(h) and h not in fileNames:
                    fileNames.append(h)

        return fileNames
    
def downloadFile(url, dest, chunk_size=1024):
    try:
        # scontext = ssl.SSLContext(ssl.PROTOCOL_TLS)
        # scontext.verify_mode = ssl.VerifyMode.CERT_NONE
        # page = urlopen(url, context=scontext)
        page = requests.get(url, stream=True, verify=False)
        total_size = int(page.headers.get('content-length', 0))
        written_size = 0
        progress = ""
        print("\t"+url)
        print("\t0%", end="\t---\t")
        with open(dest, 'wb') as f:
            for chunk in page.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                written_size += len(chunk)
                if (written_size >= total_size / 4) & (progress == ""):
                    progress = "25%"
                    print(progress, end="\t---\t")
                elif (written_size >= total_size / 2) & (progress == "25%"):
                    progress = "50%"
                    print(progress, end="\t---\t")
                elif (written_size >= total_size * 3 / 4) & (progress == "50%"):
                    progress = "75%"
                    print(progress, end="\t---\t")
            # f.write(page.read())
        print("100%")
    except Exception as e:
        print(f"{e} occurred while downloading {url}")

def getFilePaths(page, folder):
    print("Finding file paths:", folder)
    filePaths = []
    # Get files directly within that folder
    fileChildren = page.getFiles()
    for f in fileChildren:
        filePaths.append(folder + f)
    # Get files in subfolders
    subfolders = page.getFolders()
    for f in subfolders:
        folderChild = Webpage(page.url + f)
        folderChildFiles = getFilePaths(folderChild, folder + f)
        filePaths.extend(folderChildFiles)
    print(filePaths)
    return filePaths

def downloadSubFiles(page, folder, savedir, chunk_size):
    print("Finding file paths:", folder)
    if not os.path.exists(savedir + folder):
        os.makedirs(savedir + folder)
    # Get files directly within that folder
    fileChildren = page.getFiles()
    for f in fileChildren:
        downloadFile(page.url + f, savedir + folder + f, chunk_size)
    # Get files in subfolders
    subfolders = page.getFolders()
    for f in subfolders:
        folderChild = Webpage(page.url + f)
        downloadSubFiles(folderChild, folder + f, savedir, chunk_size)


def main():

# ------------------------ MODIFY THESE -------------------------
    savedir = "/Users/kathryn/EPA/keywordScraping/"
    chunk_size = 1024
 # ---------------------------------------------------------------

    if not os.path.exists(savedir):
        os.makedirs(savedir)

    # Check existing folders
    baseUrl = "https://www.epa.gov"
    parentUrl = "https://www.epa.gov/environmental-topics/air-topics"

    keywords = ["renewable", "climate"]
    
    pagesChecked = {}
    pagesToCheck = [parentUrl]

    while len(pagesToCheck) > 0:
        page = Webpage(pagesToCheck[0])
        print(f"Getting links from {pagesToCheck[0]}")
        pagesToCheck = pagesToCheck[1:]
        links = page.getLinks()
        for link in links:
            if 'http' not in link:
                link = f"{baseUrl}{link}"
            if link not in pagesChecked and link not in pagesToCheck and ".gov" in link:
                pagesToCheck.append(link)
                pagesChecked[link] = 1
                w = Webpage(link)
                matches = w.checkKeywords(keywords)
                if matches:
                    filesToDownload = w.getFiles()
                    for file in filesToDownload:
                        filename = ''
                        name = file.split('/')
                        if len(name) >= 1:
                            filename = name[-1]
                        if 'www' in file and 'http' not in file:
                            fileUrl = f"https://{file}"
                        if 'http' not in file:
                            fileUrl = f"{baseUrl}{file}"
                        if filename and ".gov" in fileUrl:
                            dest = f"{savedir}{filename}"
                            downloadFile(fileUrl, dest)
                            for word in matches:
                                with open(f"{savedir}{word}.txt", 'a') as f:
                                    f.write(f"{link},{file}\n")

if __name__ == "__main__":
    main()