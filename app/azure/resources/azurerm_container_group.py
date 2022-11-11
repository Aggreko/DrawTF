"""Azure ContainerGroup resource."""

from app.common.component import Component
from app.common.resource import Resource
from diagrams.azure import compute


class ContainerGroup(Resource):
    """Base resource component."""

    @staticmethod
    def identifier() -> str:
        """Get the identifier for this type in TF."""
        return "azurerm_container_group"

    @staticmethod
    def get_metadata(component: Component) -> str:
        """Get the metadata string from this components attributes."""
        return f"OS: {component.attributes['os_type']}"

    @staticmethod
    def get_node(component: Component, **attrs: dict):
        """Get the underlying diagrams type."""
        metadata = ContainerGroup.get_metadata(component)
        return compute.ContainerInstances(Resource.get_name(component, metadata), **attrs)
