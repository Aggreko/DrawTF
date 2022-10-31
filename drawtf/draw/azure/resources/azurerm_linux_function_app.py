"""Azure FunctionAppLinux resource."""

from draw.common.component import Component
from draw.common.resource import Resource
from diagrams.azure import compute
from typing import Dict


class FunctionAppLinux(Resource):
    """Base resource component."""

    @staticmethod
    def identifier() -> str:
        """Get the identifier for this type in TF."""
        return "azurerm_linux_function_app"

    @staticmethod
    def get_metadata(component: Component) -> str:
        """Get the metadata string from this components attributes."""
        return ""

    @staticmethod
    def get_node(component: Component, **attrs: Dict):
        """Get the underlying diagrams type."""
        metadata = FunctionAppLinux.get_metadata(component)
        return compute.FunctionApps(Resource.get_name(component, metadata), **attrs)
