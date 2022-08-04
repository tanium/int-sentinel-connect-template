#!/usr/bin/env python3

import argparse
import os
import json
import random
import sys

# constants
STREAMS_KEY = "streams"
ROUTE_KEY = "route"

ARGUMENTS_KEY = "arguments"
ARGUMENTS_SHARED_KEY = "sharedKey"
ARGUMENTS_CUSTOMER_ID = "customerId"
ARGUMENTS_TABLE_NAME = "tableName"

NAME_KEY = "name"
VALUE_KEY = "value"

SCHEDULE_KEY = "schedule"
SCHEDULETZ_KEY = "scheduleTimeZone"
TZ = "UTC"

DEST_ROUTE = "/v1/destinations/loganalytics-destination"
EVENTS_ROUTE = "/v1/sources/events"


def perr(msg: str):
    """
    Simple wrapper for Error: str
    """
    print(f"Error: {msg}")


def validate_args(args: object) -> bool:
    """
    Returns True if the args object is valid. Otherwise returns False.
    """

    if args.c is None:
        perr("-c <customer id> is a required argument")
        return False

    if args.s is None:
        perr("-s <shared key> is a required argument")
        return False

    if args.f is None:
        perr("-f <file> is a required argument")
        return False

    if not os.path.exists(args.f):
        perr(f"Error: file not found: {args.f}")
        return False

    file_basename = os.path.basename(args.f)
    if not file_basename.endswith(".json.tmpl"):
        perr(
            f"File does not appear to be our json template (should end in .json.tmpl): {args.f}")
        return False

    new_filename = get_new_filename(args.f)
    if not os.path.exists(args.f):
        perr(
            f"File already exists: {new_filename}, did you mean to overwrite with -o?")
        return False

    return True


def read_connect_export(f: str) -> object:
    """
    Opens the json file and returns a dict of the data.
    """
    file_data = open(f)
    return json.load(file_data)


def get_new_filename(f: str) -> str:
    """
    Generates new modified filename.
    """
    return f.replace(".tmpl", "")


def output_new_connect_data(new_filename: str, connect_data: object):
    f = open(new_filename, 'w')
    f.write(json.dumps(connect_data, indent=2))


def build_cron_string() -> str:
    return f"00 {random.randint(12,15)} * * *"


def main(args: object):
    """
    Main entrypoint of program. Args should be an object that has following values:
    u -> URL of Sentinel Forwarder, can be IP or url.
    s -> Secret authorization token to use when communicating with sentinel forwarder.
    f -> Path of json file of connect exported jobs in a single file to be edited.
    """
    if not validate_args(args):
        sys.exit(1)

    connect_data = read_connect_export(args.f)

    for connection in connect_data:

        if STREAMS_KEY not in connection:
            continue

        if "Threat" not in connection[NAME_KEY]:
            connection[SCHEDULE_KEY] = build_cron_string()
            connection[SCHEDULETZ_KEY] = TZ

        for stream in connection[STREAMS_KEY]:
            if ROUTE_KEY not in stream:
                continue

            if stream[ROUTE_KEY] == DEST_ROUTE:
                if ARGUMENTS_KEY not in stream:
                    continue

                stream[ARGUMENTS_KEY][ARGUMENTS_SHARED_KEY] = args.s
                stream[ARGUMENTS_KEY][ARGUMENTS_CUSTOMER_ID] = args.c

    new_filename = get_new_filename(args.f)
    output_new_connect_data(new_filename, connect_data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Edit connection exports. Will take in a file and saved the new file as <original-filename>.parsed')

    parser.add_argument(
        '-c', type=str, help='Your Microsoft Log Analytics Workspace ID.')
    parser.add_argument(
        '-s', type=str, help='Your Microsoft Log Analytics Primary Key.')

    parser.add_argument(
        '-f', type=str, help='Path of json template file of connect exports to use.')

    main(parser.parse_args())
