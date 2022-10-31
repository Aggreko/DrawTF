"""Responsible for drawing azure resources"""
from typing import List
import logging

from diagrams import Diagram, Cluster, Edge, Node
from draw.common.component import Component
from draw.azure.azure_resource_factory import AzureResourceFactory


def supported_nodes():
    return AzureResourceFactory.get_supported_nodes()


def draw(name: str, output_path: str, components: List[Component], links=[]):
    """Create the azure diagram."""
    cache = {}

    logging.info("drawing...")
    
    tags = {}
    for component in components:
        if "tags" in component.attributes:
            tags.update(component.attributes["tags"])
    
    tag_string = ""
    if len(tags.keys()) > 0:
        tag_string = "Tags: \l\n" #type: ignore
        tag_strings = []
        for key in tags.keys():
            tag_strings.append(f"{key}: {tags[key]} \l") #type: ignore
        tag_string = tag_string + "".join(tag_strings)
            
    grouped_components = AzureResourceFactory.nest_resources(components)

    graph_attr = {
        "splines": "ortho",
        "layout": "dot",
        "fontname":"times bold"
    }
    with Diagram(name, show=False, direction="TB", filename=output_path, graph_attr=graph_attr):
        __draw(grouped_components, "root", cache)
        __link(links, cache)
        if (not tag_string == ""):
            attrs = {
                "shape":"plaintext", 
                "fontsize": "9",
                "fontname":"times italic"
            }
            Node(label=tag_string, **attrs)


def __draw(components: List[Component], group: str, cache: dict):
    """Group related azure resources together."""
    graph_attrs = {
        "fontsize": "9",
        "margin": "30.0,1.0",
        "fontname":"times bold"
    }
    for component in components:
        if (component.is_cluster()):
            with Cluster(f"{component.type}: {component.name}".upper(), graph_attr=graph_attrs) as cluster:
                __draw(component.components, component.key, cache)
                __draw_component(component, group, cache)
                cache[component.name] = cluster
        else:
            __draw_component(component, group, cache)


def __draw_component(component: Component, group: str, cache: dict):
    node = AzureResourceFactory.get_node(component, group)
    if not node == None:
        cache[component.key] = node
    else:
        logging.warning(
            f"No resource icon for {component.type}: {component.name} is not yet supported")


def __link(links, cache: dict):
    """Setup links to all components in diagram."""
    if (links == None):
        return

    logging.info("linking...")

    for link in links:
        if not ("to" in link and "from" in link):
            logging.error(f"link does not contain and to and from: {link}")
            continue
        else:
            component_from = cache[link["from"]]
            component_to = cache[link["to"]]

            label: str = ""
            if "label" in link:
                label = link["label"]

            type: str = "dashed"
            if "type" in link:
                type = link["type"]

            # https://graphviz.org/doc/info/colors.html
            color: str = "black"
            if "color" in link:
                color = link["color"]

            component_from >> Edge(
                label=label, style=type, color=color) >> component_to  # type: ignore
