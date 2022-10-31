"""Azure CosmosSqlContainer resource."""

from draw.common.component import Component
from draw.common.resource import Resource
from diagrams.azure import database
from typing import Dict

from draw.azure.resources.azurerm_servicebus_queue import ServiceBusQueue


class CosmosSqlContainer(Resource):
    """Base resource component."""

    @staticmethod
    def identifier() -> str:
        """Get the identifier for this type in TF."""
        return "azurerm_cosmosdb_sql_container"

    @staticmethod
    def get_metadata(component: Component) -> str:
        """Get the metadata string from this components attributes."""
        return f"partition: {component.attributes['partition_key_path']}"

    @staticmethod
    def get_node(component: Component, **attrs: Dict):
        """Get the underlying diagrams type."""
        metadata = CosmosSqlContainer.get_metadata(component)
        return database.CosmosDb(Resource.get_name(component, metadata), **attrs)
