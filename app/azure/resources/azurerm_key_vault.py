"""Azure keyVault resource."""

from app.common.component import Component
from app.common.resource import Resource
from diagrams.azure import security


class KeyVault(Resource):
    """Base resource component."""

    @staticmethod
    def identifier() -> str:
        """Get the identifier for this type in TF."""
        return "azurerm_key_vault"

    @staticmethod
    def get_metadata(component: Component) -> str:
        """Get the metadata string from this components attributes."""
        return f"sku: {component.attributes['sku_name']}"

    @staticmethod
    def get_node(component: Component, **attrs: dict):
        """Get the underlying diagrams type."""
        new_attrs: dict = {}
        new_attrs.update(attrs)
        metadata = KeyVault.get_metadata(component)
        return security.KeyVaults(Resource.get_name(component, metadata), **new_attrs)
