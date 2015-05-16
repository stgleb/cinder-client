import argparse
import sys

from cinder_api import attach_volume
from cinder_api import create_volume
from cinder_api import delete_volume
from cinder_api import detach_volume
from cinderclient.v1 import client


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
    cinder_client = client.Client(arg_obj.username, arg_obj.password,
                                  arg_obj.tenant, arg_obj.auth_url,
                                  service_type="volume")
    vol_id = create_volume(cinder_client,
                           'test_vol', 1)

    attach_volume(cinder_client, volume_id=vol_id,
                  vm_id="6cdfe757-584c-4a9f-a356-bf2213167d7c")
    detach_volume(cinder_client, volume_id=vol_id)

    print delete_volume(cinder_client, volume_id=vol_id)


if __name__ == '__main__':
    main()
