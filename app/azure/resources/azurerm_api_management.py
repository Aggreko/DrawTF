"""Azure ApiManagement resource."""

from app.common.component import Component
from app.common.resource import Resource
from diagrams.azure import integration
from typing import List
import logging


class ApiManagement(Resource):
    """Base resource component."""

    @staticmethod
    def identifier() -> str:
        """Get the identifier for this type in TF."""
        return "azurerm_api_management"

    @staticmethod
    def get_metadata(component: Component) -> str:
        """Get the metadata string from this components attributes."""
        return f"sku: {component.attributes['sku_name']}"

    @staticmethod
    def get_node(component: Component, **attrs: dict):
        """Get the underlying diagrams type."""
        metadata = ApiManagement.get_metadata(component)
        return integration.APIManagement(Resource.get_name(component, metadata), **attrs)

    @staticmethod
    def group(components: List[Component]) -> List[Component]:
        """Handle api management groupings."""
        apim_resources_all = [
            x for x in components if x.type.startswith(ApiManagement.identifier())]
        apim_resources_top_level = [
            x for x in apim_resources_all if x.type == ApiManagement.identifier()]
        apim_resources_sub_level = [
            x for x in apim_resources_all if not x.type == ApiManagement.identifier()]

        for apim_sub in apim_resources_sub_level:
            apim = None
            if "api_management_name" in apim_sub.attributes:
                apim = next(filter(
                    lambda x: x.name == apim_sub.attributes["api_management_name"], apim_resources_top_level), None)

            if apim == None and "api_management_id" in apim_sub.attributes:
                apim = next(filter(
                    lambda x: x.attributes["id"] == apim_sub.attributes["api_management_id"], apim_resources_top_level), None)

            if apim == None:
                logging.error(
                    f"No parent for resource {apim_sub.type}: {apim_sub.name}")
                continue

            apim.add_component(apim_sub)

        return apim_resources_top_level
