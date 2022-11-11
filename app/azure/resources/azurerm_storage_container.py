"""Azure StorageContainer resource."""

from app.common.component import Component
from app.common.resource import Resource
from diagrams.azure import storage


class StorageContainer(Resource):
    """Base resource component."""

    @staticmethod
    def identifier() -> str:
        """Get the identifier for this type in TF."""
        return "azurerm_storage_container"

    @staticmethod
    def get_metadata(component: Component) -> str:
        return f"Access: {component.attributes['container_access_type']}"

    @staticmethod
    def get_node(component: Component, **attrs: dict):
        """Get the underlying diagrams type."""
        metadata = StorageContainer.get_metadata(component)
        return storage.BlobStorage(Resource.get_name(component, metadata), **attrs)
