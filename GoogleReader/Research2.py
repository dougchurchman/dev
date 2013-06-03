# -*- coding: utf-8 -*-
import sys
import os
import json
import pprint
import codecs
import datetime
import random

from mako.template import Template


def render_header():
    headerString = '''
    <html><head><title>Google Reader Flatfile</title>
    <link rel='stylesheet' type='text/css' href='bootstrap2.css'>
    <style>
    body {
    margin: 0;
    font-family: Georgia, serif;
    font-size: 18px;
    line-height: 2.0;
    color: #222222;
    background-color: #ffffff;}
    .container { width: 940px; margin-left: auto; margin-right: auto;}
    .alternatelook { background-color: #dddddd }
    .item { padding: 10px; }
    .row {
    margin-top: 10px;
    border-left: 1px solid black;
    clear: both;
    background-color: #eeeeee;
    }
    .comment {
    font-family: consolas, sans-serif;
    font-size: 16px;
    background-color: #e0e0ff;
    margin-left: -15px;
    margin-right: -15px;
    }
    .annotation {
    font-family: proxima, sans-serif;
    font-size: 16px;
    padding-top: 20px;
    background-color: #c0c0dd;
    display: block;
    margin-left: -20px;
    margin-right: -20px;
    padding-left: 50px;
    }
    .selected {
    background-color: #f0a0f0;
    }
    .PageTitle {
    float: left;
    margin-right: 200px;
    }
    .PageNav {
    float: right;
    width: 200px;
    }
    h2 {clear: all}
    h3 {clear: all; line-height: 1.1;}
    .itemorigin {
    float: right;
    width: 200px;
    font-size: 12px;
    line-height: 1.1;
    align: right;
    }

    .itemtitle {
    
    margin-right: 240px
    line-height: 1.1;
    font: 175% bold;
    font-family: proxima bold, sans-serif bold;
    font-weight: bold;
    }
    .itemContent {
    clear: all;
    background-color: #ffffff;
    padding: 10px;

    }
    .alternatelook .itemContent {
    background-color: #eeeeee;
    }
    .parentNav a:visited { color: #eeeeee ; }
    .parentNav a:link { color: #eeeeee ; }
    </style>
    </head><body>
<div class = 'parentNav' style='align: center; font: 125%; color: #eeeeee; background-color: #006;' align='center'>
<a href='DougStarred001.html'>Starred</a>
 - <a href='DougShared001.html'>Shared</a>
 - <a href='DougFollowers001.html'>FollowerShares</a>
</div>
    <div class='container'>
    '''
    return headerString


def render_footer():
    footerString = '''</div></body></html>'''
    return footerString

def render_item(readerItem=None, ItemNumber=0):
    CommentString = ""
    Itemstring = ""
    AnnotString = ""
    TimeStamp = ""
    CommentNum = 0
    UrlString = ""
    Via = ""
    Origin = ""

    TimeStamp = datetime.datetime.fromtimestamp(
        readerItem["updated"]).strftime('%m/%d/%Y %I:%M %p')

    if "via" in readerItem:
        for v in readerItem["via"]:
            Via = v["title"]

    if "origin" in readerItem:
        for o in readerItem["origin"]:
            if "title" in o:
                Origin = "<a href='" + readerItem["origin"]["htmlUrl"] + "'>" 
                Origin += readerItem["origin"]["title"] + "</a>"
                if len(Via) > 0 : 
                    Origin += " : " + Via  

    if (ItemNumber % 2) == 0:
        ItemString = "\n<div class='item'>"
    else:
        ItemString = "\n<div class='item alternatelook'>"

    ItemString += "<span class='itemorigin' id = 'item" + str(ItemNumber) + "'>"  
    ItemString += Origin + " <br></br> " + TimeStamp + "</span>"

    if "canonical" in readerItem:
        for cn in readerItem["canonical"]:
            UrlString = "<a href = '" + cn["href"] + "'>"
    elif "alternate" in readerItem:
        for al in readerItem["alternate"]:
            if "href" in al:
                UrlString = "<a href = '" + al["href"] + "'>"
    else:
        UrlString = "<a name='unlinked'>"

    if "title" in readerItem:
        ItemString += "<span class='itemtitle'>" + UrlString + readerItem["title"] + "</a></span>"

    if "content" in readerItem:
        ItemString += "\n<div class='itemcontent'>" + readerItem["content"]["content"]

    if "content" not in readerItem:
        if "summary" in readerItem:
            ItemString += "\n<div class='itemcontent'>" + readerItem["summary"]["content"]
        else:
            ItemString += "\n<div class='itemcontent' style='empty'>Empty ItemString"

    ItemString += "</div>"

    if "comments" in readerItem:
        for c in readerItem["comments"]:
            CommentNum += 1
            CommentString += "\n<div class='comment'> " + "<b> " 
            CommentString += c["author"] + ":</b> " + c["htmlContent"] 
            CommentString += "</div>"

    if "annotations" in readerItem:
        for a in readerItem["annotations"]:
            AnnotString = "\n<div class='annotation'>" 
            AnnotString += a["author"] + ": " 
            AnnotString += a["content"] + "</div>"

    ItemString = ItemString.encode('ascii', 'xmlcharrefreplace')
    AnnotString = AnnotString.encode('ascii', 'xmlcharrefreplace')
    CommentString = CommentString.encode('ascii', 'xmlcharrefreplace')
    outputString = "<div class='row'>" +  ItemString + AnnotString 
    outputString += CommentString + "</div></div>"

    return outputString


def build_file_items(itemCol, outputfilename):
    itemCount = 0
    pageCount = 0
    mostComments = 0
    mostAnnots = 0
    prevPageCount = 0
    currentItem = 0

    Pages = len(itemCol["items"]) / pageLength

    Output = ''

    myList = itemCol["items"]
    sortedList = sorted(myList, key=lambda x: x['updated'])

    print 'Pages: ' + str(Pages) + ' pageLength : ' + str(pageLength) 

    Output = render_header()
    Output += RenderNavBar(pageCount, Pages, outputfilename)
            
    for n in sortedList:
        currentItem += 1
        if (currentItem % pageLength) == 0 :
            # print 'if (itemCount % pageLength) == 0:'
            if pageCount > 0:
                # print 'ClosingPreviousPage'
                CloseCurrentPage(pageCount, Output, outputfilename, Pages)
            pageCount += 1
            
        if prevPageCount != pageCount:
            # print 'if prevPageCount != pageCount:'
            Output = render_header()
            Output += RenderNavBar(pageCount, Pages, outputfilename)
            prevPageCount = pageCount
        Output += render_item(n, currentItem)

    # close last page
    CloseCurrentPage(prevPageCount, Output, outputfilename, Pages)


def CloseCurrentPage(pagenumber, Output, outputfilename, Pages):

    Output += RenderNavBar(pagenumber, Pages, outputfilename)
    Output += render_footer()

    filename = outputfilename + str(pagenumber).zfill(3) + ".html"
    pageName = os.getcwd() + "/" + filename
    completeOutput = Output.encode('utf-8')

    f = codecs.open(filename, 'w' 'utf-8')
    f.write(completeOutput)
    f.close()
    print 'wrote out file : ' + os.getcwd() + "/" + filename

def RenderNavBar(pageCount, Pages, outputfilename):


    prevfilename = outputfilename + str(pageCount - 1).zfill(3) + ".html"
    currentfilename = outputfilename + str(pageCount).zfill(3) + ".html"
    nextfilename = outputfilename + str(pageCount + 1).zfill(3) + ".html"

    navString = ''
    navString += "<h2><div align='left' class=PageTitle>Page " 
    navString += str(pageCount) + " of " + str(Pages)
    navString += "</div><div align='right' class=PageNav>"
    if pageCount > 1:
        navString += "<a href='" + prevfilename
        navString += "'> <<" + str(pageCount - 1) + " </a>"
    if pageCount < Pages:
        navString += " - "
    if pageCount < Pages:
        navString += "<a href='" + nextfilename 
        navString += "'> " + str(pageCount + 1) + ">> </a></div>"
    navString += "</h2>"

    return navString


TotalSharedByComments = 0
TotalSharedByAnnot = 0
TotalSharedComments = 0
TotalSharedAnnot = 0
display = 1
itemContent = ""
previousContent = ""
itemDefs = []
commentDefs = []
annotationDefs = []
sharedbyDefs = []

itemCount = 0
pageCount = 0
mostComments = 0
mostAnnots = 0
pageLength = 20

pp = pprint.PrettyPrinter(indent=2)

txt = open('/Users/doug.churchman/Documents/src/data/shared-by-followers.json')
sharedby = json.loads(txt.read().decode("utf-8"))
build_file_items(sharedby, "DougFollowers")

txt = open('/Users/doug.churchman/Documents/src/data/shared.json')
shared = json.loads(txt.read().decode("utf-8"))
build_file_items(shared, "DougShared")

txt = open('/Users/doug.churchman/Documents/src/data/starred.json')
shared = json.loads(txt.read().decode("utf-8"))
build_file_items(shared, "DougStarred")


# txt = open('/Users/doug.churchman/Documents/src/data/allisonrae/starred.json')
# starred = json.loads(txt.read().decode("utf-8"))
# build_file_items(starred, "AlliStarred")

# txt = open('/Users/doug.churchman/Documents/src/data/allisonrae/liked.json')
# liked = json.loads(txt.read().decode("utf-8"))
# build_file_items(liked, "AlliLiked")

# txt = open('/Users/doug.churchman/Documents/src/data/allisonrae/shared.json')
# shared = json.loads(txt.read().decode("utf-8"))
# build_file_items(shared, "AlliShared")

# txt = open('/Users/doug.churchman/Documents/src/data/allisonrae/shared-by-followers.json')
# sharedby = json.loads(txt.read().decode("utf-8"))
# build_file_items(sharedby, "AlliSharedBy")
