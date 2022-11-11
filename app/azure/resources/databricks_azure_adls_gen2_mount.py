"""Azure DatabricksGen2Mount resource."""

from app.common.component import Component
from app.common.resource import Resource
from diagrams.azure import analytics
from typing import Dict


class DatabricksGen2Mount(Resource):
    """Base resource component."""

    @staticmethod
    def identifier() -> str:
        """Get the identifier for this type in TF."""
        return "databricks_azure_adls_gen2_mount"

    @staticmethod
    def get_metadata(component: Component) -> str:
        """Get the metadata string from this components attributes."""
        if  "storage_account_name" in component.attributes and "container_name" in component.attributes:
            storage_account_name = component.attributes['storage_account_name']
            container_name = component.attributes['container_name']
            return ", ".join([
                ('Account:' + str(storage_account_name) + ''),
                ('Container:' + str(container_name) + '')
            ])
        else:
            return ""

    @staticmethod
    def get_node(component: Component, **attrs: Dict):
        """Get the underlying diagrams type."""
        metadata = DatabricksGen2Mount.get_metadata(component)
        return analytics.DataLakeStoreGen1(Resource.get_name(component, metadata), **attrs)
