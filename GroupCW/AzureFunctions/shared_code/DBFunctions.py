#System Imports
import logging
import os
#Azure Imports
from azure.cosmos import CosmosClient

#Set up connections to CosmosDB
DB = CosmosClient(os.environ['URL'], os.environ['KEY'])
DBProxy = DB.get_database_client(os.environ['Database'])

def query_items(query, container):
    logging.info("Query Database")
    #Run Query, return results as list
    return list(container.query_items(query=query,enable_cross_partition_query=True))

def create_item(data, container):
    logging.info("Insert Data into Database")
    #Run insert
    container.create_item(data, enable_automatic_id_generation = True)
    return

def upsert_item(data, container):
    logging.info("Update Data in Database")
    #Run update
    container.upsert_item(data)
    return

def delete_item(id, container):
    logging.info("Delete Data from Database")
    #Run delete
    container.delete_item(item=id, partition_key=id)
    return