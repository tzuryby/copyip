
import sys
import os
import urllib2
from bs4 import BeautifulSoup as bsoup

print sys.argv

if len(sys.argv) < 3:
    print "Usage example: python copy.py https://www.github.com/Netflix /path/to/target-repo-directory"
    sys.exit(1)

orgurl = sys.argv[1]
targetdir = sys.argv[2]
# parallel = sys.argv[3]


# move to targetdir
print "targetdir", targetdir
os.chdir(targetdir)

# normalize url
if "?" not in orgurl:
    orgurl = orgurl + "?page="
else:
    orgurl = orgurl.split("?")[0] + "?page="

print "orgurl", orgurl
# read page
def read_page(url):
    print "reading", url
    response = urllib2.urlopen(url)
    return bsoup(response.read(), "html.parser")

def grab_last_page(page_content):
    pages = page_content.find("div", class_="paginate-container").find_all("a")
    if len(pages) > 3:
        return int (pages[-2].text)
    else:
        return "1"
    

def extract_repo_links(page_content):
    return (elem.attrs["href"] for elem in page_content.find_all("a", itemprop="name codeRepository"))

def clone_repo(link):
    repo_full_url = "https://github.com%s.git" % link
    os.system("git clone %s" % repo_full_url)
    # print ("git clone %s" % repo_full_url)

# get the last page number from "div.paginate-container" of 1st page
page_content = read_page(orgurl + "1")
last_page_number = grab_last_page(page_content)


# print (page_content)
print (last_page_number)

# firsr page
for link in extract_repo_links(page_content):
    clone_repo(link)

if grab_last_page > 0:
    for pagenum in xrange(2,last_page_number+1):
        page_content = read_page(orgurl + str(pagenum))
        for link in extract_repo_links(page_content):
            clone_repo(link)
