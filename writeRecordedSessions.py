from glob import glob
import os
import re
import datetime

import bs4

"""Used to automate addition of recorded audio sessions to the DND website.
takes a folder path containing mp3 files named per the following:
yyyy.mm.dd - Campaign Name - Session Name.mp3
and creates a section for each one. Currenlt only works with AMC MRDR sessions
but could be exteneded using the campaignTag parameter. The files are not provided
with links as they need to be hosted on google drive. Instead the src attribute
for each audio tag is set to a placeholder of the form:
https://docs.google.com/uc?export=download&amp;id={id}
where {id} is replaced with the id of the link to the file in drive. (The id is
the characters listed after the "d/" part of the link url.)

# You will need to have a html file setup with a section tag with an id for each
campaign you want to process. The HTML_FILE_PATH is this file. The HTML_WRITE_PATH
gets wiped and replaced with the contents of the HTML_FILE_PATH file plus the tags
that are created for each audio file. After getting the desired output you will 
need to go through each audio src and provide the id from google drive. 
"""

MP3_FILE_DIRECTORY = r"C:\Users\HooDoo\Documents\GitHub\ManorInnDND.github.io\audio\sessions"
HTML_FILE_PATH = r"C:\Users\HooDoo\Documents\GitHub\ManorInnDND.github.io\recordedsessions.html"
HTML_WRITE_PATH = r"C:\Users\HooDoo\Documents\GitHub\ManorInnDND.github.io\test.html"
CAMPAIGN_TAG_ID = "amcMrdrRecordedSessions" #this should not be static if processing files from different campaigns


def main():
    targetDirectory = MP3_FILE_DIRECTORY
    audioFilePaths = get_audio_file_paths(targetDirectory)
    sessionDataSets = build_session_data_sets_from_file_paths(audioFilePaths)
    
    soup = bs4.BeautifulSoup(open(HTML_FILE_PATH, "r"),"html.parser")
    html_operations(soup, sessionDataSets)
    

    with open(HTML_WRITE_PATH,"w") as outputStream:
        wipe_stream(outputStream)
        outputStream.write(soup.prettify(formatter="html5"))
    
    
def get_audio_file_paths(targetDirectory):
    os.chdir(targetDirectory)
    audioFilePaths = glob("*.mp3", recursive=True)
    return audioFilePaths 

def build_session_data_sets_from_file_paths(audioFilePaths):
    sessionDataSets = []
    
    for audioFilePath in audioFilePaths:
        sessionDataSet = build_session_data_set(audioFilePath)        
        sessionDataSets.append(sessionDataSet)
    
    return sessionDataSets

def build_session_data_set(audioFilePath):
    sessionDataSet = {
        "dateForText":None,
        "dateForDatetimeAttr":None,
        "name":None,
        "campaign":None,
        "dm":None,
        "audioAltAttr":None,
        "strippedName": None}
    pattern = re.compile(r"(?P<date>[^-]*) - (?P<campaign>[^-]*) - (?P<name>.*)\.mp3$")
    result = pattern.match(audioFilePath)
    
    sessionDataSet["name"] = result.group("name")
    sessionDataSet["strippedName"] = result.group("name").replace(" ","").lower()
    sessionDataSet["campaign"] = result.group("campaign")
    sessionDataSet["dateForDatetimeAttr"] = build_html_date(result.group("date"),"dateTime")
    sessionDataSet["dateForText"] = build_html_date(result.group("date"), "text")
    sessionDataSet["audioAltAttr"] = build_html_audioAltAttr(audioFilePath)    

    return sessionDataSet

def build_html_date(fileNameDate, option="dateTime"):
    
    if option == "dateTime":
        return fileNameDate.replace(".","/")
    elif option == "text":
        isoFormat = fileNameDate.replace(".","-")
        dateObject = datetime.date.fromisoformat(isoFormat)
        dateString = dateObject.strftime(r"%b %d, %Y")
        dateStringMyFormat = format_date(dateString)
        return dateStringMyFormat
    else:
        print("Error")

def format_date(dateString):
    pattern = re.compile(r"(\d+),")
    result = pattern.search(dateString)
    dayOfMonthRaw = result.group(1)
    
    dayInt = int(dayOfMonthRaw)
    daySuffixed =  get_day_suffixed(dayInt)
    formattedDate = pattern.sub(daySuffixed + ",", dateString)
    
    return formattedDate
    
def get_day_suffixed(day):
    
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]
    
    return str(day) + suffix

def build_html_audioAltAttr(audioFilePath):
    # relativePathPrefix = "audio/sessions/"
    # relativePath = relativePathPrefix + audioFilePath
    return audioFilePath

def html_operations(soup, sessionDataSets):
    campaignTag = soup.find(id=CAMPAIGN_TAG_NAME)
    
    for sessionDataSet in sessionDataSets:
        sessionSectionTag = build_session_section_tag(soup, sessionDataSet)
        campaignTag.append(sessionSectionTag)

def build_session_section_tag(soup, sessionDataSet):
    sectionTag = soup.new_tag("section", attrs={"id":sessionDataSet["strippedName"], "class":"sessionRecording"})
    headerTag = new_tag_with_contents(soup, "h4",sessionDataSet["name"])
    descriptionTag = build_description_tag(sessionDataSet["dateForDatetimeAttr"],
                        sessionDataSet["dateForText"], sessionDataSet["dm"],
                        soup)
    audioTag = build_audio_tag(soup,sessionDataSet["audioAltAttr"])

    sectionTag.extend([headerTag, descriptionTag, audioTag])
    
    return sectionTag

def build_description_tag(datetime, dateText, dm, soup):
    descriptionTag = soup.new_tag("p",attrs={"class":"Chapter_CORE-BODY"})
    descriptionTag.append("No description provided")
    descriptionTag.append(soup.new_tag("br"))
    descriptionTag.append(new_tag_with_contents(soup,"b","Played on: "))
    descriptionTag.append(build_date_tag(soup, datetime, dateText))
    descriptionTag.append(soup.new_tag("br"))
    descriptionTag.append(new_tag_with_contents(soup,"b","DM: "))
    descriptionTag.append("Not Set")
        
    return descriptionTag

def new_tag_with_contents(soup, tagName, stringContents):
    newTag = soup.new_tag(tagName)
    newTag.append(stringContents)
    return newTag

def build_date_tag(soup, datetimeAttr, dateText):
    dateTag = soup.new_tag("date", datetime=datetimeAttr)
    dateTag.append(dateText)
    return dateTag

def build_audio_tag(soup, audioAltAttr):
    audioTag = soup.new_tag("audio", controls="", alt=audioAltAttr)
    googleDriveLinkPlaceholder = r"https://docs.google.com/uc?export=download&id={id}"
    sourceTag = soup.new_tag("source", src=googleDriveLinkPlaceholder, type="audio/mpeg")
    audioTag.append(sourceTag)
    return audioTag

def wipe_stream(stream):
    stream.seek(0)
    stream.truncate()

main()