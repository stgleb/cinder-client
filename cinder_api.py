from novaclient.v1_1 import client as novaclient


def create_volume(client, name, size=1):
    """Function for creating cinder volume with specified size

        :param name : name of new volume
        :param size : size of volume in GB.]
        :rtype : volume id
    """
    new_volume = client.volumes.create(display_name=name, size=size)

    return new_volume.id


def find_volume(client, volume_name):
    """Function for searching volume by it's name

        :param volume_name : name volume
        :rtype : list of volume id which have appropriate name
    """
    volumes = client.volumes.list()

    return [v.id for v in volumes if v.display_name == volume_name]


def attach_volume(client, volume_name=None, volume_id=None,
                  vm_name=None, vm_id=None, mount_point="/dev/vda"):
    """Function for attaching particular volume to server.

        :param volume_name : name of volume
        :param volume_id : id of volume
        :param vm_name : name of server
        :param vm_id : id of server
    """

    vms = find_vm(client, vm_name, vm_id)

    if len(vms) > 1:
        raise Exception('Multiple servers found, '
                        'please specify vm_id')
    elif len(vms) == 0:
        raise Exception('No servers found')

    volumes = client.volumes.list()

    if volume_name:
        volumes = filter(lambda v: v.display_name == volume_name, volumes)

    if volume_id:
        volumes = filter(lambda v: v.id == volume_id, volumes)

    if len(volumes) > 1:
        raise Exception('Multiple volumes found, '
                        'please specify volume_id')
    elif len(volumes) == 0:
        raise Exception('No volumes found')

    client.volumes.attach(volumes[0], vms[0].id, mount_point)


def detach_volume(client, volume_name=None, volume_id=None):
    """Function for attaching particular volume from server.

        :param volume_name : name of volume
        :param volume_id : id of volume
    """
    volumes = client.volumes.list()

    if volume_name:
        volumes = filter(lambda v: v.display_name == volume_name, volumes)

    if volume_id:
        volumes = filter(lambda v: v.id == volume_id, volumes)

    [v.detach() for v in volumes]


def delete_volume(client, volume_name=None, volume_id=None):
    """Function for deleting volume by name or id.

        :param volume_name : name of volume
        :param volume_id : id of volume
        :rtype list of volume ids that were deleted.
    """
    volumes = client.volumes.list()

    if volume_id:
        volumes = filter(lambda v: v.id == volume_id, volumes)
    else:
        volumes = filter(lambda v: v.display_name == volume_name, volumes)

    [v.delete() for v in volumes]
    return [v.id for v in volumes]


def format_volume(client, vm_name):
    pass


def find_vm(client, vm_name, vm_id=None):
    """Function for searching servers by name or id.

        :param vm_name : name of server
        :param vm_id : id of server
    """
    nova = novaclient.Client(
        client.client.user,
        client.client.password,
        client.client.projectid,
        client.client.auth_url)

    if vm_id is None:
        return [server for server in nova.servers.list()
                if vm_name == server.name]
    else:
        return [server for server in nova.servers.list()
                if vm_id == server.id]
