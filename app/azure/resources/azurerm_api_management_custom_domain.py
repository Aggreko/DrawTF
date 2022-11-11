"""Azure ApiManagementDomain resource."""

from app.common.component import Component
from app.common.resource import Resource
from diagrams.azure import web


class ApiManagementDomain(Resource):
    """Base resource component."""

    @staticmethod
    def identifier() -> str:
        """Get the identifier for this type in TF."""
        return "azurerm_api_management_custom_domain"

    @staticmethod
    def get_metadata(component: Component) -> str:
        """Get the metadata string from this components attributes."""
        if "gateway" in component.attributes:
            for gateway in component.attributes['gateway']:
                if "host_name" in gateway:
                    return f"{gateway['host_name']}"
        return ""

    @staticmethod
    def get_node(component: Component, **attrs: dict):
        """Get the underlying diagrams type."""
        metadata = ApiManagementDomain.get_metadata(component)
        return web.AppServiceDomains(Resource.get_name(component, metadata), **attrs)
