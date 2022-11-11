"""Azure AppServicePlan resource."""

from abc import abstractmethod
from app.common.component import Component
from app.common.resource import Resource
from diagrams.azure import web
from typing import List, Dict
import logging

from app.azure.resources.azurerm_function_app import FunctionApp
from app.azure.resources.azurerm_function_app_slot import FunctionAppSlot
from app.azure.resources.azurerm_linux_function_app import FunctionAppLinux
from app.azure.resources.azurerm_windows_web_app import WindowsWebApp
from app.azure.resources.azurerm_windows_web_app_slot import WindowsWebAppSlot
from app.azure.resources.azurerm_app_service import AppService
from app.azure.resources.azurerm_app_service_slot import AppServiceSlot


class CommonServicePlan(Resource):
    """Base resource component."""

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
    def get_node(component: Component, **attrs: Dict):
        """Get the underlying diagrams type."""
        pass
    
    @staticmethod
    def group(identifier, components: List[Component]) -> List[Component]:
        """Handle service plan groupings."""
        function_apps = CommonServicePlan.__group_function_apps(components)
        windows_web_apps = CommonServicePlan.__group_web_apps(components)
        app_services = CommonServicePlan.__group_app_services(components)
        
        service_plans = [
            x for x in components if x.type.startswith(identifier)]

        for function_app in function_apps:
            service_plan_id = ""
            if "app_service_plan_id" in function_app.attributes:
                service_plan_id = function_app.attributes["app_service_plan_id"]
            else:
                service_plan_id = function_app.attributes["service_plan_id"]
                
            app_service_plan_name = service_plan_id.split("/")[-1]
            
            app_service_plan = next(filter(
                    lambda x: x.attributes["name"] == app_service_plan_name, service_plans), None)

            if app_service_plan == None:
                logging.info(f"No {identifier} found for {function_app.key}")
                continue

            app_service_plan.add_component(function_app)
            
        for windows_web_app in windows_web_apps:
            service_plan_id = ""
            if "app_service_plan_id" in windows_web_app.attributes:
                service_plan_id = windows_web_app.attributes["app_service_plan_id"]
            else:
                service_plan_id = windows_web_app.attributes["service_plan_id"]
                
            app_service_plan_name = service_plan_id.split("/")[-1]
            
            app_service_plan = next(filter(
                    lambda x: x.attributes["name"] == app_service_plan_name, service_plans), None)

            if app_service_plan == None:
                logging.info(f"No {identifier} found for {windows_web_app.key}")
                continue

            app_service_plan.add_component(windows_web_app)
            
        for app_service in app_services:
            service_plan_id = ""
            if "app_service_plan_id" in app_service.attributes:
                service_plan_id = app_service.attributes["app_service_plan_id"]
            else:
                service_plan_id = app_service.attributes["service_plan_id"]
                
            app_service_plan_name = service_plan_id.split("/")[-1]
            
            app_service_plan = next(filter(
                    lambda x: x.attributes["name"] == app_service_plan_name, service_plans), None)

            if app_service_plan == None:
                logging.info(f"No {identifier} found for {app_service.key}")
                continue

            app_service_plan.add_component(app_service)

        return service_plans
    
    
    @staticmethod
    def __group_web_apps(components: List[Component]) -> List[Component]:
        """Handle web app groupings."""
        windows_web_apps_all = [
            x for x in components if x.type.startswith(WindowsWebApp.identifier())]
        windows_web_apps = [
            x for x in windows_web_apps_all if x.type == WindowsWebApp.identifier()]
        windows_web_app_slots = [
            x for x in windows_web_apps_all if x.type == WindowsWebAppSlot.identifier()]

        for windows_web_app_slot in windows_web_app_slots:
            windows_web_app = None
            if "app_service_id" in windows_web_app_slot.attributes:
                windows_web_app = next(filter(
                    lambda x: x.attributes["id"] == windows_web_app_slot.attributes["app_service_id"], windows_web_apps), None)

            if windows_web_app == None:
                logging.info(
                    f"No parent for resource {windows_web_app_slot.type}: {windows_web_app_slot.name}")
                continue

            found = False
            for component in windows_web_app.get_components():
                if (component.key == windows_web_app_slot.key):
                    found = True
                    break
                
            if not found:
                windows_web_app.add_component(windows_web_app_slot)
            
        return windows_web_apps
    
    @staticmethod
    def __group_function_apps(components: List[Component]) -> List[Component]:
        """Handle function app groupings."""
        function_apps_all = [
            x for x in components if x.type.startswith(FunctionApp.identifier())]
        function_apps = [
            x for x in function_apps_all if x.type == FunctionApp.identifier()]
        function_app_slots = [
            x for x in function_apps_all if x.type == FunctionAppSlot.identifier()]

        for function_app_slot in function_app_slots:
            function_app = None
            if "function_app_name" in function_app_slot.attributes:
                function_app = next(filter(
                    lambda x: x.attributes["name"] == function_app_slot.attributes["function_app_name"], function_apps), None)

            if function_app == None:
                logging.info(
                    f"No parent for resource {function_app_slot.type}: {function_app_slot.name}")
                continue

            found = False
            for component in function_app.get_components():
                if (component.key == function_app_slot.key):
                    found = True
                    break
                
            if not found:
                function_app.add_component(function_app_slot)
            
        # handle linux ones too
        
        function_apps_linux = [
            x for x in components if x.type == FunctionAppLinux.identifier()]

        for function_app_linux in function_apps_linux:
            function_apps.append(function_app_linux)
            
        return function_apps   
     
    @staticmethod
    def __group_app_services(components: List[Component]) -> List[Component]:
        """Handle web app groupings."""
        app_services_all = [
            x for x in components if x.type.startswith(AppService.identifier())]
        app_services = [
            x for x in app_services_all if x.type == AppService.identifier()]
        app_service_slots = [
            x for x in app_services_all if x.type == AppServiceSlot.identifier()]

        for app_service_slot in app_service_slots:
            app_service = None
            if "app_service_id" in app_service_slot.attributes:
                app_service = next(filter(
                    lambda x: x.attributes["id"] == app_service_slot.attributes["app_service_id"], app_services), None)

            if app_service == None:
                logging.info(
                    f"No parent for resource {app_service_slot.type}: {app_service_slot.name}")
                continue

            found = False
            for component in app_service.get_components():
                if (component.key == app_service_slot.key):
                    found = True
                    break
                
            if not found:
                app_service.add_component(app_service_slot)
            
        return app_services
