
"""Azure ServiceBusSubscription resource."""

from app.common.component import Component
from app.common.resource import Resource
from diagrams.azure import integration
from typing import Dict


class ServiceBusSubscription(Resource):
    """Base resource component."""

    @staticmethod
    def identifier() -> str:
        """Get the identifier for this type in TF."""
        return "azurerm_servicebus_subscription"

    @staticmethod
    def get_metadata(component: Component) -> str:
        """Get the metadata string from this components attributes."""
        if "max_delivery_count" in component.attributes and "requires_session" in component.attributes:
            max_delivery_count = component.attributes['max_delivery_count']
            requires_session = component.attributes['requires_session']
            return ", ".join([
                ('Max Delivery: ' + str(max_delivery_count)), 
                ('Session:' + str(requires_session))
            ])
        else:
            return ""

    @staticmethod
    def get_node(component: Component, **attrs: Dict):
        """Get the underlying diagrams type."""
        metadata = ServiceBusSubscription.get_metadata(component)
        return integration.EventGridSubscriptions(Resource.get_name(component, metadata), **attrs)
