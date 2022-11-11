"""Azure AppServicePlan resource."""

from app.common.component import Component
from app.common.resource import Resource
from diagrams.azure import web
from typing import List, Dict

from app.azure.resources.common.common_service_plan import CommonServicePlan


class AppServicePlan(Resource):
    """Base resource component."""

    @staticmethod
    def identifier() -> str:
        """Get the identifier for this type in TF."""
        return "azurerm_app_service_plan"

    @staticmethod
    def get_metadata(component: Component) -> str:
        """Get the metadata string from this components attributes."""
        if 'kind' in component.attributes and 'sku' in component.attributes:
            sku = component.attributes['sku'][0]["tier"] + ", " + component.attributes['sku'][0]["size"]
            return f"OS: {component.attributes['kind']}, sku: {sku}"
        else:
            return ""

    @staticmethod
    def get_node(component: Component, **attrs: Dict):
        """Get the underlying diagrams type."""
        metadata = AppServicePlan.get_metadata(component)
        return web.AppServicePlans(Resource.get_name(component, metadata), **attrs)
    
    @staticmethod
    def group(components: List[Component]) -> List[Component]:
        """Handle service plan groupings."""
        return CommonServicePlan.group(AppServicePlan.identifier(), components)
