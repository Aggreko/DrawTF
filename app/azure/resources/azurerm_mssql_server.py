"""Azure SqlServer resource."""

from app.common.component import Component
from app.common.resource import Resource
from diagrams.azure import database
from typing import Dict, List

from app.azure.resources.azurerm_mssql_database import SqlServerDatabase


class SqlServer(Resource):
    """Base resource component."""

    @staticmethod
    def identifier() -> str:
        """Get the identifier for this type in TF."""
        return "azurerm_mssql_server"

    @staticmethod
    def get_metadata(component: Component) -> str:
        """Get the metadata string from this components attributes."""
        if  "public_network_access_enabled" in component.attributes:
            public_network_access_enabled = component.attributes['public_network_access_enabled']
            return ", ".join([
                ('Public:' + str(public_network_access_enabled) + '')
            ])
        else:
            return ""

    @staticmethod
    def get_node(component: Component, **attrs: Dict):
        """Get the underlying diagrams type."""
        metadata = SqlServer.get_metadata(component)
        return database.SQLServers(Resource.get_name(component, metadata), **attrs)
       
    @staticmethod
    def group(components: List[Component]) -> List[Component]:
        """Handle service bus namespace groupings."""
        sql_servers = [
            x for x in components if x.type.startswith(SqlServer.identifier())]
        sql_databases = [
            x for x in components if x.type.startswith(SqlServerDatabase.identifier())]
        
        for sql_database in sql_databases:
            server_id = sql_database.attributes["server_id"]
            server_name = server_id.split("/")[-1]
                
            sql_server = next(filter(
                    lambda x: x.attributes["id"] == server_id, sql_servers), None)

            if sql_server == None:
                sql_server = Component(
                    server_name, SqlServer.identifier(), "data", sql_database.resource_group, {"name": server_name, "resource_group_name": sql_database.resource_group})
                sql_servers.append(sql_server)

            sql_server.add_component(sql_database)

        return sql_servers
