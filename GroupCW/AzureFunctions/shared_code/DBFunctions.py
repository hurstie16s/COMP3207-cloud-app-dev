#System Imports
import logging
import os
# Azure Imports
from azure.cosmos import CosmosClient
# Code base imports
from shared_code import NoContainerSpecifiedException

def query_items(query, parameters=[], container=None):

    # Ensures container is specified
    if container is None:
        raise NoContainerSpecifiedException
    
    logging.info("Query Database")
    #Run Query, return results as list
    return list(container.query_items(query=query, parameters=parameters, enable_cross_partition_query=True))

def create_item(data, container=None):

    # Ensures container is specified
    if container is None:
        raise NoContainerSpecifiedException

    logging.info("Insert Data into Database")
    #Run insert
    container.create_item(data, enable_automatic_id_generation = True)
    return

def upsert_item(data, container=None):

    # Ensures container is specified
    if container is None:
        raise NoContainerSpecifiedException

    logging.info("Update Data in Database")
    #Run update
    container.upsert_item(data)
    return

def delete_item(id, container=None):

    # Ensures container is specified
    if container is None:
        raise NoContainerSpecifiedException

    logging.info("Delete Data from Database")
    #Run delete
    container.delete_item(item=id, partition_key=id)
    return