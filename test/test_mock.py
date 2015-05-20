import unittest

from cinder_client_api.cinder_api import CinderClient
from cinder_client_api.cinder_api_exceptions import MultipleServersFound
from mock import Mock
from mock import patch
from test.fakes import FakeServer
from test.fakes import FakeVolume


class TestCinderClientMock(unittest.TestCase):
    def test_create_volume(self):
        cinder = Mock()
        cinder.volumes.create.return_value = FakeVolume()
        client = CinderClient(cinder)
        self.assertEqual("1234", client.create_volume("foo", 1))

    def test_delete_volume(self):
        cinder = Mock()
        cinder.volumes.list.return_value = [FakeVolume()]
        client = CinderClient(cinder)
        assert ["1234"] == client.delete_volume("test")

    def test_find_volume(self):
        cinder = Mock()
        cinder.volumes.list.return_value = [FakeVolume(name="hello"),
                                            FakeVolume("world")]
        client = CinderClient(cinder)
        self.assertEqual(1, len(client.find_volume("hello")))

    def test_attach_volume_success(self):
        cinder = Mock()
        cinder.volumes.list.return_value = [FakeVolume(name="hello"),
                                            FakeVolume(name="world")]
        cinder.volumes.attach.return_value = 202

        servers = [FakeServer(name="server1"),
                   FakeServer(name="server2"),
                   FakeServer(id="4321")]

        servers = servers[:1]
        with patch.object(CinderClient, '_find_vm', return_value=servers):
            client = CinderClient(cinder)
            response = client.attach_volume(volume_name="hello",
                                            vm_name="server1")
        self.assertEqual(response, 202)

    def test_attach_volume_failed(self):
        cinder = Mock()
        cinder.volumes.list.return_value = [FakeVolume(name="hello"),
                                            FakeVolume(name="world")]
        cinder.volumes.attach.return_value = 202

        servers = [FakeServer(name="server1"),
                   FakeServer(name="server2"),
                   FakeServer(id="4321")]

        with patch.object(CinderClient, '_find_vm', return_value=servers):
            client = CinderClient(cinder)
            self.assertRaises(MultipleServersFound,
                              client.attach_volume, volume_name="hello",
                              vm_name="server1")

    def test_detach_volume(self):
        cinder = Mock()
        cinder.volumes.list.return_value = [FakeVolume(name="hello"),
                                            FakeVolume(name="world")]

        servers = [FakeServer(name="server1"),
                   FakeServer(name="server2"),
                   FakeServer(id="4321")]

        servers = servers[:1]
        with patch.object(CinderClient, '_find_vm', return_value=servers):
            client = CinderClient(cinder)
            response = client.detach_volume(volume_name="hello")
            self.assertEqual(response, [202])

    def test_find_vm(self):
        cinder = Mock()
        nova = Mock()
        nova.servers.list.return_value = [FakeServer(name="server1"),
                                          FakeServer(name="server2"),
                                          FakeServer(id="4321")]
        client = CinderClient(cinder)
        self.assertEqual(1, len(client._find_vm(nova, vm_name="server2")))
        self.assertEqual(1, len(client._find_vm(nova, vm_id="4321")))

if __name__ == '__main__':
    unittest.main()
