# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------


import datetime
import decimal
import uuid
from typing import Callable

from dateutil import parser as date_parser  # noqa

from ossdbtoolsservice.parsers import mysql_datatypes, pg_datatypes
from ossdbtoolsservice.utils.constants import (MYSQL_PROVIDER_NAME,
                                               PG_PROVIDER_NAME)

VALID_TRUE_VALUES = ['true', 't', 'y', 'yes', '1']
VALID_FALSE_VALUES = ['false', 'f', 'n', 'no', '0']


def parse_bool(value: str) -> bool:
    bool_val = value.lower()

    if bool_val in VALID_TRUE_VALUES:
        return True
    elif bool_val in VALID_FALSE_VALUES:
        return False
    else:
        raise ValueError()


def parse_float(value: str) -> float:
    return float(value)


def parse_int(value: str) -> int:
    return int(value)


def parse_decimal(value: str) -> decimal.Decimal:
    return decimal.Decimal(value)


def parse_str(value: str) -> str:
    return value


def parse_char(value: str) -> str:
    if len(value) > 1:
        raise ValueError('Value provided is not a character')
    return value


def parse_date(value: str) -> datetime.date:
    date: datetime.datetime = date_parser.parse(value)
    return date.date()


def parse_time(value: str) -> datetime.time:
    date: datetime.datetime = date_parser.parse(value)
    return date.time()


def parse_time_with_timezone(value: str) -> datetime.time:
    date: datetime.datetime = date_parser.parse(value)
    return date.timetz()


def parse_datetime(value: str) -> datetime.datetime:
    if value == 'now()':
        return datetime.datetime.now()
    return date_parser.parse(value)


def parse_timedelta(value: str) -> datetime.timedelta:
    raise NotImplementedError()


def parse_uuid(value: str) -> uuid.UUID:
    return uuid.UUID(value)


PG_DATATYPE_PARSER_MAP = {
    pg_datatypes.DATATYPE_BOOL: parse_bool,
    pg_datatypes.DATATYPE_REAL: parse_float,
    pg_datatypes.DATATYPE_DOUBLE: parse_float,
    pg_datatypes.DATATYPE_SMALLINT: parse_int,
    pg_datatypes.DATATYPE_INTEGER: parse_int,
    pg_datatypes.DATATYPE_BIGINT: parse_int,
    pg_datatypes.DATATYPE_NUMERIC: parse_decimal,
    pg_datatypes.DATATYPE_CHAR: parse_char,
    pg_datatypes.DATATYPE_VARCHAR: parse_str,
    pg_datatypes.DATATYPE_TEXT: parse_str,
    pg_datatypes.DATATYPE_DATE: parse_date,
    pg_datatypes.DATATYPE_TIME: parse_time,
    pg_datatypes.DATATYPE_TIME_WITH_TIMEZONE: parse_time_with_timezone,
    pg_datatypes.DATATYPE_TIMESTAMP: parse_datetime,
    pg_datatypes.DATATYPE_TIMESTAMP_WITH_TIMEZONE: parse_datetime,
    pg_datatypes.DATATYPE_INTERVAL: parse_timedelta,
    pg_datatypes.DATATYPE_UUID: parse_uuid,
    pg_datatypes.DATATYPE_NAME: parse_str
}

MYSQL_DATATYPE_PARSER_MAP = {
    mysql_datatypes.DATATYPE_FLOAT: parse_float,
    mysql_datatypes.DATATYPE_DOUBLE: parse_float,
    mysql_datatypes.DATATYPE_TINYINT: parse_int,
    mysql_datatypes.DATATYPE_SMALLINT: parse_int,
    mysql_datatypes.DATATYPE_MEDIUMINT: parse_int,
    mysql_datatypes.DATATYPE_INTEGER: parse_int,
    mysql_datatypes.DATATYPE_BIGINT: parse_int,
    mysql_datatypes.DATATYPE_DECIMAL: parse_decimal,
    mysql_datatypes.DATATYPE_NUMERIC: parse_decimal,
    mysql_datatypes.DATATYPE_CHAR: parse_char,
    mysql_datatypes.DATATYPE_VARCHAR: parse_str,
    mysql_datatypes.DATATYPE_TEXT: parse_str,
    mysql_datatypes.DATATYPE_DATE: parse_date,
    mysql_datatypes.DATATYPE_TIME: parse_time,
    mysql_datatypes.DATATYPE_TIMESTAMP: parse_datetime,
    mysql_datatypes.DATATYPE_DATETIME: parse_datetime
}

def get_parser(column_data_type: str, provider_name: str) -> Callable[[str], object]:
    '''
    Returns a parser for the column_data_type provided. If not found returns None
    '''
    if provider_name == PG_PROVIDER_NAME:
        return PG_DATATYPE_PARSER_MAP.get(column_data_type.lower())
    elif provider_name == MYSQL_PROVIDER_NAME:
        return MYSQL_DATATYPE_PARSER_MAP.get(column_data_type.lower())
