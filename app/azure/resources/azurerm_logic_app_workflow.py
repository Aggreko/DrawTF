"""Azure LogicApp resource."""

from app.common.component import Component
from app.common.resource import Resource
from diagrams.azure import integration
from typing import Dict


class LogicApp(Resource):
    """Base resource component."""

    @staticmethod
    def identifier() -> str:
        """Get the identifier for this type in TF."""
        return "azurerm_logic_app_workflow"

    @staticmethod
    def get_metadata(component: Component) -> str:
        """Get the metadata string from this components attributes."""
        return ""

    @staticmethod
    def get_node(component: Component, **attrs: Dict):
        """Get the underlying diagrams type."""
        metadata = LogicApp.get_metadata(component)
        return integration.LogicApps(Resource.get_name(component, metadata), **attrs)
