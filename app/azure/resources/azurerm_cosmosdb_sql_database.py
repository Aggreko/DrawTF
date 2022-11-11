"""Azure CosmosSqlDatabase resource."""

from app.common.component import Component
from app.common.resource import Resource
from diagrams.azure import database
from typing import List, Dict

from app.azure.resources.azurerm_servicebus_queue import ServiceBusQueue
from app.azure.resources.azurerm_cosmosdb_sql_container import CosmosSqlContainer


class CosmosSqlDatabase(Resource):
    """Base resource component."""

    @staticmethod
    def identifier() -> str:
        """Get the identifier for this type in TF."""
        return "azurerm_cosmosdb_sql_database"

    @staticmethod
    def get_metadata(component: Component) -> str:
        """Get the metadata string from this components attributes."""
        return f"RU: {component.attributes['throughput']}"

    @staticmethod
    def get_node(component: Component, **attrs: Dict):
        """Get the underlying diagrams type."""
        metadata = CosmosSqlDatabase.get_metadata(component)
        return database.SQLDatabases(Resource.get_name(component, metadata), **attrs)
    
    @staticmethod
    def group(components: List[Component]) -> List[Component]:
        """Handle cosmos database groupings."""
        cosmos_sql_databases = [
            x for x in components if x.type == CosmosSqlDatabase.identifier()]
        cosmos_containers = [
            x for x in components if x.type == CosmosSqlContainer.identifier()]

        for cosmos_container in cosmos_containers:
            cosmos_database_name = cosmos_container.attributes["database_name"]
            
            cosmos_database = next(filter(
                    lambda x: x.attributes["name"] == cosmos_database_name, cosmos_sql_databases), None)

            if cosmos_database == None:
                cosmos_database = Component(
                    cosmos_database_name, CosmosSqlDatabase.identifier(), "data", cosmos_container.resource_group, 
                    {"name": cosmos_database_name, "account_name": cosmos_container.attributes["account_name"], "resource_group_name": cosmos_container.resource_group})
                cosmos_sql_databases.append(cosmos_database)

            cosmos_database.add_component(cosmos_container)

        return cosmos_sql_databases
