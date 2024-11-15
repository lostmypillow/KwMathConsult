"""
FastAPI module for processing card registrations through device interactions.

This module defines a FastAPI application with a route that handles card processing.
It allows cardholders (either students or teachers) to be registered on a device 
based on the card scanned. The module uses `Device` and `Cardholder` classes to manage 
the registration process.

Dependencies:
    - FastAPI: A modern web framework for building APIs.
    - Cardholder: Class for managing cardholder information.
    - Device: Class for handling device interactions.

Routes:
    GET /{device_id}/{card_id}:
        Processes a card registration request by initializing a `Device` and a `Cardholder` object 
        and invoking the `register` method to complete the process.
        Returns a success message or an error message if the process fails.
"""

from fastapi import FastAPI
from .cardholder import Cardholder
from .device import Device
app = FastAPI()


@app.get('/{device_id}/{card_id}')
def process_card(card_id: str, device_id: int) -> str:
    """
    Processes a card registration request for a given device and cardholder.

    This route is triggered when a card is scanned, and it will attempt to register the cardholder 
    on the specified device. The function initializes the `Device` and `Cardholder` objects and 
    calls the `register` method of `Device` to complete the registration process. 

    Args:
        card_id (str): The unique identifier for the cardholder (either student or teacher).
        device_id (int): The unique identifier for the device where the registration is being processed.

    Returns:
        dict: A response dictionary containing a success message or an error message.
              Example: 
                - Success: {'message': 'John Doe學生 刷卡成功'}
                - Failure: {'message': '刷卡失敗'}

    Raises:
        Exception: If there is any issue in processing the registration, an exception is raised and 
                  an error message is returned.
    """
    try:
        device = Device(device_id)  # Initialize Device
        cardholder = Cardholder(card_id)  # Initialize Cardholder
        output = device.register(cardholder)  # Call register method
        return {"message": output}  # Return the output from register
    except Exception as e:
        print(str(e))
        return {"message": "刷卡失敗"}  # Handle exceptions


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}
