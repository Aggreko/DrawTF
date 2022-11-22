"""Factory for doing common tasks around azure diagrams components"""
from typing import List
import logging

from app.common.component import Component
from app.azure.resources.azurerm_key_vault import KeyVault
from app.azure.resources.azurerm_api_management import ApiManagement
from app.azure.resources.azurerm_application_insights import AppInsights
from app.azure.resources.azurerm_subnet import Subnet
from app.azure.resources.azurerm_resource_group import ResourceGroup
from app.azure.resources.azurerm_storage_account import Storage
from app.azure.resources.azurerm_api_management_custom_domain import ApiManagementDomain
from app.azure.resources.azurerm_app_configuration import AppConfig
from app.azure.resources.azurerm_api_management_certificate import ApiManagementCertificate
from app.azure.resources.azurerm_api_management_diagnostic import ApiManagementDiagnostic
from app.azure.resources.azurerm_api_management_logger import ApiManagementLogger
from app.azure.resources.azurerm_function_app import FunctionApp
from app.azure.resources.azurerm_api_management_api import ApiManagementApi
from app.azure.resources.azurerm_service_plan import ServicePlan
from app.azure.resources.azurerm_function_app_slot import FunctionAppSlot
from app.azure.resources.azurerm_servicebus_namespace import ServiceBusNamespace
from app.azure.resources.azurerm_servicebus_queue import ServiceBusQueue
from app.azure.resources.azurerm_app_service import AppService
from app.azure.resources.azurerm_app_service_plan import AppServicePlan
from app.azure.resources.azurerm_linux_function_app import FunctionAppLinux
from app.azure.resources.azurerm_signalr_service import Signalr
from app.azure.resources.azurerm_container_group import ContainerGroup
from app.azure.resources.azurerm_container_registry import ContainerRegistry
from app.azure.resources.azurerm_windows_web_app import WindowsWebApp
from app.azure.resources.azurerm_cosmosdb_account import CosmosAccount
from app.azure.resources.azurerm_cosmosdb_sql_container import CosmosSqlContainer
from app.azure.resources.azurerm_cosmosdb_sql_database import CosmosSqlDatabase
from app.azure.resources.azurerm_windows_web_app_slot import WindowsWebAppSlot
from app.azure.resources.azurerm_app_service_slot import AppServiceSlot
from app.azure.resources.azurerm_storage_container import StorageContainer
from app.azure.resources.azurerm_network_security_group import NetworkSecurityGroup
from app.azure.resources.azurerm_servicebus_subscription import ServiceBusSubscription
from app.azure.resources.azurerm_servicebus_topic import ServiceBusTopic
from app.azure.resources.azurerm_mssql_database import SqlServerDatabase
from app.azure.resources.azurerm_mssql_server import SqlServer
from app.azure.resources.azurerm_log_analytics_workspace import LogAnalyticsWorkspace
from app.azure.resources.azurerm_databricks_workspace import DatabricksWorkspace
from app.azure.resources.databricks_azure_adls_gen2_mount import DatabricksGen2Mount
from app.azure.resources.databricks_cluster import DatabricksCluster
from app.azure.resources.azurerm_kubernetes_cluster import KubernetesCluster
from app.azure.resources.azurerm_logic_app_workflow import LogicApp
from app.common.resources.draw_custom import DrawCustom


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
            ServiceBusTopic.identifier(),
            ServiceBusSubscription.identifier(),
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
            NetworkSecurityGroup.identifier(),
            SqlServer.identifier(),
            SqlServerDatabase.identifier(),
            LogAnalyticsWorkspace.identifier(),
            DatabricksWorkspace.identifier(),
            DatabricksCluster.identifier(),
            DatabricksGen2Mount.identifier(),
            KubernetesCluster.identifier(),
            LogicApp.identifier(),
            DrawCustom.identifier()
        ]

    @staticmethod
    def get_node(component: Component, group: str):
        """Create the azure diagram."""

        attrs = {
            "group": group,
            "fontsize": "8",
            "fixedsize": "true",
            "labelloc": "b",
            "width": "1.2",
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
        elif component.type == ServiceBusTopic.identifier():
            attrs["height"] = "1.8"
            return ServiceBusTopic.get_node(component, **attrs)
        elif component.type == ServiceBusSubscription.identifier():
            attrs["height"] = "1.8"
            return ServiceBusSubscription.get_node(component, **attrs)
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
        elif component.type == SqlServer.identifier():
            attrs["height"] = "1.75"
            return SqlServer.get_node(component, **attrs)
        elif component.type == SqlServerDatabase.identifier():
            attrs["height"] = "1.75"
            return SqlServerDatabase.get_node(component, **attrs)
        elif component.type == LogAnalyticsWorkspace.identifier():
            attrs["height"] = "1.75"
            return LogAnalyticsWorkspace.get_node(component, **attrs)
        elif component.type == DatabricksWorkspace.identifier():
            attrs["height"] = "1.75"
            return DatabricksWorkspace.get_node(component, **attrs)
        elif component.type == DatabricksGen2Mount.identifier():
            attrs["height"] = "1.75"
            return DatabricksGen2Mount.get_node(component, **attrs)
        elif component.type == DatabricksCluster.identifier():
            attrs["height"] = "1.9"
            return DatabricksCluster.get_node(component, **attrs)
        elif component.type == KubernetesCluster.identifier():
            attrs["height"] = "1.8"
            return KubernetesCluster.get_node(component, **attrs)
        elif component.type == LogicApp.identifier():
            return LogicApp.get_node(component, **attrs)
        elif component.type == DrawCustom.identifier():
            return DrawCustom.get_node(component, **attrs)
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
            SqlServer.group(components),
            DatabricksWorkspace.group(components),
            [x for x in components if x.type == KeyVault.identifier()],
            [x for x in components if x.type == AppConfig.identifier()],
            [x for x in components if x.type == Subnet.identifier()],
            [x for x in components if x.type == Signalr.identifier()],
            [x for x in components if x.type == ContainerGroup.identifier()],
            [x for x in components if x.type == ContainerRegistry.identifier()],
            [x for x in components if x.type == NetworkSecurityGroup.identifier()],
            [x for x in components if x.type == LogAnalyticsWorkspace.identifier()],
            [x for x in components if x.type == KubernetesCluster.identifier()],
            [x for x in components if x.type == LogicApp.identifier()]
        ]

        for resource_grouping in resources:
            resource_groups = ResourceGroup.group(
                resource_groups, resource_grouping)

        customs = [x for x in components if x.type == DrawCustom.identifier()]
        
        return resource_groups + customs
