"""Azure DatabricksCluster resource."""

from app.common.component import Component
from app.common.resource import Resource
from diagrams.azure import analytics
from typing import Dict


class DatabricksCluster(Resource):
    """Base resource component."""

    @staticmethod
    def identifier() -> str:
        """Get the identifier for this type in TF."""
        return "databricks_cluster"

    @staticmethod
    def get_metadata(component: Component) -> str:
        """Get the metadata string from this components attributes."""
        if  "cluster_id" in component.attributes and \
            "driver_node_type_id" in component.attributes and \
            "node_type_id" in component.attributes and \
            "spark_version" in component.attributes and \
            "num_workers" in component.attributes:
            cluster_id = component.attributes['cluster_id']
            driver_node_type_id = component.attributes['driver_node_type_id']
            node_type_id = component.attributes['node_type_id']
            spark_version = component.attributes['spark_version']
            num_workers = component.attributes['num_workers']
            return ", ".join([
                ('Id:' + str(cluster_id) + ''),
                ('Driver:' + str(driver_node_type_id) + ''),
                ('Worker:' + str(node_type_id) + ''),
                ('Version:' + str(spark_version) + ''),
                ('Num:' + str(num_workers) + '')
            ])
        else:
            return ""

    @staticmethod
    def get_node(component: Component, **attrs: Dict):
        """Get the underlying diagrams type."""
        metadata = DatabricksCluster.get_metadata(component)
        return analytics.Hdinsightclusters(Resource.get_name(component, metadata), **attrs)
