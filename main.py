import argparse
import cinderclient.v1
import sys

from cinder_api import CinderClient


def parse_args(argv):
    parser = argparse.ArgumentParser(description=
                                     'Parse command line arguments')
    parser.add_argument('--username', type=str, help='username',
                        required=True)
    parser.add_argument('--password', type=str, help='username',
                        required=True)
    parser.add_argument('--tenant', type=str, help='username',
                        required=True)
    parser.add_argument('--auth_url', type=str, help='username',
                        required=True)

    return parser.parse_args(argv)


def main():
    arg_obj = parse_args(sys.argv[1:])
    client = cinderclient.v1.Client(arg_obj.username, arg_obj.password,
                                    arg_obj.tenant, arg_obj.auth_url,
                                    service_type="volume")

    cinder_client = CinderClient(client)
    vol_id = cinder_client.create_volume('test_vol2', size=1)

    cinder_client.attach_volume(volume_id=vol_id,
                                vm_id="6cdfe757-584c-4a9f-a356-bf2213167d7c")
    cinder_client.detach_volume(volume_id=vol_id)

    print(cinder_client.delete_volume(volume_id=vol_id))


if __name__ == '__main__':
    main()
