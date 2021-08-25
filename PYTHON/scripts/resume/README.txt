Steps:
1. python sort_bibliography.py > oruanaidh_sorted.bib
2. cat oruanaidh_sorted.bib | perl -ne 'print "\\nocite{$1}\n" if /^\@\S+\{(\S+)\,/;' | pbcopy
3. Paste the text into the resume
