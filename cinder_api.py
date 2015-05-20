from novaclient.v2 import client as novaclient

import exceptions


class CinderClient(object):

    def __init__(self, cinder_client):
        self.client = cinder_client

    def create_volume(self, name, size=1):
        """Create cinder volume with specified size.

            :param name : name of new volume
            :param size : size of volume in GB.
            :return : volume id
        """
        new_volume = self.client.\
            volumes.create(display_name=name, size=size)

        return new_volume.id

    def find_volume(self, volume_name):
        """Search volume by its name.

            :param volume_name : name volume
            :return : list of volume id which have appropriate name
        """
        volumes = self.client.volumes.list()

        return [v.id for v in volumes if v.display_name == volume_name]

    def attach_volume(self, volume_name=None, volume_id=None,
                      vm_name=None, vm_id=None, mount_point="/dev/vda"):
        """Attach particular volume to server.

            :param volume_name : name of volume
            :param volume_id : id of volume
            :param vm_name : name of server
            :param vm_id : id of server
        """

        vms = self._find_vm(self._nova_client_from_cinder(),
                            vm_name, vm_id)

        if len(vms) > 1:
            raise exceptions.MultipleServersFound('Multiple servers found, '
                                                  'please specify vm_id')
        elif len(vms) == 0:
            raise exceptions.ServerNotFound('No servers found')

        volumes = self.client.volumes.list()

        if volume_name:
            volumes = filter(lambda v: v.display_name == volume_name, volumes)

        if volume_id:
            volumes = filter(lambda v: v.id == volume_id, volumes)

        if len(volumes) > 1:
            raise ('Multiple volumes found, '
                   'please specify volume_id')
        elif len(volumes) == 0:
            raise exceptions.VolumeNotFound('No volumes found')

        return self.client.volumes.attach(volumes[0], vms[0].id, mount_point)

    def detach_volume(self, volume_name=None, volume_id=None):
        """Detach particular volume from server.

            :param volume_name : name of volume
            :param volume_id : id of volume
        """
        volumes = self.client.volumes.list()

        if volume_name:
            volumes = filter(lambda v: v.display_name == volume_name, volumes)

        if volume_id:
            volumes = filter(lambda v: v.id == volume_id, volumes)

        return [v.detach() for v in volumes]

    def delete_volume(self, volume_name=None, volume_id=None):
        """Delete volume by name or id.

            :param volume_name : name of volume
            :param volume_id : id of volume
            :return list of volume ids that were deleted.
        """
        volumes = self.client.volumes.list()

        if volume_id and volume_name:
            raise ValueError("Too many arguments has been passed")

        if volume_id:
            volumes = filter(lambda v: v.id == volume_id, volumes)
        else:
            volumes = filter(lambda v: v.display_name == volume_name, volumes)

        [v.delete() for v in volumes]
        return [v.id for v in volumes]

    def _nova_client_from_cinder(self):
        nova = novaclient.Client(
            self.client.client.user,
            self.client.client.password,
            self.client.client.projectid,
            self.client.client.auth_url)

        return nova

    @staticmethod
    def _find_vm(nova,  vm_name=None, vm_id=None):
        """Search servers by name or id.

            :param vm_name : name of server
            :param vm_id : id of server
        """

        if vm_id is None:
            return [server for server in nova.servers.list()
                    if vm_name == server.name]
        else:
            return [server for server in nova.servers.list()
                    if vm_id == server.id]
