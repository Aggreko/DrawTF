"""Azure AppServiceSlot resource."""

from app.common.component import Component
from app.common.resource import Resource
from diagrams.azure import web
from typing import Dict


class AppServiceSlot(Resource):
    """Base resource component."""

    @staticmethod
    def identifier() -> str:
        """Get the identifier for this type in TF."""
        return "azurerm_app_service_slot"

    @staticmethod
    def get_metadata(component: Component) -> str:
        """Get the metadata string from this components attributes."""
        return ""

    @staticmethod
    def get_node(component: Component, **attrs: Dict):
        """Get the underlying diagrams type."""
        metadata = AppServiceSlot.get_metadata(component)
        return web.AppServices(Resource.get_name(component, metadata), **attrs)
