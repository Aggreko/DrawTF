"""Azure DrawCustom resource."""

from app.common.component import Component
from app.common.resource import Resource
from diagrams.azure import integration
from typing import Dict


class DrawCustom(Resource):
    """Base resource component."""

    @staticmethod
    def identifier() -> str:
        """Get the identifier for this type in TF."""
        return "draw_custom"

    @staticmethod
    def get_metadata(component: Component) -> str:
        """Get the metadata string from this components attributes."""
        return ""

    @staticmethod
    def get_node(component: Component, **attrs: Dict):
        """Get the underlying diagrams type."""
        if (component.custom == None):
            return integration.APIManagement("test");
        
        names = str(component.custom).split(".")
        from_names = ".".join(names[0:2])
        import_name = ".".join(names[2:3])
        type_names = ".".join(names[2:4])
        
        command = 'exec("from ' + from_names + ' import ' + import_name + '") or ' + type_names + '(Resource.get_name(component, ""), **attrs)'
        return eval(command)
