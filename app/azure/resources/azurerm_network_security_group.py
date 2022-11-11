"""Azure NetworkSecurityGroup resource."""

from app.common.component import Component
from app.common.resource import Resource
from diagrams.azure import network


class NetworkSecurityGroup(Resource):
    """Base resource component."""

    @staticmethod
    def identifier() -> str:
        """Get the identifier for this type in TF."""
        return "azurerm_network_security_group"

    @staticmethod
    def get_metadata(component: Component) -> str:
        return ""

    @staticmethod
    def get_node(component: Component, **attrs: dict):
        """Get the underlying diagrams type."""
        metadata = NetworkSecurityGroup.get_metadata(component)
        return network.NetworkSecurityGroupsClassic(Resource.get_name(component, metadata), **attrs)
