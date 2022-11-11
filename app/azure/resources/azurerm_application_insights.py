"""Azure AppInsights resource."""

from app.common.component import Component
from app.common.resource import Resource
from diagrams.azure import devops
from typing import List
import logging


class AppInsights(Resource):
    """Base resource component."""

    @staticmethod
    def identifier() -> str:
        """Get the identifier for this type in TF."""
        return "azurerm_application_insights"

    @staticmethod
    def get_metadata(component: Component) -> str:
        """Get the metadata string from this components attributes."""
        return f"Retention days: {component.attributes['retention_in_days']}"

    @staticmethod
    def get_node(component: Component, **attrs: dict):
        """Get the underlying diagrams type."""
        metadata = AppInsights.get_metadata(component)
        return devops.ApplicationInsights(Resource.get_name(component, metadata), **attrs)

    @staticmethod
    def group(components: List[Component]) -> List[Component]:
        """Handle app insights groupings."""
        app_insights_resources_all = [
            x for x in components if x.type.startswith(AppInsights.identifier())]
        app_insights_resources_top_level = [
            x for x in app_insights_resources_all if x.type == AppInsights.identifier()]
        app_insights_resources_sub_level = [
            x for x in app_insights_resources_all if not x.type == AppInsights.identifier()]

        for app_insights_sub in app_insights_resources_sub_level:
            app_insights = None
            if "source_id" in app_insights_sub.attributes:
                app_insights = next(filter(
                    lambda x: x.attributes["id"] == app_insights_sub.attributes["source_id"], app_insights_resources_top_level), None)

            if app_insights == None:
                logging.error(
                    f"No parent for resource {app_insights_sub.type}: {app_insights_sub.name}")
                continue

            app_insights.add_component(app_insights_sub)

        return app_insights_resources_top_level
