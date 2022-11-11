"""Azure KubernetesCluster resource."""

from app.common.component import Component
from app.common.resource import Resource
from diagrams.azure import compute
from typing import Dict


class KubernetesCluster(Resource):
    """Base resource component."""

    @staticmethod
    def identifier() -> str:
        """Get the identifier for this type in TF."""
        return "azurerm_kubernetes_cluster"

    @staticmethod
    def get_metadata(component: Component) -> str:
        """Get the metadata string from this components attributes."""
        if  "sku_tier" in component.attributes and \
            "default_node_pool" in component.attributes:
            sku_tier = component.attributes['sku_tier']
            default_node_pool = component.attributes['default_node_pool'][0]
            node_count = default_node_pool['node_count']
            vm_size = default_node_pool['vm_size']
            return ", ".join([
                ('Sku:' + str(sku_tier) + ''),
                ('Nodes:' + str(node_count) + ''),
                ('Size:' + str(vm_size) + '')
            ])
        else:
            return ""

    @staticmethod
    def get_node(component: Component, **attrs: Dict):
        """Get the underlying diagrams type."""
        metadata = KubernetesCluster.get_metadata(component)
        return compute.KubernetesServices(Resource.get_name(component, metadata), **attrs)
