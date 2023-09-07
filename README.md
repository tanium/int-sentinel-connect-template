# int-sentinel-connect-template

This is deprecated and should not be used. Please reach out to your Tanium representative for further help.

## Older instructions

The Tanium and Microsoft Sentinel integration has a few connections that are required. This repo stores a template file of Tanium Connect connections, and a python script that can parse the template. Since each connection requires a Workspace ID, and a Primary Key to send data into Microsoft Sentinel, the python script will inject the workspace ID and primary key into the template, and create a new file called "all.json". This new file can be imported into Tanium Connect to quickly and easily create the required connections.

Proper usage should look like this:

```
python3 ./connect_import_rewriter.py -c <WORKSPACE_ID> -s <PRIMARY_KEY> -f all.json.tmpl
```