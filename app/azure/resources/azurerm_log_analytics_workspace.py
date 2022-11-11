"""Azure LogAnalyticsWorkspace resource."""

from app.common.component import Component
from app.common.resource import Resource
from diagrams.azure import analytics
from typing import Dict


class LogAnalyticsWorkspace(Resource):
    """Base resource component."""

    @staticmethod
    def identifier() -> str:
        """Get the identifier for this type in TF."""
        return "azurerm_log_analytics_workspace"

    @staticmethod
    def get_metadata(component: Component) -> str:
        """Get the metadata string from this components attributes."""
        if "sku" in component.attributes and "retention_in_days" in component.attributes:
            sku = component.attributes['sku']
            retention_in_days = component.attributes['retention_in_days']
            return ", ".join([
                ('Sku: ' + str(sku)), 
                ('Retention:' + str(retention_in_days) + ' days')
            ])
        else:
            return ""

    @staticmethod
    def get_node(component: Component, **attrs: Dict):
        """Get the underlying diagrams type."""
        metadata = LogAnalyticsWorkspace.get_metadata(component)
        return analytics.LogAnalyticsWorkspaces(Resource.get_name(component, metadata), **attrs)
