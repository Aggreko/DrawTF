"""Factory for doing common tasks around azure diagrams components"""
from typing import List
import logging

from draw.common.component import Component
from draw.azure.resources.azurerm_key_vault import KeyVault
from draw.azure.resources.azurerm_api_management import ApiManagement
from draw.azure.resources.azurerm_application_insights import AppInsights
from draw.azure.resources.azurerm_subnet import Subnet
from draw.azure.resources.azurerm_resource_group import ResourceGroup
from draw.azure.resources.azurerm_storage_account import Storage
from draw.azure.resources.azurerm_api_management_custom_domain import ApiManagementDomain
from draw.azure.resources.azurerm_app_configuration import AppConfig
from draw.azure.resources.azurerm_api_management_certificate import ApiManagementCertificate
from draw.azure.resources.azurerm_api_management_diagnostic import ApiManagementDiagnostic
from draw.azure.resources.azurerm_api_management_logger import ApiManagementLogger
from draw.azure.resources.azurerm_function_app import FunctionApp
from draw.azure.resources.azurerm_api_management_api import ApiManagementApi
from draw.azure.resources.azurerm_service_plan import ServicePlan
from draw.azure.resources.azurerm_function_app_slot import FunctionAppSlot
from draw.azure.resources.azurerm_servicebus_namespace import ServiceBusNamespace
from draw.azure.resources.azurerm_servicebus_queue import ServiceBusQueue
from draw.azure.resources.azurerm_app_service import AppService
from draw.azure.resources.azurerm_app_service_plan import AppServicePlan
from draw.azure.resources.azurerm_linux_function_app import FunctionAppLinux
from draw.azure.resources.azurerm_signalr_service import Signalr
from draw.azure.resources.azurerm_container_group import ContainerGroup
from draw.azure.resources.azurerm_container_registry import ContainerRegistry
from draw.azure.resources.azurerm_windows_web_app import WindowsWebApp
from draw.azure.resources.azurerm_cosmosdb_account import CosmosAccount
from draw.azure.resources.azurerm_cosmosdb_sql_container import CosmosSqlContainer
from draw.azure.resources.azurerm_cosmosdb_sql_database import CosmosSqlDatabase
from draw.azure.resources.azurerm_windows_web_app_slot import WindowsWebAppSlot
from draw.azure.resources.azurerm_app_service_slot import AppServiceSlot
from draw.azure.resources.azurerm_storage_container import StorageContainer
from draw.azure.resources.azurerm_network_security_group import NetworkSecurityGroup


class AzureResourceFactory:
    @staticmethod
    def get_supported_nodes() -> List[str]:
        return [
            KeyVault.identifier(),
            Subnet.identifier(),
            ApiManagement.identifier(),
            ApiManagementApi.identifier(),
            ApiManagementCertificate.identifier(),
            ApiManagementDomain.identifier(),
            ApiManagementDiagnostic.identifier(),
            ApiManagementLogger.identifier(),
            AppConfig.identifier(),
            AppInsights.identifier(),
            ResourceGroup.identifier(),
            Storage.identifier(),
            StorageContainer.identifier(),
            FunctionApp.identifier(),
            FunctionAppSlot.identifier(),
            ServicePlan.identifier(),
            ServiceBusNamespace.identifier(),
            ServiceBusQueue.identifier(),
            AppServicePlan.identifier(),
            AppService.identifier(),
            FunctionAppLinux.identifier(),
            Signalr.identifier(), 
            ContainerGroup.identifier(), 
            ContainerRegistry.identifier(),
            WindowsWebApp.identifier(),
            WindowsWebAppSlot.identifier(),
            CosmosAccount.identifier(),
            CosmosSqlContainer.identifier(),
            CosmosSqlDatabase.identifier(),
            AppServiceSlot.identifier(),
            NetworkSecurityGroup.identifier()
        ]

    @staticmethod
    def get_node(component: Component, group: str):
        """Create the azure diagram."""

        attrs = {
            "group": group,
            "fontsize": "8",
            "fixedsize": "true",
            "labelloc": "b",
            "width": "1",
            "height": "1.5",
            "imagepos": "tc",
            "imagescale": "true",
            "margin": "30.0,1.0"
        }

        if component.type == KeyVault.identifier():
            return KeyVault.get_node(component, **attrs)
        elif component.type == ApiManagement.identifier():
            attrs["height"] = "1.75"
            return ApiManagement.get_node(component, **attrs)
        elif component.type == ApiManagementDomain.identifier():
            attrs["height"] = "1.75"
            return ApiManagementDomain.get_node(
                component, **attrs)
        elif component.type == ApiManagementCertificate.identifier():
            attrs["height"] = "1.75"
            return ApiManagementCertificate.get_node(
                component, **attrs)
        elif component.type == ApiManagementDiagnostic.identifier():
            return ApiManagementDiagnostic.get_node(
                component, **attrs)
        elif component.type == ApiManagementLogger.identifier():
            return ApiManagementLogger.get_node(
                component, **attrs)
        elif component.type == Storage.identifier():
            attrs["height"] = "1.75"
            return Storage.get_node(component, **attrs)
        elif component.type == StorageContainer.identifier():
            return StorageContainer.get_node(component, **attrs)
        elif component.type == AppConfig.identifier():
            attrs["height"] = "1.75"
            return AppConfig.get_node(component, **attrs)
        elif component.type == ResourceGroup.identifier():
            return ResourceGroup.get_node(component, **attrs)
        elif component.type == AppInsights.identifier():
            attrs["height"] = "1.6"
            return AppInsights.get_node(component, **attrs)
        elif component.type == Subnet.identifier():
            attrs["height"] = "1.5"
            return Subnet.get_node(component, **attrs)
        elif component.type == FunctionApp.identifier():
            return FunctionApp.get_node(component, **attrs)
        elif component.type == FunctionAppLinux.identifier():
            return FunctionAppLinux.get_node(component, **attrs)
        elif component.type == FunctionAppSlot.identifier():
            return FunctionAppSlot.get_node(component, **attrs)
        elif component.type == ApiManagementApi.identifier():
            attrs["height"] = "1.75"
            return ApiManagementApi.get_node(component, **attrs)
        elif component.type == ServicePlan.identifier():
            attrs["height"] = "1.75"
            return ServicePlan.get_node(component, **attrs)
        elif component.type == ServiceBusNamespace.identifier():
            attrs["height"] = "1.8"
            return ServiceBusNamespace.get_node(component, **attrs)
        elif component.type == ServiceBusQueue.identifier():
            attrs["height"] = "1.8"
            return ServiceBusQueue.get_node(component, **attrs)
        elif component.type == AppServicePlan.identifier():
            attrs["height"] = "1.75"
            return AppServicePlan.get_node(component, **attrs)
        elif component.type == AppService.identifier():
            return AppService.get_node(component, **attrs)
        elif component.type == AppServiceSlot.identifier():
            return AppServiceSlot.get_node(component, **attrs)
        elif component.type == Signalr.identifier():
            return Signalr.get_node(component, **attrs)
        elif component.type == ContainerGroup.identifier():
            return ContainerGroup.get_node(component, **attrs)
        elif component.type == ContainerRegistry.identifier():
            return ContainerRegistry.get_node(component, **attrs)
        elif component.type == WindowsWebApp.identifier():
            return WindowsWebApp.get_node(component, **attrs)
        elif component.type == WindowsWebAppSlot.identifier():
            return WindowsWebAppSlot.get_node(component, **attrs)
        elif component.type == CosmosAccount.identifier():
            return CosmosAccount.get_node(component, **attrs)
        elif component.type == CosmosSqlContainer.identifier():
            return CosmosSqlContainer.get_node(component, **attrs)
        elif component.type == CosmosSqlDatabase.identifier():
            return CosmosSqlDatabase.get_node(component, **attrs)
        elif component.type == NetworkSecurityGroup.identifier():
            return NetworkSecurityGroup.get_node(component, **attrs)
        else:
            logging.warning(
                f"No resource icon for {component.type}: {component.name} is not yet supported")

    @staticmethod
    def nest_resources(components: List[Component]) -> List[Component]:
        """Group related azure resources together."""

        resource_groups = [
            x for x in components if x.type == ResourceGroup.identifier()]

        resources = [
            ApiManagement.group(components),
            AppInsights.group(components),
            ServicePlan.group(components),
            AppServicePlan.group(components),
            ServiceBusNamespace.group(components),
            CosmosAccount.group(components),
            Storage.group(components),
            [x for x in components if x.type == KeyVault.identifier()],
            [x for x in components if x.type == AppConfig.identifier()],
            [x for x in components if x.type == Subnet.identifier()],
            [x for x in components if x.type == Signalr.identifier()],
            [x for x in components if x.type == ContainerGroup.identifier()],
            [x for x in components if x.type == ContainerRegistry.identifier()],
            [x for x in components if x.type == NetworkSecurityGroup.identifier()]
        ]

        for resource_grouping in resources:
            resource_groups = ResourceGroup.group(
                resource_groups, resource_grouping)

        return resource_groups
