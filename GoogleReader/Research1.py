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
    <html><head>
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
    .alternatelook { background-color: #eeeeee }
    .item { padding: 10px; }
    .row {
    margin-top: 10px;
    border-left: 1px solid black;
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
    </style>
    </head><body>

    <div class='container'>
    '''
    return headerString


def render_footer():
    footerString = '''</div></body></html>'''
    return footerString



#     <script src="jquery-2.0.0.js"> </script>
#     <script>
#     $('.container').keyup(function(event) {
#         switch  (e.keyCode) {
#         case 37:
#         case 39:
#         }

#         });
#     </script>


# <script>$('div .item').first().addClass('selected')</script>
    
# <script>
# var currIndex = 0;
    
# $(document).keyup(function(e) {

#     switch (e.keyCode) {
#         case 74:
#         currIndex++;
#         break;
#         case 75:
#         currIndex--;
#         break;
#     }

#     if (currIndex < 0) 
#         currIndex = 0;
#     if ( currIndex > 19 )
#         currIndex=0;
    
#     //alert('keypress' + e.keyCode);
#     var selected = $("div .item");
#     //alert(selected.length + otheritems.length);

#     selected.each(function (index, domEle) {
#          if ($(this).is(".selected")) {
#              $(this).removeClass("selected");
#         }

#         if (currIndex === index) {
#              $(this).addClass("selected");
#              $('html, body').animate({
#                 scrollTop: $(this).offset().top}, 2000);
#              return;
#         }

#     });

#     });

#     //selectedItem.removeClass("selected");

#     // var selected = $(".selected");
#     // switch  (e.keyCode) {
#     // case 39:
#     //    selected.siblings.next().addClass("selected");
#     // }
# // if (e.keyCode == 38) { // up
# // var selected = $(".selected");
# // $("div .item").removeClass("selected");

# // // if there is no element before the selected one, we select the last one
# // if (selected.prev().length == 0) {
# //     selected.siblings().last().addClass("selected");
# // } else { // otherwise we just select the next one
# //     selected.prev().addClass("selected");
# // }
# // }
# </script>

# sharedby = sharedby.decode("utf-8")


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
        readerItem["updated"]).strftime('%Y-%m-%d %H:%M')

    if "via" in readerItem:
        for v in readerItem["via"]:
            Via = v["title"]

    if "origin" in readerItem:
        for o in readerItem["origin"]:
            if "title" in o:
                Origin = "<a href='" + readerItem["origin"]["htmlUrl"] + "'>" 
                Origin += readerItem["origin"]["title"] + "</a>"

    if (ItemNumber % 2) == 0:
        ItemString = "\n<div class='item'>"
    else:
        ItemString = "\n<div class='item alternatelook'>"

    ItemString += "<span id = 'item" + str(ItemNumber) + "'>"  
    ItemString += Origin + " : " + Via + " at " + TimeStamp + "</span>"

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
        ItemString += "<h3>" + UrlString + readerItem["title"] + "</a></h3>"

    if "content" in readerItem:
        ItemString += readerItem["content"]["content"]

    if "content" not in readerItem:
        if "summary" in readerItem:
            ItemString += readerItem["summary"]["content"]
        else:
            ItemString += "\n<div class='item' style='empty'>Empty ItemString"

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
    outputString += CommentString + "</div>"

    return outputString


def build_file_items(itemCol, outputfilename):
    itemCount = 0
    pageCount = 0
    mostComments = 0
    mostAnnots = 0
    prevPageCount = 0
    currentItem = 0

    # print str(len(itemCol["items"]))

    Pages = len(itemCol["items"]) / pageLength

    # randomPage = int(random.uniform(0, Pages))
    #
    # print str(randomPage) + " of " + str(Pages)
    #
    # for n in itemCol["items"]:
    #     itemCount += 1
    #     if ( itemCount % pageLength ) == 0 :
    #         pageCount += 1
    #     if prevPageCount != pageCount :
    #         prevPageCount = pageCount
    #     if pageCount == randomPage :
    #         Output += render_item(n, itemCount)
    #
    # filenameroot = outputfilename + str(pageCount).zfill(3) + ".html"
    # pageName = os.getcwd() + "/" + filenameroot + str(pageCount)
    # Output += render_footer()
    # completeOutput = Output.encode('utf-8')
    #
    # filename = outputfilename
    # f = codecs.open(filename, 'w' 'utf-8')
    # f.write(completeOutput)
    # f.close()
    # print 'wrote out file : ' + os.getcwd() + "/" + filename

    Output = ''

    myList = itemCol["items"]
    sortedList = sorted(myList, key=lambda x: x['updated'])

    print 'Pages: ' + str(Pages) + ' pageLength : ' + str(pageLength) 

    for n in sortedList:
        currentItem += 1
        if (currentItem % pageLength) == 0:
            print 'if (itemCount % pageLength) == 0:'
            prevfilename = outputfilename + str(pageCount - 1).zfill(3) + ".html"
            currentfilename = outputfilename + str(pageCount).zfill(3) + ".html"
            nextfilename = outputfilename + str(pageCount + 1).zfill(3) + ".html"
            pageCount += 1
            if pageCount > 1:
                print 'ClosingPage'
                CloseCurrentPage(pageCount, Output, outputfilename, 
                    Pages, prevfilename, nextfilename)
        if prevPageCount != pageCount:
            print 'if prevPageCount != pageCount:'
            Output = render_header()
            Output += RenderNavBar(pageCount, Pages, prevfilename, nextfilename)
            # OpenNewPage(pageCount, Output)
            prevPageCount = pageCount
        Output += render_item(n, currentItem)

    # close last page
    #Already closed if we end on the right page
    if (currentItem % pageLength) > 0 :
        CloseCurrentPage(prevPageCount, Output, outputfilename, Pages, prevfilename, nextfilename)


def CloseCurrentPage(pagenumber, Output, outputfilename, Pages, 
    prevfilename, nextfilename):
    Output += RenderNavBar(pagenumber, Pages, prevfilename, nextfilename)
    Output += render_footer()

    filename = outputfilename + str(pagenumber).zfill(3) + ".html"
    pageName = os.getcwd() + "/" + filename
    completeOutput = Output.encode('utf-8')

    f = codecs.open(filename, 'w' 'utf-8')
    f.write(completeOutput)
    f.close()
    print 'wrote out file : ' + os.getcwd() + "/" + filename


def OpenNewPage(pagenumber, Output):
    Output = render_header()


def RenderNavBar(pageCount, Pages, prevfilename, nextfilename):
    navString = ''
    navString += "<h2><div align='left'>Page " 
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
pageLength = 10

pp = pprint.PrettyPrinter(indent=2)

# txt = open('/Users/doug.churchman/Documents/src/data/shared-by-followers.json')
# sharedby = json.loads(txt.read().decode("utf-8"))
# build_file_items(sharedby, "SharedBy")
# #
# txt = open('/Users/doug.churchman/Documents/src/data/shared.json')
# shared = json.loads(txt.read().decode("utf-8"))
# build_file_items(shared, "Shared")
# #
# # pageLength = 10

# txt = open('/Users/doug.churchman/Documents/src/data/starred.json')
# shared = json.loads(txt.read().decode("utf-8"))
# build_file_items(shared, "Starred")


# txt = open('/Users/doug.churchman/Documents/src/data/allisonrae/starred.json')
# starred = json.loads(txt.read().decode("utf-8"))
# build_file_items(starred, "AlliStarred")


# txt = open('/Users/doug.churchman/Documents/src/data/allisonrae/liked.json')
# liked = json.loads(txt.read().decode("utf-8"))
# build_file_items(liked, "AlliLiked")


# txt = open('/Users/doug.churchman/Documents/src/data/allisonrae/shared.json')
# shared = json.loads(txt.read().decode("utf-8"))
# build_file_items(shared, "AlliShared")


txt = open('/Users/doug.churchman/Documents/src/data/allisonrae/shared-by-followers.json')
sharedby = json.loads(txt.read().decode("utf-8"))
build_file_items(sharedby, "AlliSharedBy")
