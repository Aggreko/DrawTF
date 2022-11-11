"""Azure AppConfig resource."""

from app.common.component import Component
from app.common.resource import Resource
from diagrams.azure import integration


class AppConfig(Resource):
    """Base resource component."""

    @staticmethod
    def identifier() -> str:
        """Get the identifier for this type in TF."""
        return "azurerm_app_configuration"

    @staticmethod
    def get_metadata(component: Component) -> str:
        """Get the metadata string from this components attributes."""
        return f"sku: {component.attributes['sku']}"

    @staticmethod
    def get_node(component: Component, **attrs: dict):
        """Get the underlying diagrams type."""
        metadata = AppConfig.get_metadata(component)
        return integration.AppConfiguration(Resource.get_name(component, metadata), **attrs)
