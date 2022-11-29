"""Console script for drawtf."""
import sys
import click
import json
import os
from typing import Dict, List
import logging

from app.azure import azure
from app.common.component import Component
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from azure.mgmt.storage import StorageManagementClient

UNPARENTED = "Unparented"

def commonDraw(name, state, platform, output_path, json_config_path, verbose):
    """Console script for drawtf."""
    # Set logging level
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        
    # Load the config if it exists
    config_data = {}
    if (not json_config_path is None):
        logging.info(f"Reading config from {json_config_path}.")
        
        if (not os.path.exists(json_config_path)):
            raise click.BadParameter(
                message="The path to the config file does not exist.")
      
        try:
            cf = open(json_config_path)
            config_data = json.load(cf)
        except ValueError:
            click.secho(f"Error while reading config for {json_config_path}", fg='red')
            return 1
            
    if ("base" in config_data):
        base_path = config_data['base']
        logging.info(f"Reading base config from {base_path}.")
        
        if (not os.path.exists(base_path)):
            raise click.BadParameter(
                message="The path to the base configuration file does not exist.")
        
        # read base config and apply this config on top of it
        
        try:
            cfo = open(base_path)
            config_data_override = json.load(cfo)
        except ValueError:
            click.secho(f"Error while reading config for BASE {base_path}", fg='red')
            return 1
        
        
        config_data_override.update(config_data)
        config_data = config_data_override
        
    # Take name from cli if not in config, default to 'design'
    if (name == None and "name" in config_data):
        name = config_data["name"]
        
    if (name == None):
        name = "design"
        
    # Take name from cli if not in config, default to '[]' if nothing found
    if (state == None and "state" in config_data):
        state = config_data["state"]
    
    data = {
        "resources": []
    }
    
    if (not state == None and not os.path.exists(state)):
        click.secho("The path to the state file does not exist.", fg='red')
        if ("storage-azure" in config_data):
            storage_config = config_data["storage-azure"]
            remote_state = str(state).strip("./")
            click.secho(f"Checking if file '{remote_state}' exists on storage container '{storage_config['account']}/{storage_config['container']}'.", fg='yellow')
            default_credential = DefaultAzureCredential()
            storage_client = StorageManagementClient(default_credential, storage_config['subscription-id'])
            storage_keys = storage_client.storage_accounts.list_keys(storage_config['resource-group'], storage_config['account'])
            storage_keys = {v.key_name: v.value for v in storage_keys.keys}  # type: ignore
            connection = f"DefaultEndpointsProtocol=https;AccountName={storage_config['account']};AccountKey={storage_keys['key1']};EndpointSuffix=core.windows.net"
            blob_service_client = BlobServiceClient.from_connection_string(connection)
            container_client = blob_service_client.get_container_client(storage_config['container'])
            blob_client = container_client.get_blob_client(remote_state)
            
            if blob_client.exists():
                click.secho(f"Found state file '{remote_state}' on container '{storage_config['account']}/{storage_config['container']}'.", fg='green')
                blob_data = blob_client.download_blob()
                data_bytes = blob_data.readall()
                data = json.loads(data_bytes.decode('utf-8'))
            else:
                click.secho(f"Blob '{remote_state}' doesn't exist on '{storage_config['account']}/{storage_config['container']}'.", fg='red')
        else:
            click.secho("No storage container or store connection string defined.", fg='red')
    else:
        if (not state == None):
            f = open(state)
            data = json.load(f)
    
    # Take platform from cli if not in config, or default to 'azure'
    if ("platform" in config_data):
        platform = config_data["platform"]
        
    if (platform == None):
        platform = "azure"
        
    # Take output from cli if not in config
    if (output_path == None and "outputPath" in config_data):
        output_path = config_data["outputPath"]
        
    if (output_path == None and not json_config_path == None):
        output_path = os.path.splitext(json_config_path)[0]
        
    # Take excludes if exists
    excludes = []
    if ("excludes" in config_data):
        excludes = config_data["excludes"]
    
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
            click.echo(f"Resource type {type} is not supported.")
            continue

        for instance in resource["instances"]:
            attributes = instance["attributes"]
            if (not "resource_group_name" in attributes):
                resource_group_name = UNPARENTED
            else:
                resource_group_name = attributes["resource_group_name"]

            if ("name" in attributes):
                resource_name = attributes["name"]

            component = Component(resource_name, type,
                              mode, resource_group_name, attributes);
            
            if (not component.key in excludes):
                click.echo(f"Adding resource {component.key}")
                components.append(component)
            else:
                click.echo(f"Excluding resource {component.key}")

    links = None
    if "links" in config_data:
        links = config_data["links"]
    if "components" in config_data:
        custom_components = __get_custom_components(excludes, supported_nodes, config_data)
        components = components + custom_components
            
    if (platform.lower() == 'azure'): 
        azure.draw(name, output_path, components, links)
    else:
        raise Exception(f"Platform {platform} is not yet supported.")

    return 0

def __get_custom_components(excludes, supported_nodes, config_data: Dict) -> List[Component]:
    new_components = []
    
    if not "components" in config_data:
        return new_components
    
    config_components = config_data["components"]  
    
    for instance in config_components:
        resource_name = instance["name"]
        type = instance["type"]
        
        if (not type in supported_nodes):
            click.echo(f"Resource type {type} is not supported.")
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
            child_config_components = __get_custom_components(excludes, supported_nodes, instance)
        
        component = Component(resource_name, type, mode, resource_group_name, attributes, child_config_components, custom)
        
        if (not component.key in excludes):
            click.echo(f"Adding resource (from config) {component.key}")
            new_components.append(component)
        else:
            click.echo(f"Excluding resource (from config) {component.key}")
            
    return new_components
