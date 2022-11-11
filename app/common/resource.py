"""Base diagram resource."""

from abc import ABC, abstractmethod
import re

from app.common.component import Component


class Resource(ABC):
    """Base resource component."""
    @staticmethod
    def get_name(component: Component, metadata: str) -> str:
        max_length = 25
        expression = "(.{" + str(max_length) + "})"
        
        component_name = component.name if len(component.name) <= max_length else re.sub(
            expression, "\\1\n", component.name, 0, re.DOTALL)
        
        if (component.type == "draw_custom"):
            return component_name
        
        component_type = component.type if len(component.type) <= max_length else re.sub(
            expression, "\\1\n", component.type, 0, re.DOTALL)
        if metadata != "":
            metadata = metadata if len(metadata) <= max_length else re.sub(
                expression, "\\1\n", metadata, 0, re.DOTALL)
        return f'{component_type}\n({component_name})\n{metadata}'

    @staticmethod
    @abstractmethod
    def identifier() -> str:
        """Get the identifier for this type in TF."""
        pass

    @staticmethod
    @abstractmethod
    def get_metadata(component: Component) -> str:
        """Get the metadata string from this components attributes."""
        pass

    @staticmethod
    @abstractmethod
    def get_node(component: Component, **attrs: dict):
        """Get the underlying diagrams type."""
        pass
