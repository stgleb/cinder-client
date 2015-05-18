import unittest
from cinder_api import CinderClient

from cinderclient.v1 import Client


class TestCinderClientOpenstack(unittest.TestCase):
    def setUpClass(cls):
        username = "admin"
        password = "admin"
        tenant = "admin"
        auth_url = "http://172.16.55.130:5000/v2.0/"

        cinder = Client(username, password,
                        tenant, auth_url,
                        service_type="volume")
        cls.client = CinderClient(cinder)

    def test_create_delete(self):
        vol_id = self.client.create_volume('test_volume', size=1)
        assert len(vol_id) == 36


    def test_delete(self):
        pass

    def test_attach_detach(self):
        pass

    def test_find_vm(self):
        pass
