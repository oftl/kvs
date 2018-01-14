import unittest
from webtest import TestApp
import kvs
import json

class Test_KVS (unittest.TestCase):

    def test (self):
        app = TestApp (kvs.app)

        res = app.get ('http://localhost:8080/items',
            status = 200,
        )
        self.assertEqual (res.json_body, [])

        res = app.post ('http://localhost:8080/items/name/max',
            status = 201,
        )
        self.assertEqual (res.json_body, dict (key = 'name', value='max'))

        res = app.post ('http://localhost:8080/items/name/moritz',
            status = 201,
        )
        self.assertEqual (res.json_body, dict (key = 'name', value='moritz'))

        res = app.get ('http://localhost:8080/items',
            status = 200,
        )
        self.assertEqual (
            sorted_response (res.json_body),
            sorted_response ([
                dict (key = 'name', value = 'max'),
                dict (key = 'name', value = 'moritz'),
            ])
        )

        res = app.put ('http://localhost:8080/item/0/name/MAX',
            status = 204,
        )
        self.assertEqual (res.text, '')

        res = app.get ('http://localhost:8080/items',
            status = 200,
        )
        self.assertEqual (
            sorted_response (res.json_body),
            sorted_response ([
                dict (key = 'name', value = 'MAX'),
                dict (key = 'name', value = 'moritz'),
            ])
        )

        res = app.delete ('http://localhost:8080/item/age',
            status = 200,
        )
        self.assertEqual (res.json_body, dict (deleted = 0))

        res = app.delete ('http://localhost:8080/item/name',
            status = 200,
        )
        self.assertEqual (res.json_body, dict (deleted = 2))

        res = app.get ('http://localhost:8080/items',
            status = 200,
        )
        self.assertEqual (res.json_body, [])

        ###

        res = app.post ('http://localhost:8080/items/name/jim')
        res = app.post ('http://localhost:8080/items/name/garfield')
        res = app.post ('http://localhost:8080/items/name/odie')

        res = app.get ('http://localhost:8080/items',
            status = 200,
        )
        self.assertEqual (
            sorted_response (res.json_body),
            sorted_response ([
                dict (key = 'name', value = 'jim'),
                dict (key = 'name', value = 'garfield'),
                dict (key = 'name', value = 'odie'),
            ])
        )

        res = app.delete ('http://localhost:8080/items',
            status = 204,
        )
        self.assertEqual (res.text, '')

        #  res = app.get ('http://localhost:8080/items',
        #      status = 200,
        #  )
        #  self.assertEqual (res.json_body, [])

def sorted_response (res):
    return [ dict (
        key   = item.get ('key'),
        value = item.get ('value'),
      )
      for item in sorted (
          res,
          key = lambda i: i.get ('key')
      )
    ]


if __name__ == '__main__':
    unittest.main()
