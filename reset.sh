#!/bin/bash

# this script will reset the file called all.json to remove the auth
# and url that we use for our internal instance.

# To use:
# - Highlight all the connections were using for sentinel in connect, export all of them into a file and download it locally
# - move the file into this folder and call it "all.json"
# execute this bash script.

python3 ./connect_import_rewriter.py -f all.json.tmpl -c changeme_workspaceid -s changeme_primarykey
mv all.json all.json.tmpl
