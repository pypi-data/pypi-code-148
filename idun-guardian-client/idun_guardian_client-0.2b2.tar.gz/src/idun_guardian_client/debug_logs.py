"""
This module contains the functions that are used to log the debug messages.
"""
import logging


def log_first_message(data_model, package_receipt, debug):
    if debug:
        logging.info("[API]: First package sent")
        logging.info(
            "[API]: data_model.stop = %s",
            data_model.stop,
        )
        logging.info(
            "[API]: data_model.device_id = %s",
            data_model.device_id,
        )
        logging.info(
            "[API]: data_model.recording_id = %s",
            data_model.recording_id,
        )
        logging.info(
            "[API]: First package receipt: %s",
            package_receipt,
        )


def log_final_message(data_model, package_receipt, debug):
    if debug:
        logging.info("[API]: Last package sent")
        logging.info(
            "[API]: data_model.stop = %s",
            data_model.stop,
        )
        logging.info(
            "[API]: data_model.device_id = %s",
            data_model.device_id,
        )
        logging.info(
            "[API]: data_model.recording_id = %s",
            data_model.recording_id,
        )
        logging.info(
            "[API]: Last package receipt: %s",
            package_receipt,
        )
        logging.info("[API]: Cloud connection sucesfully terminated")
        logging.info("[API]: Breaking inner loop of API client")


def logging_connection(websocket_resource_url, debug):
    if debug:
        logging.info(
            "[API]: Connected to websocket resource url: %s",
            websocket_resource_url,
        )
        logging.info("[API]: Sending data to the cloud")


def logging_break(debug):
    if debug:
        logging.info("[API]: Breaking API client while loop")


def logging_ping_error(error, retry_time, debug):
    if debug:
        logging.info("[API]: Ping interuption: %s", error)
        logging.info("[API]: Ping failed, connection closed")
        logging.info(
            "[API]: Trying to reconnect in %s seconds",
            retry_time,
        )


def logging_not_empty(debug: bool) -> None:
    """Log the queue is not empty."""
    if debug:
        logging.info("[API]: Data queue is not empty, waiting for last timestamp")


def log_interrupt_error(error, debug):
    if debug:
        logging.info(
            "[API]: Interuption in sending data to the cloud: %s",
            error,
        )


def logging_connection_closed(debug):
    if debug:
        logging.info("[API]: ws client connection closed or asyncio Timeout")


def logging_reconnection(debug):
    if debug:
        logging.info("[API]: Ping successful, connection alive and continue..")
        logging.info("Try to ping websocket successful")


def logging_empty(debug):
    if debug:
        logging.info("[API]: Device queue is empty, sending computer time")


def logging_cloud_termination(debug):
    if debug:
        logging.info("[API]: Terminating cloud connection")


def logging_gaieerror(error, retry_time, debug):
    if debug:
        logging.info("[API]: Interruption in connecting to the cloud: %s", error)
        logging.info("[API]: Retrying connection in %s sec ", retry_time)


def logging_connection_refused(error, retry_time, debug):
    if debug:
        logging.info("[API]: Interruption in connecting to the cloud: %s", error)
        logging.info(
            "Cannot connect to API endpoint. Please check the URL and try again."
        )
        logging.info("Retrying connection in {} seconds".format(retry_time))


def logging_cancelled_error(error, debug):
    if debug:
        logging.info(
            "[API]: Error in sending data to the cloud: %s",
            error,
        )
        logging.info("[API]: Re-establishing cloud connection in exeption")
        logging.info("[API]: Fetching last package from queue")


def logging_connecting_to_cloud(debug):
    if debug:
        logging.info("[API]: Connecting to cloud...")


def logging_api_completed(debug):
    if debug:
        logging.info("[API]: -----------  API client is COMPLETED ----------- ")
