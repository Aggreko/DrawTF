"""Console script for drawtf."""
import sys
import click
import json
import os
from typing import Dict, List
import logging

from draw.azure import azure
from draw.common.component import Component
from draw.common.resources.draw_custom import DrawCustom

UNPARENTED = "Unparented"

@click.command()
@click.option('--name', help='The diagram name.')
@click.option('--state', help='The tfstate file to run against.')
@click.option('--platform', help="The platform to use 'azure' or 'aws', only 'azure' currently supported",  default='azure')
@click.option('--output-path', help='Output path if to debug generated json populated.')
@click.option('--json-config-path', help='Config file path if populated.')
@click.option('--verbose', is_flag=True, default=False, help='Add verbose logs.')
def main(name: str, state: str, platform: str, output_path: str, json_config_path: str, verbose: bool):
    """Console script for drawtf."""
    # Set logging level
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        
    # Load the config if it exists
    config_data = None
    if (not json_config_path is None):
        logging.info(f"Reading config from {json_config_path}.")
        
        if (not os.path.exists(json_config_path)):
            raise click.BadParameter(
                message="The path to the config file does not exist.")
            
        cf = open(json_config_path)
        config_data = json.load(cf)

    # Get the state file passed in or in config and set it up
    if (not config_data == None and "state" in config_data and state == None):
        state = config_data["state"]
        
    if (not state == None and not os.path.exists(state)):
        raise click.BadParameter(
            message="The path to the state file does not exist.")

    if (not state == None):
        f = open(state)
        data = json.load(f)
    else:
        data = {
            "resources": []
        }
        
    # Validate name and output path too
    if (not config_data == None and name == None and "name" in config_data):
        name = config_data["name"]
        
    if (name == None):
        name = "Design"
        
    if (not config_data == None and output_path == None and "outputPath" in config_data):
        output_path = config_data["outputPath"]
        
    if (output_path == None and not json_config_path == None):
        output_path = os.path.splitext(json_config_path)[0]

    supported_nodes = []
    if (platform.lower() == 'azure'):
        supported_nodes = azure.supported_nodes()
    else:
        raise Exception(f"Platform {platform} is not yet supported.")
    
    components: List[Component] = []

    for resource in data["resources"]:
        resource_name = resource["name"]
        type = resource["type"]
        mode = "manual"
        if ("mode" in resource):
            mode = resource["mode"]

        if (not type in supported_nodes):
            print(f"Resource type {type} is not supported.")
            continue

        for instance in resource["instances"]:
            attributes = instance["attributes"]
            if (not "resource_group_name" in attributes):
                resource_group_name = UNPARENTED
            else:
                resource_group_name = attributes["resource_group_name"]

            if ("name" in attributes):
                resource_name = attributes["name"]

            print(f"Adding resource {resource_name}-{type}")
            components.append(Component(resource_name, type,
                              mode, resource_group_name, attributes))

    links = None
    if (not config_data is None):
        if "links" in config_data:
            links = config_data["links"]
        if "components" in config_data:
            custom_components = get_custom_components(supported_nodes, config_data)
            components = components + custom_components
            
    if (platform.lower() == 'azure'): 
        azure.draw(name, output_path, components, links)
    else:
        raise Exception(f"Platform {platform} is not yet supported.")

    return 0

def get_custom_components(supported_nodes, config_data: Dict) -> List[Component]:
    new_components = []
    
    if not "components" in config_data:
        return new_components
    
    config_components = config_data["components"]  
    
    for instance in config_components:
        resource_name = instance["name"]
        type = instance["type"]
        
        if (not type in supported_nodes):
            print(f"Resource type {type} is not supported.")
            continue
        
        mode = "manual"
        if ("mode" in instance):
            mode = instance["mode"]
            
        custom = None
        if ("custom" in instance):
            custom = instance["custom"]
            
        resource_group_name = instance["resource_group_name"]
        attributes = instance["attributes"]
        
        child_config_components = []
        if ("components" in instance):
            child_config_components = get_custom_components(supported_nodes, instance)
            
        print(f"Adding resource (from config) {resource_name}-{type}")
        new_components.append(Component(resource_name, type, mode, resource_group_name, attributes, child_config_components, custom))
            
    return new_components
    
if __name__ == "__main__":
    sys.exit(main())  # type: ignore # pragma: no cover
