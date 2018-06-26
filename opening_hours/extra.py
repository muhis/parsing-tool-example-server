import random
import sys
import time
from hashlib import md5
from typing import Dict

import simplejson
from parsing_tools import parse

HOURS_IN_DAY = [number for number in range(24)]


def generate_new_json():
    json_load = simplejson.loads('''
    {"monday": [],
    "tuesday": [
        {
            "type": "open",
            "value": 36000
        },
        {
            "type": "close",
            "value": 64800
        }]}
        ''')
    for _, periods in json_load.items():
        for period in periods:
            period['value'] = random.choice(HOURS_IN_DAY)

    return simplejson.dumps(json_load)


def test_parser(json_value):
    start = time.time()
    dic = simplejson.loads(json_value)
    parse(dic)
    end = time.time()
    return (end - start)

in_memory_db = {}  # type: Dict


def test_cache(json_value):
    start = time.time()
    if json_value not in in_memory_db:
        dic = simplejson.loads(json_value)
        parsed = parse(dic)
        in_memory_db.update(
            {json_value: parsed}
        )
    end = time.time()
    return (end - start)


def full_test(repet):
    """
    Run this with an integer, the speed depends on your computer.
    """
    in_memory_db.clear()
    parse_result = 0
    cache_result = 0
    for number in range(repet):
        new_json = generate_new_json()
        temp_parse = test_parser(new_json)
        temp_dict = test_cache(new_json)
        parse_result += temp_parse
        cache_result += temp_dict
        if number % 1000 == 0:
            print(
                f"cache result: {temp_dict}, parse result: ",
                f"{temp_parse}, diff: {temp_parse - temp_dict}, ",
                f"db size: {len(in_memory_db)}")
    db_as_json = simplejson.dumps(in_memory_db)
    db_size = sys.getsizeof(db_as_json)
    result = (
        f"Final results: dict result: {cache_result}second, "
        f"parse result: {parse_result}second, "
        f"summation of time diffs: {cache_result - parse_result}second, "
        f"db length: {len(in_memory_db)} item and db size:{db_size}byte"
    )
    print(result)
