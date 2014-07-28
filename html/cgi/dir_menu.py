#!/usr/bin/env python

import os
import fnmatch
print ""

# this sets up the directory menu tree using the css template

print "<table style='cellspacing:2px; cellpading:2px; width:100%'><tr><td>"
print "   <font style='text-align: center; align:center;'>"
print "     <b><u>File Menu</u></b></font></td></tr><tr><td align=left>"
print "      <ol id='menutree'>"

c = 0;
for root, dir, files in os.walk("/home/locutus/.ot/server_data"):
        c += 1;
        print "       <li><label class='menu_label' for='c%i'>" % c         
        print "          " + root
        print "       </label><input type='checkbox' id='c%i'onClick='javascript:resetHeight()'/>\n" % c
        print "       <ol>"
        for items in fnmatch.filter(files, "*"):
                print "           <li class='page'><a href='javascript:resetHeight()'>"

                print "           " + items + "</a></li>\n"
        print "       </ol></li>"

print "</ol>"
print "</td></tr></table>"
