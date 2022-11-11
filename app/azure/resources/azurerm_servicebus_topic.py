
"""Azure ServiceBusTopic resource."""

from app.common.component import Component
from app.common.resource import Resource
from diagrams.azure import integration
from typing import List, Dict

from app.azure.resources.azurerm_servicebus_subscription import ServiceBusSubscription


class ServiceBusTopic(Resource):
    """Base resource component."""

    @staticmethod
    def identifier() -> str:
        """Get the identifier for this type in TF."""
        return "azurerm_servicebus_topic"

    @staticmethod
    def get_metadata(component: Component) -> str:
        """Get the metadata string from this components attributes."""
        if "max_message_size_in_kilobytes" in component.attributes and "max_message_size_in_kilobytes" in component.attributes:
            max_message_size_in_kilobytes = component.attributes['max_message_size_in_kilobytes']
            max_size_in_megabytes = component.attributes['max_size_in_megabytes']
            return ", ".join([
                ('Message: ' + str(max_message_size_in_kilobytes) + 'kb'), 
                ('Size:' + str(max_size_in_megabytes) + 'MB')
            ])
        else:
            return ""

    @staticmethod
    def get_node(component: Component, **attrs: Dict):
        """Get the underlying diagrams type."""
        metadata = ServiceBusTopic.get_metadata(component)
        return integration.SystemTopic(Resource.get_name(component, metadata), **attrs)
    
    @staticmethod
    def group(components: List[Component]) -> List[Component]:
        """Handle service bus topic groupings."""
        servicebus_topics = [
            x for x in components if x.type.startswith(ServiceBusTopic.identifier())]
        servicebus_subscriptions = [
            x for x in components if x.type.startswith(ServiceBusSubscription.identifier())]

        for servicebus_queue in servicebus_subscriptions:
            servicebus_topic_id = ""
            if "topic_id" in servicebus_queue.attributes:
                servicebus_topic_id = servicebus_queue.attributes["topic_id"]
            else:
                continue
            
            servicebus_topic = next(filter(
                    lambda x: x.attributes["id"] == servicebus_topic_id, servicebus_topics), None)

            if servicebus_topic == None:
                continue

            servicebus_topic.add_component(servicebus_queue)

        return servicebus_topics
