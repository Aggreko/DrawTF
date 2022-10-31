"""Azure ApiManagementDiagnostic resource."""

from draw.common.component import Component
from draw.common.resource import Resource
from diagrams.elastic import observability


class ApiManagementDiagnostic(Resource):
    """Base resource component."""

    @staticmethod
    def identifier() -> str:
        """Get the identifier for this type in TF."""
        return "azurerm_api_management_diagnostic"

    @staticmethod
    def get_metadata(component: Component) -> str:
        """Get the metadata string from this components attributes."""
        return ""

    @staticmethod
    def get_node(component: Component, **attrs: dict):
        """Get the underlying diagrams type."""
        metadata = ApiManagementDiagnostic.get_metadata(component)
        return observability.Metrics(Resource.get_name(component, metadata), **attrs)
