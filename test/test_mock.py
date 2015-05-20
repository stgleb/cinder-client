import unittest
from mock import MagicMock, patch
from cinder_api import CinderClient
from test.fakes import FakeVolume, FakeServer


class TestCinderClientMock(unittest.TestCase):
    """
        Testing CinderClient with mock object.
    """

    def test_create_volume(self):
        cinder = MagicMock()
        cinder.volumes.create.return_value = FakeVolume()
        client = CinderClient(cinder)
        assert "1234" == client.create_volume("foo", 1)

    def test_delete_volume(self):
        cinder = MagicMock()
        cinder.volumes.list.return_value = [FakeVolume()]
        client = CinderClient(cinder)
        assert ["1234"] == client.delete_volume("test")

    def test_find_volume(self):
        cinder = MagicMock()
        cinder.volumes.list.return_value = [FakeVolume(name="hello"),
                                            FakeVolume("world")]
        client = CinderClient(cinder)
        assert 1 == len(client.find_volume("hello"))

    def test_attach_volume_success(self):
        cinder = MagicMock()
        cinder.volumes.list.return_value = [FakeVolume(name="hello"),
                                            FakeVolume(name="world")]
        cinder.volumes.attach.return_value = 202

        servers = [FakeServer(name="server1"),
                   FakeServer(name="server2"),
                   FakeServer(id="4321")]

        servers = servers[:1]
        with patch.object(CinderClient, 'find_vm', return_value=servers):
            client = CinderClient(cinder)
            response = client.attach_volume(volume_name="hello", vm_name="server1")
            assert response == 202

    def test_attach_volume_failed(self):
        cinder = MagicMock()
        cinder.volumes.list.return_value = [FakeVolume(name="hello"),
                                            FakeVolume(name="world")]
        cinder.volumes.attach.return_value = 202

        servers = [FakeServer(name="server1"),
                   FakeServer(name="server2"),
                   FakeServer(id="4321")]

        with patch.object(CinderClient, 'find_vm', return_value=servers):
            client = CinderClient(cinder)
            self.assertRaises(Exception,
                              client.attach_volume, volume_name="hello",
                              vm_name="server1")

    def test_detach_volume(self):
        cinder = MagicMock()
        cinder.volumes.list.return_value = [FakeVolume(name="hello"),
                                            FakeVolume(name="world")]

        servers = [FakeServer(name="server1"),
                              FakeServer(name="server2"),
                              FakeServer(id="4321")]

        servers = servers[:1]
        with patch.object(CinderClient, 'find_vm', return_value=servers):
            client = CinderClient(cinder)
            response = client.detach_volume(volume_name="hello")
            assert response == [202]

    def test_find_vm(self):
        cinder = MagicMock()
        nova = MagicMock()
        nova.servers.list.return_value = [FakeServer(name="server1"),
                                          FakeServer(name="server2"),
                                          FakeServer(id="4321")]
        client = CinderClient(cinder)
        assert 1 == len(client._find_vm(nova, vm_name="server2"))
        assert 1 == len(client._find_vm(nova, vm_id="4321"))

if __name__ == '__main__':
    unittest.main()

