"""Azure ApiManagementLogger resource."""

from app.common.component import Component
from app.common.resource import Resource
from diagrams.azure import devops


class ApiManagementLogger(Resource):
    """Base resource component."""

    @staticmethod
    def identifier() -> str:
        """Get the identifier for this type in TF."""
        return "azurerm_api_management_logger"

    @staticmethod
    def get_metadata(component: Component) -> str:
        """Get the metadata string from this components attributes."""
        return ""

    @staticmethod
    def get_node(component: Component, **attrs: dict):
        """Get the underlying diagrams type."""
        metadata = ApiManagementLogger.get_metadata(component)
        return devops.ApplicationInsights(Resource.get_name(component, metadata), **attrs)
