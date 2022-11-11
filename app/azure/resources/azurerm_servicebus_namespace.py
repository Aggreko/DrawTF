"""Azure ServiceBusNamespace resource."""

from app.common.component import Component
from app.common.resource import Resource
from diagrams.azure import integration
from typing import List, Dict

from app.azure.resources.azurerm_servicebus_queue import ServiceBusQueue
from app.azure.resources.azurerm_servicebus_topic import ServiceBusTopic


class ServiceBusNamespace(Resource):
    """Base resource component."""

    @staticmethod
    def identifier() -> str:
        """Get the identifier for this type in TF."""
        return "azurerm_servicebus_namespace"

    @staticmethod
    def get_metadata(component: Component) -> str:
        """Get the metadata string from this components attributes."""
        if ("sku" in component.attributes):
            return f"sku: {component.attributes['sku']}"
        else:
            return ""

    @staticmethod
    def get_node(component: Component, **attrs: Dict):
        """Get the underlying diagrams type."""
        metadata = ServiceBusNamespace.get_metadata(component)
        return integration.ServiceBus(Resource.get_name(component, metadata), **attrs)
    
    @staticmethod
    def group(components: List[Component]) -> List[Component]:
        """Handle service bus namespace groupings."""
        servicebus_namespaces = [
            x for x in components if x.type.startswith(ServiceBusNamespace.identifier())]
        servicebus_topics = ServiceBusTopic.group(components)
        servicebus_queues = [
            x for x in components if x.type.startswith(ServiceBusQueue.identifier())]
        servicebus_queues = servicebus_queues + servicebus_topics
        
        for servicebus_queue in servicebus_queues:
            servicebus_namespace_name = ""
            if "namespace_id" in servicebus_queue.attributes:
                servicebus_namespace_id = servicebus_queue.attributes["namespace_id"]
                servicebus_namespace_name = servicebus_namespace_id.split("/")[-1]
            else:
                servicebus_namespace_name = servicebus_queue.attributes["namespace_name"]

            servicebus_namespace = next(filter(
                    lambda x: x.attributes["name"] == servicebus_namespace_name, servicebus_namespaces), None)

            if servicebus_namespace == None:
                servicebus_namespace = Component(
                    servicebus_namespace_name, ServiceBusNamespace.identifier(), "data", servicebus_queue.resource_group, {"name": servicebus_namespace_name, "resource_group_name": servicebus_queue.resource_group})
                servicebus_namespaces.append(servicebus_namespace)

            servicebus_namespace.add_component(servicebus_queue)

        return servicebus_namespaces
