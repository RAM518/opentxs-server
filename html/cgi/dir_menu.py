#!/usr/bin/env python

import os
import fnmatch
import cgi
import sys
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

thisTarget = ''
if fileTarget == 'server_data':
  thisTarget = 'server_data'
elif fileTarget == 'client_data':
  thisTarget = 'client_data'
# the above conditional prevents ajax requests for other directory readings

# this sets up the directory menu tree within the dir_menus.css template

print "<table border=1px style='cellspacing:2px; cellpadding:2px; width:100%'><tr><td>"
print "  <font style='float:left'><b><a href=\"javascript: set_leftPanel('server_data')\">server_data</a></b></font>"
print "  <font style='float:right'><b><a href=\"javascript: set_leftPanel('client_data')\">client_data</a></b></font></td></tr><tr><td>"
print "  <b><u>File Menu</u></b><br />"
print "  <div class='menu'>"
print "    <ul id='folder_list'>"
c = 0;
r = 0;
lastLevel = 0;
level = 0;

# here we need to look for the ~/.ot folder
from subprocess import Popen, PIPE
cmd = "cd ~; pwd"
p = Popen(cmd , shell=True, stdout=PIPE, stderr=PIPE)
out, err = p.communicate()
if p.returncode:
  print "Couldn't get dir listing for ~/.ot folder"
homePath = out.rstrip()

startFolder = homePath + '/.ot/' + fileTarget;
for root, dir, files in os.walk(startFolder, topdown=True):
  dir.sort()
  files.sort()
  #print len(root), " ", len(dir), " ", len(files)
  c += 1;
  r += 1;
  level = root.replace(startFolder,'').count(os.sep)
  # these three conditionals close up the xml behind the loop properly
  if lastLevel == level:
    if lastLevel > 0:
      print '    </ul>'
  if lastLevel > level:
    print '    </ul>' + '</li></ul>' * (lastLevel - level)   
    c = 1;
  if lastLevel < level:
    c = 1;
  print "  <li class='close'>",
  if r==1:
    print "     <span class='symbol-close' id=treeRoot onClick='TreeMenu.toggle(this);'></span>",
  else:
    print "     <span class='symbol-close' onclick='TreeMenu.toggle(this);'></span>",
  # this takes out the prepended full path of the directory names
  path = root.split('/')
  # this piece appends the filenames for readability
  dirname = os.path.basename(root).split('.')
  if len(dirname)==2:
    if len(dirname[0])>17:
      print dirname[0][:15] + '...' + dirname[1],
    else:
      print dirname[0] + '.' + dirname[1],
  else:
    if len(dirname[0])>17:
      print dirname[0][:15] + '...',
    else:
      print dirname[0],
  print "    <ul style='display:none;'>"
  fileEnd = 0;
  for items in files:    
    fileEnd += 1;
    filename = items.split('.')
    fullFileName = root + "/" + items;
    # this piece appends the filenames for readability       
    if len(filename)==2:
      if filename[1] == 'rct':
        print "      <li><span class='symbol-item'></span>"
      elif filename[1] == 'success':
        print "      <li><span class='symbol-item'></span>"
      elif filename[1] == 'xml':
        print "      <li><span class='symbol-html'></span>"
      elif filename[1] == 'PUBLIC':
        print "      <li><span class='symbol-key'></span>"
      elif filename[1] == 'cred':
        print "      <li><span class='symbol-key'></span>"
      elif filename[1] == 'crn':
        print "      <li><span class='symbol-clock'></span>"
      else:
        print "      <li><span class='symbol-txt'></span>"    
    # here we print out hyperlinks and set_rightPanel(path,type) constructors  
      if len(filename[0])>17:
        print "         "+"<a href='javascript:set_rightPanel(\"" + fullFileName + "\",\"" + filename[1] + "\");'>"
        print "         "+filename[0][:15] + "..." + filename[1] + "</a>"
      else:
        print "         "+"<a href='javascript:set_rightPanel(\"" + fullFileName + "\",\"" + filename[1] + "\");'>"
        print "         "+filename[0] + "." + filename[1] + "</a>"          
    else:
      print "      <li><span class='symbol-txt'></span>"
      if len(filename[0])>17:
        print "         "+"<a href='javascript:set_rightPanel(\"" + fullFileName + "\",\"none\");'>"
        print "         "+filename[0][:15] + "..." + "</a>"
      else:
        print "         "+"<a href='javascript:set_rightPanel(\"" + fullFileName + "\",\"none\");'>"
        print "         "+filename[0] + "</a>"
    print "      </li>"
    # another conditional needed here to close up the xml properly
    if fileEnd == len(files):
      if c == len(dir):
         print '</ul>'
  lastLevel = level;
print "  </ul></div>"
print "</td></tr></table>"
