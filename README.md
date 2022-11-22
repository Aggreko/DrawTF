[![PyPI Version](https://img.shields.io/pypi/v/drawtf.svg)](https://pypi.python.org/project/drawtf) ![Latest Build](https://github.com/aggreko/drawtf/actions/workflows/main.yml/badge.svg)

# drawtf
Draw diagrams which include Cloud resources using TF state files or without them. Inspired by the [Diagrams](https://github.com/mingrammer/diagrams) package and a burning desire to not have to manually keep architecture diagrams updated, this was born.

## Prerequisites
* Install Python
* Install [Graphviz](https://graphviz.org/)
  
## Install
```console
foo@bar:~$ python -m pip install --upgrade pip
foo@bar:~$ pip install drawtf
foo@bar:~$ drawtf --help

Usage: drawtf [OPTIONS]

  Top level command for drawtf.

Options:
  --help  Show this message and exit.

Commands:
  draw   Draw a single design from config and settings.
  watch  Watch a directory for changes to draw.

foo@bar:~$ drawtf draw --help

Usage: drawtf draw [OPTIONS]

  Draw a single design from config and settings.

Options:
  --name TEXT              The diagram name.
  --state TEXT             The tfstate file to run against.
  --platform TEXT          The platform to use 'azure' or 'aws', only 'azure'
                           currently supported

  --output-path TEXT       Output path if to debug generated json populated.
  --json-config-path TEXT  Config file path if populated.
  --verbose                Add verbose logs.
  --help                   Show this message and exit.

foo@bar:~$ drawtf watch --help

Usage: drawtf watch [OPTIONS]

  Watch a directory for changes to draw.

Options:
  --directory TEXT  Directory to watch for changes in.
  --help            Show this message and exit.
```

## Draw
There are a few ways we can create diagrams here, all options on the CLI are optional, and it is basically just the order which you create them that draws a diagram.

### Sample config File (app.json)
If we use a config file with the fields below, this will set the name for the designs title, import a state file, and add some custom components not in the state file, The final section at the bottom draws the lines between the resources.

```json 
{
    "name": "Aggreko Application (All Resources)",
    "state": "./test/app.tfstate",
    "components": [
        {
            "name": "Aggreko",
            "type": "draw_custom",
            "resource_group_name": "",
            "attributes":{},
            "components": [
                {
                    "name": "InternalDB",
                    "type": "draw_custom",
                    "resource_group_name": "",
                    "custom": "diagrams.azure.database.DatabaseForMysqlServers",
                    "attributes": {}
                },
                {
                    "name": "App",
                    "type": "draw_custom",
                    "resource_group_name": "",
                    "custom": "diagrams.onprem.compute.Server",
                    "attributes": {}
                },
                {
                    "name": "AnotherApp",
                    "type": "draw_custom",
                    "resource_group_name": "",
                    "custom": "diagrams.onprem.compute.Server",
                    "attributes": {}
                }
            ]
        }
    ],
	"links": [
        {
            "from": "App-draw_custom",
            "to": "InternalDB-draw_custom",
            "color": "darkgreen",
            "label": "Write",
            "type": "dotted"
        },
        {
            "from": "AnotherApp-draw_custom",
            "to": "InternalDB-draw_custom",
            "color": "darkgreen",
            "label": "Write",
            "type": "dotted"
        }
    ],
    "excludes": []
}                                            
```

```console 
foo@bar:~$ drawtf draw --json-config-path ./test/app.json    
``` 
![Example](https://github.com/aggreko/drawtf/blob/main/test/app.png?raw=true)

By running the command above pointing to the config file, this will set the name and grab other resources from the state file linked. Outputs from will create the design in the same sub-folder with the name **app.png**.

### Override config File (app-subset.json)

Providing an override config alongside our main config file with the fields below, this will override the initial the designs title but still use the same state file and components from the original and attempt to join the links if all of the resources are available. You will notice an excludes section, if the keys for each resource added are in this list, then it will exclude those items.

```json
{
    "name": "Aggreko Application (Subset)",
    "base": ".//test//app.json",
    "excludes": [ 
        "AnotherApp-draw_custom"
    ]
}  
```

```console 
foo@bar:~$ drawtf draw --json-config-path ./test/app-subset.json
```
![Example](https://github.com/aggreko/drawtf/blob/main/test/app-subset.png?raw=true)

By running the command above pointing to the config file and override files, this will set the name from the override and grab other resources from the state file linked. Outputs from will create the design in the same sub-folder with the name **app-subset.png**.

### Override config File and CLI overrides

```console 
foo@bar:~$ drawtf draw --json-config-path ./test/app-subset.json --name "Aggreko Application (Sample)" --state ./test/app.tfstate --output-path ./test/sample --verbose                                                                           
```
![Example](https://github.com/aggreko/drawtf/blob/main/test/sample.png?raw=true)

The command above, though using the same config files, can override all for the name, state file path and output path. Outputs from will create the design in the directory **test** with the name **sample.png**.

## Watch

It is now possible to simply watch a folder for *.json files to change or be created, this will then pick up the changes and draw designs as required.

```console
foo@bar:~$ drawtf watch --directory ./test   

Starting watch for *.json files...
Watching in .//test...
Modified file .//test\app.json, drawing...
Adding resource APPLICATION_DEV-azurerm_resource_group
Adding resource storageaccount-azurerm_storage_account
Adding resource (from config) InternalDB-draw_custom
Adding resource (from config) App-draw_custom
Adding resource (from config) AnotherApp-draw_custom
Adding resource (from config) Aggreko-draw_custom
.//test\app.json done.
Modified file .//test\app-subset.json, drawing...
Adding resource APPLICATION_DEV-azurerm_resource_group
Adding resource storageaccount-azurerm_storage_account
Adding resource (from config) InternalDB-draw_custom
Adding resource (from config) App-draw_custom
Excluding resource (from config) AnotherApp-draw_custom
Adding resource (from config) Aggreko-draw_custom
WARNING:root:Ignoring link as object not in component cache: {'from': 'AnotherApp-draw_custom', 'to': 'InternalDB-draw_custom', 'color': 'firebrick', 'label': 'Write', 'type': 'dotted'}
.//test\app-subset.json done.
```

## CI/CD Steps

Yes you can run this via GitHub actions or devops pipelines.

### GitHub Actions

```yaml
      - name: Setup Graphviz
        uses: ts-graphviz/setup-graphviz@v1
      - name: Set up Python 3.7
        uses: actions/setup-python@v4
        with:
          python-version: '3.7'
      - name: Generate Diagram
        run: |
          python -m pip install --upgrade pip
          pip install drawtf
          drawtf --help
          drawtf draw --json-config-path "./test/app.json"
```

### Azure Devops

```yaml
      - script: sudo apt-get -yq install graphviz
        displayName: Setup Graphviz
      - script: |
          python -m pip install --upgrade pip
          pip install drawtf
          drawtf --help
          drawtf draw --json-config-path "./test/app.json"
        displayName: Generate Diagram
```

## Early days

Just an FYI, its early days here and is still a development style project. That said we are using for all of our projects internally using TF, but loads of resources types are still to be added.