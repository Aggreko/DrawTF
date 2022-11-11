"""Azure ResourceGroup resource."""

from app.common.component import Component
from app.common.resource import Resource
from diagrams.azure import general
from typing import List


class ResourceGroup(Resource):
    """Base resource component."""

    @staticmethod
    def identifier() -> str:
        """Get the identifier for this type in TF."""
        return "azurerm_resource_group"

    @staticmethod
    def get_metadata(component: Component) -> str:
        """Get the metadata string from this components attributes."""
        return ""

    @staticmethod
    def get_node(component: Component, **attrs: dict):
        """Get the underlying diagrams type."""
        metadata = ResourceGroup.get_metadata(component)
        return general.Resourcegroups(Resource.get_name(component, metadata), **attrs)

    @staticmethod
    def group(resource_groups: List[Component], components: List[Component]) -> List[Component]:
        """Nest inside related resource groups."""
        resource_groups_copy = resource_groups.copy()

        for component in components:
            resource_group = next(filter(
                lambda x: x.name.lower() == component.resource_group.lower(), resource_groups_copy), None)

            if resource_group == None:
                resource_group = Component(
                    component.resource_group, ResourceGroup.identifier(), "data", "Unparented", {})
                resource_groups_copy.append(resource_group)

            resource_group.add_component(component)

        return resource_groups_copy
