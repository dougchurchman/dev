# -*- coding: utf-8 -*-
import sys
import json
import pprint
from mako.template import Template
import codecs

pp = pprint.PrettyPrinter(indent=2)

# txt = open('/Users/doug.churchman/Documents/src/data/shared-by-followers.json')
txt = open('/Users/doug.churchman/Documents/src/data/shared.json')
sharedby = json.loads(txt.read().decode("utf-8"))


# txt = open('/Users/doug.churchman/Documents/src/data/shared.json')
# shared = json.loads(txt.read().decode("utf-8"))


# Build output file
# Header
# Body
# Footer


# sharedby = sharedby.decode("utf-8")
def render_item(readerItem=None, ItemNumber=0) :
    CommentString = ""
    Itemstring = ""
    AnnotString = ""
    
    CommentNum = 0
    
    if "content" in readerItem : 
        ItemString = "\n<div class='item'>" + str(ItemNumber) + " : " + readerItem["content"]["content"]  + "</div>"
    
    if "content" not in readerItem :
        ItemString = "\n<div class='item' style='empty'>Empty Item</div>"
    
    ItemString = ItemString.encode('ascii', 'xmlcharrefreplace')
    
    if "comments" in readerItem:
        for c in readerItem["comments"] : 
            CommentNum += 1
            CommentString += "\n<div class='comment'> comment - " + str(CommentNum) + "<b>" + c["author"] + ":</b> " + c["htmlContent"] + "</div>"

    if "annotations" in n :
        for a in readerItem["annotations"] :
            AnnotString = "\n<div class='annotation'> annotation - " + a["author"] + ": " + a["content"] + "</div>"
        
    outputString = AnnotString + ItemString + CommentString    
    # outputString = Template(outputString)
    
    return outputString


TotalSharedByComments = 0
TotalSharedByAnnot = 0
TotalSharedComments = 0
TotalSharedAnnot = 0
display=1
itemContent = ""
previousContent = ""
itemDefs = []
commentDefs = []
annotationDefs = []
sharedbyDefs = []

# add itemDef to object
# if its not in there, add it

# do this for comments and annotations

itemCount = 0
pageCount = 0
mostComments = 0
mostAnnots = 0
prevPageCount = 0
pageLength = 100

sharedByOutput = ""

# print sharedby.keys()
for n in sharedby["items"]:
    # print n["content"]["content"]
    itemCount += 1
    if ( itemCount % pageLength ) == 0 : 
        pageCount += 1
    
    if prevPageCount != pageCount :
        # Finish current page
        # Open a new file
        prevPageCount = pageCount
    
    if pageCount == 0 :
        sharedByOutput += render_item(n, itemCount)
        
    # itemContent = str(n.keys())
    
    # if itemContent not in sharedbyDefs:
    #     sharedbyDefs.append(itemContent)
    # 
    # if "comments" in n :
    #     if len(n["comments"]) > 0 :
    #         TotalSharedByComments += len(n["comments"])
    #         if len(n["comments"]) > mostComments:
    #             mostComments = len(n["comments"])
    # if "annotations" in n :
    #     if len(n["annotations"]) > 0 :
    #         TotalSharedByAnnot += len(n["annotations"])
    #         if len(n["annotations"]) > mostAnnots:
    #             mostAnnots = len(n["annotations"])
# 
# print "sharedby : " + str(len(sharedby["items"])) + " : TotalComments : " + str(TotalSharedByComments) + " : TotalAnnotations : " + str(TotalSharedByAnnot)
# 
# print "\n items: " + str(itemCount)
# print "\n pages: " + str(pageCount)
# print "\n mostComments : " + str(mostComments) 
# print "\n mostAnnotations : " + str(mostAnnots) 
# 
#     #            mostCommented = render_item(n)
#                 
# completeOutput = sharedByOutput.render_unicode().encode('utf-8')
completeOutput = sharedByOutput.encode('utf-8')

filename = 'SharedByLimited.html'
f = codecs.open(filename, 'w' 'utf-8')
f.write(completeOutput)
f.close()

import os

print 'wrote out file : ' + os.getcwd() + "/" + filename

#   "[u'origin', u'updated', u'via', u'isReadStateLocked', u'author', u'alternate', u'timestampUsec', u'comments', u'id', u'crawlTimeMsec', u'published', u'title', u'annotations', u'categories']",    
#  "[u'origin', u'updated', u'via', u'isReadStateLocked', u'author', u'replies', u'alternate', u'timestampUsec', u'comments', u'id', u'content', u'crawlTimeMsec', u'published', u'annotations', u'categories']",

# print "--------------------"
# pp.pprint(sharedbyDefs)
# print "--------------------"
# pp.pprint(itemDefs)


