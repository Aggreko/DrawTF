"""Azure StaticWebApp resource."""

from app.common.component import Component
from app.common.resource import Resource
from diagrams.azure import web

class StaticWebApp(Resource):
    """Base resource component."""

    @staticmethod
    def identifier() -> str:
        """Get the identifier for this type in TF."""
        return "azurerm_static_site"

    @staticmethod
    def get_metadata(component: Component) -> str:
        """Get the metadata string from this components attributes."""
        host = component.attributes['default_host_name']
        sku_tier = component.attributes['sku_tier']
        return ",".join([host, sku_tier])

    @staticmethod
    def get_node(component: Component, **attrs: dict):
        """Get the underlying diagrams type."""
        metadata = StaticWebApp.get_metadata(component)
        return web.AppServices(Resource.get_name(component, metadata), **attrs)
