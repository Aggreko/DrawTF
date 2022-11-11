"""Responsible for drawing azure resources"""
from typing import List
import logging

from diagrams import Diagram, Cluster, Edge, Node
from app.common.component import Component
from app.azure.azure_resource_factory import AzureResourceFactory
from app.common.resources.draw_custom import DrawCustom


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
    for component in components:
        bgcolor = "#F8F8F8"
        if (component.mode == "managed"):
            bgcolor = "#e5fbe5"
            
        graph_attrs = {
            "fontsize": "9",
            "margin": "30.0,1.0",
            "fontname":"times bold",
            "bgcolor": bgcolor,
        }
        
        if (component.is_cluster()):
            with Cluster(component.get_label().upper(), graph_attr=graph_attrs) as cluster:
                __draw(component.components, component.key, cache)
                
                if (not component.type == DrawCustom.identifier()):
                    __draw_component(component, group, cache)
                    
                cache['cluster-' + component.key] = cluster
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
            if not (link["from"] in cache and link["to"] in cache):
                logging.warning(f"Ignoring link as object not in component cache: {link}")
                continue
            
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
