#!/usr/bin/env python3

import bottle
from bottle import request, response, route, post, get, run, template
import logging
import json


items = []
app = bottle.Bottle()


@app.get ('/')
def root ():
    return get_items()


@app.get ('/items')
def get_items ():
    log ('fetch all items, count: <{}>'.format (len (items)))

    return json.dumps ([
        dict (
            id    = i[0],
            key   = i[1].get ('key'),
            value = i[1].get ('value'),
        )
        for i in enumerate (items)
    ])


@app.post ('/items/<key>/<value>')
def post_item (key, value):
    item = dict (
        key   = key,
        value = value,
    )

    items.append (item)

    log ('create new item with id <{}>'.format (len (items) - 1))

    return bottle.HTTPResponse (
        body = json.dumps (item),
        status = 201,
    )


@app.put ('/item/<id>/<key>/<value>')
def put_item (id, key, value):
    id = int (id)

    if id >= len (items):
        raise (LookupError, 'no such id')

    log ('update item <{}>'.format (id))

    items[id] = dict (
        key   = key,
        value = value,
    )

    return bottle.HTTPResponse (status = 204)


@app.delete ('/item/<key>')
def delete_item_by_key (key):
    index = 0
    deleted = 0

    global items
    new_items = []

    for item in items:
        log ('[DEBUG] item: %s' % item.get('key'))
        if item.get ('key') == key:
            log ('delete item: key=<{}> at index=<{}>'.format (key, index))
            deleted += 1
        else:
            new_items.append (item)
        index += 1

    if deleted:
        log ('deleted {} items'.format (deleted))
        items = [i for i in new_items]
    else:
        log ('no such key <{}>'.format (key))

    return bottle.HTTPResponse (
        status = 200,
        body = json.dumps (dict (deleted = deleted)),
    )


@app.delete ('/items')
def delete_items ():
    global items # WTF?
    log ('delete all items, count: <{}>'.format (len (items)))

    items = []

    return bottle.HTTPResponse (status = 204)

### main ###

handler = logging.FileHandler ('./kvs.log')
handler.setFormatter (logging.Formatter (fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger = logging.getLogger ('kvs')
logger.addHandler (handler)
logger.setLevel (logging.INFO)
log = lambda msg: logger.info (msg)

if __name__ == '__main__':
    log ('ready ...')

    app.run (
        host = 'localhost',
        port = 8080,
    )

    log ('... bye')
