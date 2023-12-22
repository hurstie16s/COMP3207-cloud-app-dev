#System Imports
import logging
# Azure Imports
## NONE
# Code base imports
from shared_code.Exceptions import NoContainerSpecifiedException, EmptyQueryException

def validate(container):
    # Ensure Container is specified
    if container is None:
        raise NoContainerSpecifiedException

def query_items(query, parameters=[], container=None):

    # Fault tolerance for development
    validate(container)
    
    logging.info("Query Database")
    #Run Query, return results as list
    return list(container.query_items(query=query, parameters=parameters, enable_cross_partition_query=True))

def create_item(data, container=None):

    # Fault tolerance for development
    validate(container)

    logging.info("Insert Data into Database")
    #Run insert
    container.create_item(data, enable_automatic_id_generation = True)
    return

def upsert_item(data, container=None):

    # Fault tolerance for development
    validate(container)

    logging.info("Update Data in Database")
    #Run update
    container.upsert_item(data)
    return

def delete_item(id, container=None):

    # Fault tolerance for development
    validate(container)

    logging.info("Delete Data from Database")
    #Run delete
    container.delete_item(item=id, partition_key=id)
    return