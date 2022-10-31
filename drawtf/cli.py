"""Console script for drawtf."""
import sys
import click
import json
import os
from typing import List
import logging

from draw.azure import azure
from draw.common.component import Component

UNPARENTED = "Unparented"


@click.command()
@click.option('--name', help='The diagram name.', required=True)
@click.option('--state', help='The tfstate file to run against.', required=True)
@click.option('--platform', help="The platform to use 'azure' or 'aws', only 'azure' currently supported",  default='azure')
@click.option('--output-path', help='Output path if to debug generated json populated.')
@click.option('--json-config-path', help='Config file path if populated.')
@click.option('--json-output-path', help='Output path if to debug generated json populated.')
@click.option('--verbose', is_flag=True, default=False, help='Add verbose logs.')
def main(name: str, state: str, platform: str, output_path: str, json_config_path: str, json_output_path: str, verbose: bool):
    """Console script for drawtf."""
    if (not os.path.exists(state)):
        raise click.BadParameter(
            message="The path to the state file does not exist.")

    if (not json_config_path == None and not os.path.exists(json_config_path)):
        raise click.BadParameter(
            message="The path to the config file does not exist.")

    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    f = open(state)
    data = json.load(f)

    components: List[Component] = []
    resources = {}

    supported_nodes = []
    if (platform == 'azure'):
        supported_nodes = azure.supported_nodes()
    else:
        logging.error(f"Platform {platform} is not yet supported.")

    for resource in data["resources"]:
        resource_name = resource["name"]
        mode = resource["mode"]
        type = resource["type"]

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
            resources[resource_name] = {}
            resources[resource_name]["name"] = resource_name
            resources[resource_name]["type"] = type
            resources[resource_name]["mode"] = mode
            resources[resource_name]["resource_group"] = resource_group_name
            resources[resource_name]["attributes"] = attributes
            resources[resource_name]["components"] = {}
            components.append(Component(resource_name, type,
                              mode, resource_group_name, attributes))

    links = None
    if (not json_config_path is None):
        logging.info(f"Reading config from {json_config_path}.")
        cf = open(json_config_path)
        config_data = json.load(cf)
        if "links" in config_data:
            links = config_data["links"]

    if (not json_output_path is None):
        logging.info(f"Writing debug output to {json_output_path}.")
        with open(json_output_path, 'w') as f:
            json.dump(resources, f, indent=4)

    if (platform == 'azure'):
        azure.draw(name, output_path, components, links)
    else:
        print(f"Platform {platform} is not yet supported.")

    return 0


if __name__ == "__main__":
    sys.exit(main())  # type: ignore # pragma: no cover
