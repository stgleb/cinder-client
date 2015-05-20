import cinder_api
import cinderclient.v1 as cinderclient
import novaclient.v2.client as novaclient
import time
import unittest


class TestCinderClientOpenstack(unittest.TestCase):
    """Testing cinder api with specified Openstack cluster.
    """
    @classmethod
    def setUpClass(cls):
        """Create nova, cinder and CinderClient object.
        """
        username = "admin"
        password = "admin"
        tenant = "admin"
        auth_url = "http://172.16.55.130:5000/v2.0/"

        cinder = cinderclient.Client(username, password,
                                     tenant, auth_url,
                                     service_type="volume")
        cls.cinder_client = cinder
        cls.cinder = cinder_api.CinderClient(cinder)
        cls.nova = novaclient.Client(username,
                                     password,
                                     tenant,
                                     auth_url)

    def test_create_delete(self):
        """Create volume, ensure is okay and delete volume.
        """
        vol_id = self.cinder.create_volume('test', size=1)
        self.assertEqual(len(vol_id), 36)
        res = self.cinder.delete_volume(volume_id=vol_id)
        self.assertEqual(res, [vol_id])

    def test_attach_detach(self):
        """Create volume and server. Attach, wait 10 sec
            and detach volume from server.
            Ensure status of volume is not in-use.
        """
        flavors = self.nova.flavors.list()
        images = self.nova.images.list()
        assert len(images) > 0
        image = images[0]
        flavor = flavors[0]
        server = self.nova.servers.create(name="test_server",
                                          image=image,
                                          flavor=flavor)
        time.sleep(10)
        volume = self.cinder_client.volumes.create(display_name=
                                                   "dummy",
                                                   size=1)
        time.sleep(5)
        self.cinder.attach_volume(volume_name=volume.display_name,
                                  vm_id=server.id, mount_point="/dev/vda")
        time.sleep(10)
        self.cinder.detach_volume(volume.display_name)
        time.sleep(10)
        self.assertEqual(volume.status, 'available')
        self.cinder_client.volumes.delete(volume=volume)
        server.delete()

if __name__ == '__main__':
    unittest.main()
