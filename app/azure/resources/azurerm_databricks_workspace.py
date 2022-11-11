"""Azure DatabricksWorkspace resource."""

from app.common.component import Component
from app.common.resource import Resource
from diagrams.azure import analytics
from typing import Dict, List

from app.azure.resources.databricks_cluster import DatabricksCluster
from app.azure.resources.databricks_azure_adls_gen2_mount import DatabricksGen2Mount


class DatabricksWorkspace(Resource):
    """Base resource component."""

    @staticmethod
    def identifier() -> str:
        """Get the identifier for this type in TF."""
        return "azurerm_databricks_workspace"

    @staticmethod
    def get_metadata(component: Component) -> str:
        """Get the metadata string from this components attributes."""
        return f"{component.attributes['sku']}"

    @staticmethod
    def get_node(component: Component, **attrs: Dict):
        """Get the underlying diagrams type."""
        metadata = DatabricksWorkspace.get_metadata(component)
        return analytics.Databricks(Resource.get_name(component, metadata), **attrs)    
    
    @staticmethod
    def group(components: List[Component]) -> List[Component]:
        """Handle service bus namespace groupings."""
        databricks_workspaces = [
            x for x in components if x.type.startswith(DatabricksWorkspace.identifier())]
        
        if (len(databricks_workspaces) <= 0):
            return []
        
        databricks_workspace = databricks_workspaces[0]
        databricks_clusters = [
            x for x in components if x.type.startswith(DatabricksCluster.identifier())]
        databricks_mounts = [
            x for x in components if x.type.startswith(DatabricksGen2Mount.identifier())]
        
        for databricks_cluster in databricks_clusters:
            databricks_workspace.add_component(databricks_cluster)
        
        for databricks_mount in databricks_mounts:
            databricks_workspace.add_component(databricks_mount)
            
        return [databricks_workspace]
