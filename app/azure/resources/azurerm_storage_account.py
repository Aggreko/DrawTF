"""Azure Storage resource."""

from typing import List
from app.common.component import Component
from app.common.resource import Resource
from diagrams.azure import storage

from app.azure.resources.azurerm_storage_container import StorageContainer


class Storage(Resource):
    """Base resource component."""

    @staticmethod
    def identifier() -> str:
        """Get the identifier for this type in TF."""
        return "azurerm_storage_account"

    @staticmethod
    def get_metadata(component: Component) -> str:
        """Get the metadata string from this components attributes."""
        access_tier = component.attributes['access_tier']
        account_kind = component.attributes['account_kind']
        account_replication_type = component.attributes['account_replication_type']
        account_tier = component.attributes['account_tier']
        return ",".join([access_tier, account_kind,
                         account_replication_type, account_tier])

    @staticmethod
    def get_node(component: Component, **attrs: dict):
        """Get the underlying diagrams type."""
        metadata = Storage.get_metadata(component)
        return storage.StorageAccounts(Resource.get_name(component, metadata), **attrs)
    
    @staticmethod
    def group(components: List[Component]) -> List[Component]:
        """Handle storage groupings."""
        storage_accounts = [
            x for x in components if x.type == Storage.identifier()]
        storage_containers = [
            x for x in components if x.type == StorageContainer.identifier()]

        for storage_container in storage_containers:
            storage_account_name = storage_container.attributes["storage_account_name"]
            
            storage_account = next(filter(
                    lambda x: x.attributes["name"] == storage_account_name, storage_accounts), None)

            if storage_account == None:
                storage_account = Component(
                    storage_account_name, Storage.identifier(), "data", storage_container.resource_group, 
                    {"name": storage_account_name, "resource_group_name": storage_container.resource_group})
                storage_accounts.append(storage_account)

            storage_account.add_component(storage_container)

        return storage_accounts
