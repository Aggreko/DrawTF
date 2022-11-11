"""Azure ApiManagementApi resource."""

from app.common.component import Component
from app.common.resource import Resource
from diagrams.azure import web
from typing import Dict


class ApiManagementApi(Resource):
    """Base resource component."""

    @staticmethod
    def identifier() -> str:
        """Get the identifier for this type in TF."""
        return "azurerm_api_management_api"

    @staticmethod
    def get_metadata(component: Component) -> str:
        """Get the metadata string from this components attributes."""
        return f"Display: {component.attributes['display_name']}, Rev: {component.attributes['revision']}"

    @staticmethod
    def get_node(component: Component, **attrs: Dict):
        """Get the underlying diagrams type."""
        metadata = ApiManagementApi.get_metadata(component)
        return web.APIConnections(Resource.get_name(component, metadata), **attrs)
