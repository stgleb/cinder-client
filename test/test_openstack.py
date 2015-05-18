import unittest
from cinder_api import CinderClient
from cinderclient.v1 import Client
from novaclient.v2 import client as novaclient


class TestCinderClientOpenstack(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        username = "admin"
        password = "admin"
        tenant = "admin"
        auth_url = "http://172.16.55.130:5000/v2.0/"

        cinder = Client(username, password,
                        tenant, auth_url,
                        service_type="volume")
        cls.cinder_client = cinder
        cls.cinder = CinderClient(cinder)
        cls.nova = novaclient.Client(username,
                                     password,
                                     tenant,
                                     auth_url)

    def test_create_delete(self):
        vol_id = self.cinder.create_volume('test_volume', size=1)
        assert len(vol_id) == 36
        res = self.cinder.delete_volume(volume_id=vol_id)
        assert res == [vol_id]
        pass

    def test_attach_detach(self):
        flavors = self.nova.flavors.list()
        images = self.nova.images.list()
        assert len(images) > 0
        image = images[0]
        flavor = flavors[0]
        server = self.nova.servers.create(name="test_server",
                                          image=image,
                                          flavor=flavor)
        volume = self.cinder_client.volumes.create(display_name="test_volume",
                                                   size=1)
        self.cinder.attach_volume(volume, server.id, "/dev/vda")
        self.cinder_client.volumes.delete(volume=volume)

    def test_find_vm(self):
        pass

if __name__ == '__main__':
    unittest.main()