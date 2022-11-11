"""Azure ContainerRegistry resource."""

from app.common.component import Component
from app.common.resource import Resource
from diagrams.azure import compute


class ContainerRegistry(Resource):
    """Base resource component."""

    @staticmethod
    def identifier() -> str:
        """Get the identifier for this type in TF."""
        return "azurerm_container_registry"

    @staticmethod
    def get_metadata(component: Component) -> str:
        """Get the metadata string from this components attributes."""
        return f"sku: {component.attributes['sku']}"

    @staticmethod
    def get_node(component: Component, **attrs: dict):
        """Get the underlying diagrams type."""
        metadata = ContainerRegistry.get_metadata(component)
        return compute.ContainerRegistries(Resource.get_name(component, metadata), **attrs)
