from app import mongo
from .model import Recipe
from pymongo import ReturnDocument
import pymongo
import datetime
from datetime import timedelta
from dateutil import tz
from exception import AbortException, NotFoundException
from_zone = tz.gettz('UTC')
to_zone = tz.gettz('Asia/Jakarta')


def generate_recipe(user_id):
    recipedb = mongo.db.recipes
    cnt = len(get_all_recipes())
    while recipedb.find_one({'queue_number': '{:03d}'.format(cnt)}):
        cnt += 1
    return create_recipe('{:03d}'.format(cnt), user_id)


def create_recipe(queue_number, user_id):
    recipedb = mongo.db.recipes
    recipedb.create_index([('queue_number', pymongo.TEXT)], unique=True)
    utc = datetime.datetime.now()
    utc = utc.replace(tzinfo=from_zone)
    date_now = utc.astimezone(to_zone)
    recipe_id = recipedb.insert({
        'queue_number': queue_number,
        'date_created': date_now,
        'date_update': date_now,
        'status': 1,
        'user_id': user_id})
    recipe = recipedb.find_one({'_id': recipe_id})
    recipe = Recipe(
        queue_number=recipe['queue_number'],
        status=recipe['status'],
        date_created=recipe['date_created'],
        date_update=recipe['date_update'],
        user_id=recipe['user_id']
    )
    return recipe


def update_recipe(queue_number, status, user_id):
    recipedb = mongo.db.recipes
    recipe = recipedb.find_one({'queue_number': queue_number})
    if not recipe:
        raise NotFoundException('recipe not found')
    utc = datetime.datetime.now()
    utc = utc.replace(tzinfo=from_zone)
    date_now = utc.astimezone(to_zone)

    recipe = recipedb.find_one_and_update(
        {'queue_number': queue_number},
        {'$set': {
            'status': status,
            'date_update': date_now,
            'user_id': user_id
        }},
        return_document=ReturnDocument.AFTER
    )

    recipe = Recipe(
        queue_number=recipe['queue_number'],
        status=recipe['status'],
        date_created=recipe['date_created'],
        date_update=recipe['date_update'],
        user_id=recipe['user_id']
    )
    return recipe


def delete_recipe(queue_number):
    recipedb = mongo.db.recipes
    recipe = recipedb.find_one({'queue_number': queue_number})
    if not recipe:
        raise NotFoundException('recipe not found')
    recipedb.delete_many({'_id': recipe['_id']})
    recipe = Recipe(
        queue_number=recipe['queue_number'],
        status=recipe['status'],
        date_created=recipe['date_created'],
        date_update=recipe['date_update'],
        user_id=recipe['user_id']
    )
    return recipe


def get_all_recipes():
    recipedb = mongo.db.recipes
    result = recipedb.find().sort([("status", -1)])
    recipes = []
    date_now = datetime.datetime.now()
    for recipe in list(result):
        # only show receipt above 1 days before
        date_before = date_now - timedelta(days=1)
        receipt_date = datetime.datetime.strptime(
            recipe['date_update'].strftime(
                "%H:%M:%S %d-%m-%Y"), '%H:%M:%S %d-%m-%Y')
        if (receipt_date < date_before):
            # delete receipt
            recipedb.delete_many({'_id': recipe['_id']})
            continue
        recipes.append(Recipe(
            queue_number=recipe['queue_number'],
            status=recipe['status'],
            date_created=recipe['date_created'].strftime(
                "%%d-%m-%Y H:%M:%S"),
            date_update=recipe['date_update'].strftime(
                "%d-%m-%Y %H:%M:%S"),
            user_id=recipe['user_id']
        ).to_json())
    return recipes


def get_recipe(queue_number):
    recipedb = mongo.db.recipes
    recipe = recipedb.find_one({'queue_number': queue_number})
    if not recipe:
        raise NotFoundException('recipe not found')
    recipe = Recipe(
        queue_number=recipe['queue_number'],
        status=recipe['status'],
        date_created=recipe['date_created'].strftime(
            "%H:%M:%S %d-%m-%Y"),
        date_update=recipe['date_update'].strftime(
            "%H:%M:%S %d-%m-%Y"),
        user_id=recipe['user_id']
    )
    return recipe
