"""Azure ServiceBusQueue resource."""

from app.common.component import Component
from app.common.resource import Resource
from diagrams.azure import integration
from typing import List, Dict

from app.azure.resources.azurerm_servicebus_subscription import ServiceBusSubscription


class ServiceBusQueue(Resource):
    """Base resource component."""

    @staticmethod
    def identifier() -> str:
        """Get the identifier for this type in TF."""
        return "azurerm_servicebus_queue"

    @staticmethod
    def get_metadata(component: Component) -> str:
        """Get the metadata string from this components attributes."""
        if "max_message_size_in_kilobytes" in component.attributes and "max_message_size_in_kilobytes" in component.attributes and "requires_session" in component.attributes:
            max_message_size_in_kilobytes = component.attributes['max_message_size_in_kilobytes']
            max_size_in_megabytes = component.attributes['max_size_in_megabytes']
            requires_session = component.attributes['requires_session']
            return ", ".join([
                ('Message: ' + str(max_message_size_in_kilobytes) + 'kb'), 
                ('Size:' + str(max_size_in_megabytes) + 'MB'), 
                ('Session:' + str(requires_session))
            ])
        else:
            return ""

    @staticmethod
    def get_node(component: Component, **attrs: Dict):
        """Get the underlying diagrams type."""
        metadata = ServiceBusQueue.get_metadata(component)
        return integration.ServiceBus(Resource.get_name(component, metadata), **attrs)
