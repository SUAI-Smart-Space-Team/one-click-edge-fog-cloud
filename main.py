"""
 Copyright (c) 2021 Dell Inc, or its subsidiaries.
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at
      http://www.apache.org/licenses/LICENSE-2.0
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

from src.director import *
import argparse

if __name__ == "__main__":
    """Invokes the functions of the director. 
    The argparse library is used to parse arguments. 
    Fatal exceptions are also handled here. """

    parser = argparse.ArgumentParser(
        description='Manage Fog infrastructure. \n',
        formatter_class=argparse.HelpFormatter)

    parser.add_argument("-v", "--version", action='version',
                        version='IAAC-FOG v0.1')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-j", "--json", action="store", type=str,
                       help="The path to the json configuration file (may not be used with -e)")
    group.add_argument("-e", "--env", action="store_true",
                       help="Choose environment variables for input of configuration (may not be used with -j)")

    subparsers = parser.add_subparsers(help='Choose module')
    # create the parser for the "ovirt" command
    parser_ovirt = subparsers.add_parser('ovirt', help='ovirt module')
    ovirt_group = parser_ovirt.add_mutually_exclusive_group(required=True)
    ovirt_group.add_argument("--setup", dest='action', action='store_const', const="ovirt_setup",
                             help="Setup oVirt")
    ovirt_group.add_argument("--cleanup", dest='action', action='store_const', const="ovirt_cleanup",
                             help="Cleanup oVirt")
    ovirt_group.add_argument("--template", dest='action', action='store_const', const="ovirt_template",
                             help="Add templates to oVirt listed in the input configuration")

    # create the parser for the "terraform" command
    parser_terraform = subparsers.add_parser('terraform', help='terraform module')
    terraform_group = parser_terraform.add_mutually_exclusive_group(required=True)
    terraform_group.add_argument("--setup", dest='action', action='store_const', const="terraform_setup",
                                 help="Setup Terraform")
    terraform_group.add_argument("--cleanup", dest='action', action='store_const', const="terraform_cleanup",
                                 help="Cleanup Terraform")
    terraform_group.add_argument("--create_vm", dest='action', action='store_const', const="terraform_create_vm",
                                 help="Create VMs listed in the input configuration")

    # create the parser for the "infra" command
    parser_infra = subparsers.add_parser('infra', help='infra module include all above')
    infra_group = parser_infra.add_mutually_exclusive_group(required=True)
    infra_group.add_argument("--setup", dest='action', action='store_const', const="infra_setup",
                             help="Setup whole infrastructure")
    infra_group.add_argument("--cleanup", dest='action', action='store_const', const="infra_cleanup",
                             help="Cleanup whole infrastructure")

    args = parser.parse_args()

    if args.env:
        configurator = ENVConfigurator()
    elif args.json:
        configurator = JSONConfigurator(path_to_json_file=args.json)

    director = Director(configurator)

    try:
        # Choose action
        if args.action == "ovirt_setup":
            director.ovirt_product_setup()
        elif args.action == "ovirt_cleanup":
            director.ovirt_product_cleanup()
        elif args.action == "ovirt_template":
            director.ovirt_product_add_template()
        elif args.action == "terraform_setup":
            director.terraform_product_setup()
        elif args.action == "terraform_cleanup":
            director.terraform_product_cleanup()
        elif args.action == "terraform_create_vm":
            director.terraform_apply_vm_template()
        elif args.action == "infra_setup":
            director.fog_infra_setup()
        elif args.action == "infra_cleanup":
            director.fog_infra_cleanup()

    except (ConfiguratorKeyError, ValidationValueError, VMStatusError,
            TerraformAppError, AnsibleException) as error:
        logger.error('Fatal error: ' + repr(error))
        exit(-1)
