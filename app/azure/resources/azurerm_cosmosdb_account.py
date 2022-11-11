"""Azure CosmosAccount resource."""

from app.common.component import Component
from app.common.resource import Resource
from diagrams.azure import database
from typing import List, Dict

from app.azure.resources.azurerm_cosmosdb_sql_container import CosmosSqlContainer
from app.azure.resources.azurerm_cosmosdb_sql_database import CosmosSqlDatabase


class CosmosAccount(Resource):
    """Base resource component."""

    @staticmethod
    def identifier() -> str:
        """Get the identifier for this type in TF."""
        return "azurerm_cosmosdb_account"

    @staticmethod
    def get_metadata(component: Component) -> str:
        """Get the metadata string from this components attributes."""
        return f"sku: {component.attributes['offer_type']}"

    @staticmethod
    def get_node(component: Component, **attrs: Dict):
        """Get the underlying diagrams type."""
        metadata = CosmosAccount.get_metadata(component)
        return database.CosmosDb(Resource.get_name(component, metadata), **attrs)
    
    @staticmethod
    def group(components: List[Component]) -> List[Component]:
        """Handle cosmos account groupings."""
        cosmos_accounts = [
            x for x in components if x.type == CosmosAccount.identifier()]
        cosmos_dbs = CosmosSqlDatabase.group(components)

        for cosmos_db in cosmos_dbs:
            cosmos_db_name = cosmos_db.attributes["account_name"]
            
            cosmos_account = next(filter(
                    lambda x: x.attributes["name"] == cosmos_db_name, cosmos_accounts), None)

            if cosmos_account == None:
                cosmos_account = Component(
                    cosmos_db_name, CosmosAccount.identifier(), "data", cosmos_db.resource_group, {"name": cosmos_db_name, "resource_group_name": cosmos_db.resource_group})
                cosmos_accounts.append(cosmos_account)

            cosmos_account.add_component(cosmos_db)

        return cosmos_accounts
