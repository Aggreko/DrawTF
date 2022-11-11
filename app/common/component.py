"""Component class which builds up a tree of objects."""

from typing import List


class Component:
    """Component class which builds up a tree of objects."""

    def __init__(self, name: str, type: str, mode: str, resource_group: str, attributes: dict, components = [], custom = None):
        """Ctor for component."""
        self.name = name
        self.type = type
        self.key = f"{name}-{type}"
        self.mode = mode
        self.resource_group = resource_group
        self.attributes = attributes
        self.components: List[Component] = components.copy()
        self.custom = custom
        

    def get_label(self):
        """Get Components from structure."""
        if (self.type == "draw_custom"):
            return self.name
        else:
            return f"{self.type}: {self.name}"

    def get_components(self):
        """Get Components from structure."""
        return self.components
    
    def add_component(self, component):
        """Add a Component to the tree structure."""
        self.components.append(component)

    def is_cluster(self) -> bool:
        """Check if this is a cluster type."""
        return len(self.components) > 0
