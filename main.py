# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os
import asyncio
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import MethodResponse
import RPi.GPIO as GPIO
import time

Relay_Ch1 = 26
Relay_Ch2 = 20
Relay_Ch3 = 21

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(Relay_Ch1, GPIO.OUT)
GPIO.setup(Relay_Ch2, GPIO.OUT)
GPIO.setup(Relay_Ch3, GPIO.OUT)


async def main():
    print("Start...")
    # The connection string for a device should never be stored in code. For the sake of simplicity we're using an environment variable here.
    conn_str = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")

    print("Set Default Relais Setup...")
    # Set default value for Relais 1
    GPIO.output(Relay_Ch1, GPIO.HIGH)

    # The client object is used to interact with your Azure IoT hub.
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    async def connect_iothub():
        try:
            # connect the client.
            await device_client.connect()
        except:
            print("Connect to IoT Hub... Retry")
            time.sleep(2)
            connect_iothub()

    print("Connect to IoT Hub...")
    await connect_iothub()

    # Define behavior for handling methods
    async def method_request_handler(method_request):
        # Determine how to respond to the method request based on the method name
        if method_request.name == "onAlarm":
            # set response payload
            payload = {"result": True}
            status = 200  # set return status code
            print("Executed onAlarm")
            GPIO.output(Relay_Ch1, GPIO.LOW)
            print("Relais Action ON\n")
            time.sleep(3)
            GPIO.output(Relay_Ch1, GPIO.HIGH)
            print("Relais Action OFF\n")
        elif method_request.name == "onHealthCheck":
            # set response payload
            payload = {"result": True}
            status = 200  # set return status code
        else:
            # set response payload
            payload = {"result": False, "data": "unknown method"}
            status = 400  # set return status code
            print("executed unknown method: " + method_request.name)

        # Send the response
        method_response = MethodResponse.create_from_method_request(
            method_request, status, payload)
        await device_client.send_method_response(method_response)

    # Set the method request handler on the client
    device_client.on_method_request_received = method_request_handler

    # Define behavior for halting the application
    def stdin_listener():
        while True:
            print("Nothing Received\n")
            time.sleep(500)

    # Run the stdin listener in the event loop
    loop = asyncio.get_running_loop()
    user_finished = loop.run_in_executor(None, stdin_listener)

    # Wait for user to indicate they are done listening for method calls
    await user_finished

    # Finally, shut down the client
    await device_client.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
