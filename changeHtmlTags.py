from glob import glob
import os

import bs4

TARGET_TAG_FILTER_SETS = [
    {"targetTagClass": "Chapter_CHAPTER-TITLE", "changeToTagName": "h1"},
    {"targetTagClass": "Chapter_CHAPTER-SECTION", "changeToTagName": "h2"},
    {"targetTagClass": "Chapter_SECTION-HEADER-1", "changeToTagName": "h3"},
    {"targetTagClass": "Chapter_SECTION-HEADER-2", "changeToTagName": "h4"}
]

def main():
    targetFilePaths = get_file_paths()
    
    for targetFilePath in targetFilePaths:
        with open(targetFilePath, "r+") as stream:
            soup = stream_to_processed_soup(stream)
            wipe_stream(stream)
            stream.write(soup.prettify(formatter="html5"))

def get_file_paths():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    filePaths = glob("*.html", recursive=True)
    return filePaths

def stream_to_processed_soup(stream):
    soup = bs4.BeautifulSoup(stream, "html.parser")
    process_soup(soup)
    return soup

def process_soup(soup):
    for tagFilterSet in TARGET_TAG_FILTER_SETS:
        targetTags = soup.find_all("p", class_=tagFilterSet["targetTagClass"])
        process_tags(targetTags, tagFilterSet)

def process_tags(tags, tagFilterSet):
    for tag in tags:
        tag.name = tagFilterSet["changeToTagName"]
        del tag["class"]

def wipe_stream(stream):
    stream.seek(0)
    stream.truncate()

main()