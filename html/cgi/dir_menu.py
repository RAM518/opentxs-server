#!/usr/bin/env python

import os
import fnmatch
print ""

# this sets up the directory menu tree using the css template

print "<table style='cellspacing:2px; cellpading:2px; width:100%'><tr><td>"
print "      <b><u>File Menu</u></b><br />"
print "      <ol id='menutree' style='display: inline;'>",

c = 0;
for root, dir, files in os.walk("/home/locutus/.ot/server_data"):
  c += 1;
  print "<li><label class='menu_label' style='z-index:-1;' for='c%i'>" % c,
  path = root.split('/')
  dirname = os.path.basename(root).split('.')
  if len(dirname)==2:
     if len(dirname[0])>15:
        print (len(path) - 5) *'&nbsp;&nbsp;' + "-" + dirname[0][:15] + '...' + dirname[1],
     else:
        print (len(path) - 5) *'&nbsp;&nbsp;' + "-" + dirname[0] + '.' + dirname[1],
  else:
     if len(dirname[0])>15:
        print (len(path) - 5) *'&nbsp;&nbsp;' + "-" + dirname[0][:15] + '...',
     else:
        print (len(path) - 5) *'&nbsp;&nbsp;' + "-" + dirname[0],
  print "</label><input type='checkbox' id='c%i'" % c,
  print " onClick='javascript:resetHeight()'/>"
  print "<ol>",
  for items in fnmatch.filter(files, "*"):
     filename = items.split('.')
     print "  <li class='page'><a href='javascript:resetHeight()'>",
     if len(filename)==2:
        if len(filename[0])>15:
           print " ",filename[0][:15] + "...." + filename[1],
        else:
           print " ",filename[0] + "." + filename[1],           
     else:
        if len(filename[0])>15:
          print " "+filename[0][:15] + "...",
        else:
          print " ",filename[0],
     print "</a></li>"
  print "</ol></li>"

print "</ol>",
print "</td></tr></table>"
