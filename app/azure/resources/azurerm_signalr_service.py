"""Azure Signalr resource."""

from app.common.component import Component
from app.common.resource import Resource
from diagrams.azure import web
from typing import Dict


class Signalr(Resource):
    """Base resource component."""

    @staticmethod
    def identifier() -> str:
        """Get the identifier for this type in TF."""
        return "azurerm_signalr_service"

    @staticmethod
    def get_metadata(component: Component) -> str:
        """Get the metadata string from this components attributes."""
        if 'sku' in component.attributes:
            capacity = component.attributes['sku'][0]['capacity']
            tier = component.attributes['sku'][0]["name"]
            return f"Capacity: {(str(capacity))}, sku: {tier}"
        else:
            return ""

    @staticmethod
    def get_node(component: Component, **attrs: Dict):
        """Get the underlying diagrams type."""
        metadata = Signalr.get_metadata(component)
        return web.Signalr(Resource.get_name(component, metadata), **attrs)
