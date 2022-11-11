"""Azure Subnet resource."""

from app.common.component import Component
from app.common.resource import Resource
from diagrams.azure import network


class Subnet(Resource):
    """Base resource component."""

    @staticmethod
    def identifier() -> str:
        """Get the identifier for this type in TF."""
        return "azurerm_subnet"

    @staticmethod
    def get_metadata(component: Component) -> str:
        """Get the metadata string from this components attributes."""
        if "address_prefix" in component.attributes:
            return f"{component.attributes['address_prefix']}"
        else:
            return ""

    @staticmethod
    def get_node(component: Component, **attrs: dict):
        """Get the underlying diagrams type."""
        metadata = Subnet.get_metadata(component)
        return network.Subnets(Resource.get_name(component, metadata), **attrs)
