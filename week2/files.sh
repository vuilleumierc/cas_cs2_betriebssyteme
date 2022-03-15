#!/bin/bash
rm -r diff.txt
cat /var/lib/dpkg/info/*.{list,conffiles} | sort | uniq > pkg_files.txt
find / -type f | sort > all_files.txt
diff pkg_files.txt all_files.txt | grep ">" | awk {'print($2)'} > diff.txt