"""Azure SqlServerDatabase resource."""

from app.common.component import Component
from app.common.resource import Resource
from diagrams.azure import database
from typing import Dict


class SqlServerDatabase(Resource):
    """Base resource component."""

    @staticmethod
    def identifier() -> str:
        """Get the identifier for this type in TF."""
        return "azurerm_mssql_database"

    @staticmethod
    def get_metadata(component: Component) -> str:
        """Get the metadata string from this components attributes."""
        if "sku_name" in component.attributes and "max_size_gb" in component.attributes:
            sku_name = component.attributes['sku_name']
            max_size_gb = component.attributes['max_size_gb']
            return ", ".join([
                ('Public:' + str(sku_name) + ''),
                ('Max size:' + str(max_size_gb) + 'GB')
            ])
        else:
            return ""

    @staticmethod
    def get_node(component: Component, **attrs: Dict):
        """Get the underlying diagrams type."""
        metadata = SqlServerDatabase.get_metadata(component)
        return database.SQLDatabases(Resource.get_name(component, metadata), **attrs)
