#!/usr/bin/env python

import os
import fnmatch
print ""

# this sets up the directory menu tree within the dir_menus.css template

print "<table style='cellspacing:2px; cellpading:2px; width:100%'><tr><td>"
print "  <b><u>File Menu</u></b><br />"
print "  <div class='menu'>"
print "    <ul id='folder_list'>"
c = 0;
lastLevel = 0;
level = 0;
startFolder = '/home/locutus/.ot/server_data';
for root, dir, files in os.walk(startFolder, topdown=True):
  dir.sort()
  files.sort()
  #print len(root), " ", len(dir), " ", len(files)
  c += 1;
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
  print "     <span class='symbol-close' onclick='TreeMenu.toggle(this)'></span>",
  # this takes out the prepended full path of the firectory names
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
    print "      <li><span class='symbol-png'></span>"
    # this piece appends the filenames for readability       
    if len(filename)==2:
      if len(filename[0])>17:
        print "         ",filename[0][:15] + "...." + filename[1]
      else:
        print "         ",filename[0] + "." + filename[1]           
    else:
      if len(filename[0])>17:
        print "         "+filename[0][:15] + "..."
      else:
        print "         ",filename[0]
    print "      </li>"
    # another conditional needed here to close up the xml properly
    if fileEnd == len(files):
      if c == len(dir):
         print '</ul>'
  lastLevel = level;
print "  </ul>"
print "</td></tr></table>"
