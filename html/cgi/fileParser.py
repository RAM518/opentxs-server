#!/usr/bin/env python

# this parses files of various types, decrypts and decodes xml content
# by calling the opentxs client "opentxs decode" function, then serves up the
# content in an nested xml class with custom style-sheet
# the stylesheet definitions for the xml classes are in dir_menu.css

import os
import fnmatch
import sys
import subprocess
import cgi
import json
import time
import re
from subprocess import Popen, PIPE
import xml.etree.ElementTree as ET
import codecs
from xml.etree.ElementTree import XMLParser
import cgitb
cgitb.enable()
parser = XMLParser(encoding="utf-8")

# Path to Opentxs client 
#pathToOpentxs = "/usr/bin/"      #DEFAULT
pathToOpentxs = "/home/locutus/installs/opentxs_bailment/build/bin/";  #CUSTOM


def decodeThis(thisMemo,string):  # decodes files, xml strings, keys
  if string>0:
    cmd = "echo -e \"" + thisMemo + "\" | " + pathToOpentxs + "opentxs decode"
  else:
    cmd = "cat " + thisMemo + " | " + pathToOpentxs + "opentxs decode"
  p = Popen(cmd , shell=True, stdout=PIPE, stderr=PIPE)
  out, err = p.communicate()
  fileContents = out.rstrip()
  if string == 0 or string == 1:   #for files or xml
    if re.search(r'xml\sversion=\"1',fileContents,re.M|re.I):
      fileContents = fileContents.split('<?xml version="1.0"?>')
    elif re.search(r'xml\sversion=\"2',fileContents,re.M|re.I):
      fileContents = fileContents.split('<?xml version="2.0"?>')
    else:
      fileContents = fileContents.split('SAMY')
    fileContents = fileContents[1].split('-----BEGIN') # stop at bottom sig header
    fileXML = fileContents[0]; # holds xml content of (filetype)
  elif string == 2:
    fileXML = fileContents; # just display the entire pgp key, no parsing
  return fileXML

def displayXML(root):
  # iterate the decoded xml file, reprint it with display form / css style   
  for node in root.iter():
    print '<table class="decoded"><tr><td>'
    print "<li class='top' value='"+node.tag+"'>"
    print '<center><b><font style="color:#A4F1A6;">'+node.tag+'</font></b></center>'
    if ( node.tag == 'inReferenceTo' or node.tag == 'publicCredential' ) :
      if node.text: 
        subText = decodeThis(node.text,1) # 1 here is for decoding encoded xml
        subText1 = re.sub(r'@','at',subText); 
          # this sanitizes the @ symbol out of the xml class headers
        subRoot = ET.fromstring(subText1)
        displayXML(subRoot)
      else:
        print "inReferenceTo data was empty!<br />"
    elif ( node.tag == 'item' or node.tag == 'attachment' or 
       node.tag == 'credentialList' or node.tag == 'masterPublic' or
       node.tag == 'masterSigned' or node.tag == 'accountLedger' or
       node.tag == 'responseLedger' or node.tag == 'transaction' ): 
      if node.text: 
        if len(node.attrib.items()):
          print node.text          
        else:
          subText = decodeThis(node.text,1) # 1 here is for decoding xml strings
          subText1 = re.sub(r'@','at',subText); 
             # this sanitizes the @ symbol out of the xml class headers
          subRoot = ET.fromstring(subText1)
          displayXML(subRoot)
      else:
        print "inReferenceTo data was empty!<br />"
    elif node.tag == 'nymIDSource':
      if node.text: 
        if len(node.attrib.items()):
          print node.text          
        else:
          subText = decodeThis(node.text,2) # 2 here is for decoding pgp pubkeys
          print subText     
      else:
        print "inReferenceTo data was empty!<br />"
    elif ( node.tag == 'publicInfo' or node.tag == 'privateInfo' or
           node.tag == 'mintPublicInfo' or node.tag == 'note' or 
           node.tag == 'transactionNums' or node.tag == 'issuedNums' or
           node.tag == 'ackReplies' ) :
      # special case for publicInfo and privateInfo xml objects with raw data
      if node.text: 
        subText = decodeThis(node.text,2) # 2 here is for decoding pgp pubkeys
        print subText     
      else:
        print "inReferenceTo data was empty!<br />"
    elif node.tag == 'publicContents' or node.tag == 'privateContents':
      # special case for publicContents / privateContents xml objects
      continue
    elif ( node.tag == 'credentials' or node.tag == 'mintPublicKey' or
           node.tag == 'mintPrivateInfo' or 'tokenID' ):
      # special case fields that don't get decoded
      if node.text: 
        print node.text
    for name, value in sorted(node.attrib.items()):
      print ' <lu class="itemName" value="'+name+'">'
      print ' &nbsp;&nbsp;&nbsp;&nbsp;<b><u>'+name+'</u></b><br />'
      print '   <div class="itemValue">'
      print '      <center><font style="color:#E2E3E8;">'+value+'</font>',
      # here we split cases based on the xml name property of each tag
      if name == 'dateSigned':
        print '<br /><b><font style="color:#E2FBE3;">',
        print time.strftime("%Y-%b-%d %H:%M:%S",time.gmtime(float(value)))
        print '</font></b>'
      if name == 'date':
        print '<br /><b><font style="color:#E2FBE3;">',
        print time.strftime("%Y-%b-%d %H:%M:%S",time.gmtime(float(value)))
        print '</font></b>'
      elif name == 'serverID':
        print '<br /><b><font style="color:#E2FBE3;">',
        fileTarget = fileRoot + "contracts/" + value        
        serverXML = decodeThis(fileTarget,0)
        rootXML = ET.fromstring(serverXML)
        for node in rootXML.iter('entity'):         
          for name, value in sorted(node.attrib.items()):
            if name == 'shortname':
              print value + "<br />" 
        print '</font></b>'
      print '</center>'
      print '   </div>'
      print ' </lu>'
    print "</li><br />"
    print "</td><tr></table>" 



print "Content-Type: text/html"
print ""
fs = cgi.FieldStorage()

d = {}
for k in fs.keys():
    d[k] = fs.getvalue(k)
try: 
  fileTarget = d["target"]
except:
    #print "Unexpected error:", sys.exc_info()[0]
    print ""
    #raise
try: 
  fileType = d["type"]
except:
    #print "Unexpected error:", sys.exc_info()[0]
    print ""
    #raise

# check the fileTarget and ensure it is a file that exists on the system
try: 
  isFile = os.path.isfile(fileTarget)
except:
  isFile = 0
  #raise


# only execute the fileTarget input if it is a VALID file path on the system!
if isFile:

  cmd = "rm ~/.ot/client_data/ot.pid"
  p = Popen(cmd , shell=True, stdout=PIPE, stderr=PIPE)
  out, err = p.communicate()

  fileXML = decodeThis(fileTarget,0); # 0 here is for decoding a file
  root = ET.fromstring(fileXML)
  fileRoot=""

  if re.search(r'client_data',fileTarget,re.M|re.I):
    fileParse = fileTarget.split("/.ot/")
    fileRoot = fileParse[0] + "/.ot/client_data/"    
  elif re.search(r'server_data',fileTarget,re.M|re.I):
    fileParse = fileTarget.split("/.ot/")
    fileRoot = fileParse[0] + "/.ot/server_data/"

  displayXML(root);
  





