import sys
import json
import pprint

pp = pprint.PrettyPrinter(indent=2)

txt = open('/Users/doug.churchman/Documents/src/data/followers.json')
followers = json.loads(txt.read())

txt = open('/Users/doug.churchman/Documents/src/data/following.json')
following = json.loads(txt.read())

txt = open('/Users/doug.churchman/Documents/src/data/liked.json')
liked = json.loads(txt.read())

txt = open('/Users/doug.churchman/Documents/src/data/notes.json')
notes = json.loads(txt.read())

txt = open('/Users/doug.churchman/Documents/src/data/shared-by-followers.json')
sharedby = json.loads(txt.read())

txt = open('/Users/doug.churchman/Documents/src/data/shared.json')
shared = json.loads(txt.read())

txt = open('/Users/doug.churchman/Documents/src/data/starred.json')
starred = json.loads(txt.read())

TotalSharedComments = 0
TotalSharedByComments = 0
TotalSharedAnnot = 0
TotalSharedByAnnot = 0

shared.keys()
print "Doug's data "
print "followers : " + str(len(followers["friends"]))
print "following : " + str(len(following["friends"]))
print "liked : " + str(len(liked["items"]))
print "notes : " + str(len(notes["items"]))
print "starred : " + str(len(starred["items"]))

for n in shared["items"]:
    # print n["content"]["content"]
    if "comments" in n :
        if len(n["comments"]) > 0 :
            TotalSharedComments += len(n["comments"])
    if "annotations" in n :
        if len(n["annotations"]) > 0 :
            TotalSharedAnnot += len(n["annotations"])
            # for m in n["comments"] :
                # print m["author"] + " : " + m["htmlContent"] + "\n"

for n in sharedby["items"]:
    # print n["content"]["content"]
    if "comments" in n :
        if len(n["comments"]) > 0 :
            TotalSharedByComments += len(n["comments"])                
    if "annotations" in n :
        if len(n["annotations"]) > 0 :
            TotalSharedByAnnot += len(n["annotations"])                

print "sharedby : " + str(len(sharedby["items"])) + " : TotalComments : " + str(TotalSharedByComments) + " : TotalAnnotations : " + str(TotalSharedByAnnot)
               
print "shared : " + str(len(shared["items"])) + " : TotalComments : " + str(TotalSharedComments) + " : TotalAnnotations : " + str(TotalSharedAnnot)


txt = open('/Users/doug.churchman/Documents/src/data/allisonrae/followers.json')
followers = json.loads(txt.read())

txt = open('/Users/doug.churchman/Documents/src/data/allisonrae/following.json')
following = json.loads(txt.read())

txt = open('/Users/doug.churchman/Documents/src/data/allisonrae/liked.json')
liked = json.loads(txt.read())

txt = open('/Users/doug.churchman/Documents/src/data/allisonrae/shared-by-followers.json')
sharedby = json.loads(txt.read())

txt = open('/Users/doug.churchman/Documents/src/data/allisonrae/shared.json')
shared = json.loads(txt.read())

txt = open('/Users/doug.churchman/Documents/src/data/allisonrae/starred.json')
starred = json.loads(txt.read())

TotalSharedComments = 0
TotalSharedByComments = 0
TotalSharedAnnot = 0
TotalSharedByAnnot = 0

print "\n"
print "Allison's data "
print "followers : " + str(len(followers["friends"]))
print "following : " + str(len(following["friends"]))
print "liked : " + str(len(liked["items"]))
print "starred : " + str(len(starred["items"]))

for n in shared["items"]:
    # print n["content"]["content"]
    if "comments" in n :
        if len(n["comments"]) > 0 :
            TotalSharedComments += len(n["comments"])
    if "annotations" in n :
        if len(n["annotations"]) > 0 :
            TotalSharedAnnot += len(n["annotations"])
            # for m in n["comments"] :
                # print m["author"] + " : " + m["htmlContent"] + "\n"

for n in sharedby["items"]:
    # print n["content"]["content"]
    if "comments" in n :
        if len(n["comments"]) > 0 :
            TotalSharedByComments += len(n["comments"])                
    if "annotations" in n :
        if len(n["annotations"]) > 0 :
            TotalSharedByAnnot += len(n["annotations"])                

print "sharedby : " + str(len(sharedby["items"])) + " : TotalComments : " + str(TotalSharedByComments) + " : TotalAnnotations : " + str(TotalSharedByAnnot)
               
print "shared : " + str(len(shared["items"])) + " : TotalComments : " + str(TotalSharedComments) + " : TotalAnnotations : " + str(TotalSharedAnnot)


# from time import gmtime, strftime
# strftime("%Y %b %d - %I:%M %p", gmtime(1311691796))
#  '2011 Jul 26 - 02:49 PM'               
               
#   for n in data["friends"]:
#     print("##" + n["displayName"])
#     if "location" in n : 
#         print("### hometown: " + n["location"])
#     if "websites" in n :
#         for m in n["websites"]:
#             if "title" in m :
#                 print("[ " + m["url"] + " : " + m["title"] +"](" + m["url"] + ")\n")

'''
  "friends" : [ {
    "userIds" : [ "03310580441156450829" ],
    "profileIds" : [ "112420739249290976418" ],
    "contactId" : "6230409899125640545",
    "photoUrl" : "/s2/photos/public/AIbEiAIAAABECKK59o2hkdWvrAEiC3ZjYXJkX3Bob3RvKigzM2I4N2I4NTdlMTQzOWQ1Mzk2NDFlZGM1MjE2ZmU2ZTFiYzFlMmM4MAGPkBnqnr8Y2npv1lelVYoz1yyDEQ",
    "location" : "Louisville, KY",
    "stream" : "user/03310580441156450829/state/com.google/broadcast",
    "flags" : 544,
    "types" : [ 0, 1, 3, 6, 7 ],
    "displayName" : "Gary Quick",
    "givenName" : "Gary",
    "n" : "",
    "p" : "",
    "groupId" : [ "18", "13", "2" ],
    "websites" : [ {
      "title" : "garyquick.com",
      "url" : "http://www.garyquick.com/"
    }, {
      "title" : "Picasa Web Albums",
      "url" : "http://picasaweb.google.com/mrquick"
    }, {
      "title" : "Shared on Google Reader",
      "url" : "http://www.google.com/reader/shared/03310580441156450829"
    }, {
      "title" : "YouTube - mrquicknet",
      "url" : "http://youtube.com/user/mrquicknet"
    }, {
      "title" : "On Louisville Photo Collective",
      "url" : "http://www.louisvillephoto.org/profile/GaryQuick"
    }, {
      "title" : "Gary Quick Photography Facebook Page",
      "url" : "http://www.facebook.com/pages/Louisville-KY/Gary-Quick-Photography/75206431774"
    }, {
      "title" : "On Art Sanctuary",
      "url" : "http://www.art-sanctuary.org/artists/Gary.Quick.php"
    }, {
      "title" : "Gary Q.",
      "url" : "http://www.yelp.com/user_details?userid=PS4PN_IrpN-4KX39hLpjwQ"
    }, {
      "title" : "My Flickr Photostream",
      "url" : "http://www.flickr.com/photos/mrquicknet/"
    }, {
      "title" : "Gary Quick",
      "url" : "http://www.youtube.com/user/mrquicknet"
    }, {
      "title" : "Buzz",
      "url" : "https://profiles.google.com/112420739249290976418/buzz"
    }, {
      "title" : "Gary Quick Facebook",
      "url" : "http://www.facebook.com/people/Gary-Quick/500629876"
    }, {
      "title" : "Gary Quick Photography",
      "url" : "http://photo.garyquick.com"
    }, {
      "title" : "On Twitter",
      "url" : "http://twitter.com/mrquick"
    } ]
''' 
