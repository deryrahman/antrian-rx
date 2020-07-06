from datetime import datetime
from app import mongo
from dateutil import tz
from exception import NotFoundException
from .model import Counter
import pymongo
import mmap
import os

MMAP_PATH = './counter/tmp'


def is_unique(addr):
    lines = []
    with open(MMAP_PATH, "r") as f:
        lines = f.read().splitlines()

    today = datetime.now(tz.gettz('Asia/Jakarta')).strftime('%Y-%m-%d')

    if len(lines) == 0 or lines[0] != today:
        lines = [today]

    is_exist = addr in lines[1:]
    if not is_exist:
        lines.append(addr)

    with open(MMAP_PATH, "w") as f:
        f.write('\n'.join(lines))

    return is_exist


def hit():
    today = datetime.now(tz.gettz('Asia/Jakarta')).strftime('%Y-%m-%d')
    counter_repo = mongo.db.counters
    counter = counter_repo.find_one_and_update({'date': today}, {'$inc': {
                                               'count': 1}}, upsert=True, return_document=pymongo.ReturnDocument.AFTER)


def get_count(date):
    counter_repo = mongo.db.counters
    counter = counter_repo.find_one({'date': date})
    count = 0
    if counter:
        count = counter['count']

    return Counter(
        date=date,
        count=count
    )
