"""Azure AppServicePlan resource."""

from app.common.component import Component
from app.common.resource import Resource
from diagrams.azure import web
from typing import List, Dict

from app.azure.resources.common.common_service_plan import CommonServicePlan


class ServicePlan(CommonServicePlan):
    """Base resource component."""

    @staticmethod
    def identifier() -> str:
        """Get the identifier for this type in TF."""
        return "azurerm_service_plan"

    @staticmethod
    def get_metadata(component: Component) -> str:
        """Get the metadata string from this components attributes."""
        if 'os_type' in component.attributes and 'sku_name' in component.attributes:
            return f"OS: {component.attributes['os_type']}, sku: {component.attributes['sku_name']}"
        else:
            return ""

    @staticmethod
    def get_node(component: Component, **attrs: Dict):
        """Get the underlying diagrams type."""
        metadata = ServicePlan.get_metadata(component)
        return web.AppServicePlans(Resource.get_name(component, metadata), **attrs)
    
    @staticmethod
    def group(components: List[Component]) -> List[Component]:
        """Handle service plan groupings."""
        return CommonServicePlan.group(ServicePlan.identifier(), components)
