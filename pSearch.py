#!/home/muzahid/linuxbrew/bin/python
import pdb
import sys
import json
import pprint
import time
import google
from multiprocessing.dummy import Pool as ThreadPool
from apiclient.discovery import build
from functools import partial

#--------------------------------------------------------
# Function for querying results
#--------------------------------------------------------
def queryGoogleApi(name, keywords, customsearchID, service) :

    pList = []

    res = service.cse().list(
      q=name,
      cx=customsearchID,
    ).execute()

    pprint.pprint(res['items'][0]['title'])
    pList.append({"researcher": res['items'][0]['title'],"paper": "NotFound", "keyword": "NotFound"})
    # for each paper find search for each keyword
    for paper in res['items'][0]['pagemap']['scholarlyarticle'] :
        for keyword in keywords :
            if keyword.strip().lower() in paper['name'].lower() :
                #pprint.pprint(paper)
                paperTuple = {"researcher": res['items'][0]['title'],"paper": paper, "keyword": keyword.strip()}
                pList.append(paperTuple)
                break

    pList.append({"researcher": "","paper": "", "keyword": "separator"})

    return pList

#--------------------------------------------------------
# Function for outputing results
#--------------------------------------------------------
def outputResults(output_filename, paperList) :

    target = open(output_filename, 'aw')
    currResearcher = ""

    for entry in paperList :
        if entry["paper"] == "" :
            target.write("---------------------------------------------------------\n")
        else :
            if(currResearcher != entry["researcher"]) :
                currResearcher = entry["researcher"]
                target.write(entry["researcher"] + "\n")
                target.write("---------------------------------------------------------\n")

            if(entry['paper'] != "NotFound" ) :
                target.write("Article: " + entry['paper']['name'] + "\n")
                target.write("Keyword: " + entry['keyword'] + "\n\n")


    target.close()

#--------------------------------------------------------
# Main
#--------------------------------------------------------
def main(argv) :
    print "Two parameters: ./pSearch.py namefile keywords";
    # Get configuration file
    #with open('/home/muzahid/projects/code/custom_search/PaperSearch/config.json') as data_file:
    #    config_data = json.load(data_file)

    config_data = {
    "type": "customsearch",
    "version": "v1",
    "developerKey": "AIzaSyDhETdVAVnuucoz41pgvct6EGkEdKA2pmI",
    "customsearchID": "013317773812904460726:bdzgcfd4oq8"
    }
    # Open input files
    namesFile = open(argv[1])
    keywords_input = open(argv[2])

    # Variables
    paperList = []
    names = []
    keywords = []
    output_filename = "Results.txt"

    # Open google api service
    service = build(config_data["type"], config_data["version"], developerKey=config_data["developerKey"])

    # Get keywords from input file into a resuable array
    for word in keywords_input :
        keywords.append(word)

    # Call a google search for each name
    for name in namesFile:
        paperList = queryGoogleApi(name, keywords, config_data["customsearchID"], service)
        time.sleep(0.5) # Allow only two request per second to avoid trottling
        # Output results
        outputResults(output_filename, paperList)

#--------------------------------------------------------
# Start
#--------------------------------------------------------
if __name__ == "__main__" :
    main(sys.argv)
