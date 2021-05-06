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



from __future__ import annotations

from src.builder.ovirt_builder import *
from src.builder.terraform_builder import *
from src.configurator.json_configurator import *
from src.configurator.env_configurator import *
from src.product.ovirt_product import *
from src.product.terraform_product import *


class InfrastructureTestError(Exception):
    pass


class Director:
    """
    Is used for Manages the launch of the builders and products.

    Contains methods:
    - ovirt_product_setup
    - ovirt_product_cleanup
    - ovirt_product_add_template
    - terraform_product_setup
    - terraform_product_cleanup
    - terraform_product_cleanup
    - terraform_apply_vm_template
    - fog_infra_setup
        - ovirt_product_setup
        - ovirt_product_add_template
        - terraform_product_setup
    - fog_infra_cleanup
        - ovirt_product_cleanup
        - terraform_product_cleanup

    The director is the governing structure that describes how specific product and builder
     methods interact for specific tasks selected in the main.
    """

    def __init__(self, chosen_configurator: ConfiguratorInterface) -> None:
        self._configurator = chosen_configurator
        # Create products of FOG infrastructure
        self.ovirt_product = None
        self.terraform_product = None

    def ovirt_product_setup(self) -> None:
        if self.ovirt_product is None:
            self.ovirt_product = OvirtProduct(self._configurator)
        ovirt_setup_builder = OvirtSetupBuilder(self.ovirt_product, self._configurator)
        ovirt_setup_builder.build_product()

        # compare oVirt product with current setup
        if self.ovirt_product != OvirtProduct(self._configurator):
            raise InfrastructureTestError("Built oVirt product does not match current infrastructure")

    def ovirt_product_cleanup(self) -> None:
        if self.ovirt_product is None:
            self.ovirt_product = OvirtProduct(self._configurator)
        ovirt_cleanup_builder = OvirtCleanupBuilder(self.ovirt_product, self._configurator)
        ovirt_cleanup_builder.build_product()

        # compare oVirt product with current setup
        if self.ovirt_product != OvirtProduct(self._configurator):
            raise InfrastructureTestError("Built oVirt product does not match current infrastructure")

    def ovirt_product_add_template(self) -> None:
        if self.ovirt_product is None:
            self.ovirt_product = OvirtProduct(self._configurator)
        ovirt_add_template_builder = OvirtAddTemplateBuilder(self.ovirt_product, self._configurator)
        ovirt_add_template_builder.build_product()

        # compare oVirt product with current setup
        if self.ovirt_product != OvirtProduct(self._configurator):
            raise InfrastructureTestError("Built oVirt product does not match current infrastructure")

    def terraform_product_setup(self) -> None:
        if self.terraform_product is None:
            self.terraform_product = TerraformProduct(self._configurator)
        terraform_setup_builder = TerraformSetupBuilder(self.terraform_product, self._configurator)
        terraform_setup_builder.build_product()

        # compare Terraform product with current setup
        if self.terraform_product != TerraformProduct(self._configurator):
            raise InfrastructureTestError("Built Terraform product does not match current infrastructure")

    def terraform_product_cleanup(self) -> None:  # cleanup Terraform
        if self.terraform_product is None:
            self.terraform_product = TerraformProduct(self._configurator)
        terraform_cleanup_builder = TerraformCleanupBuilder(self.terraform_product, self._configurator)
        terraform_cleanup_builder.build_product()

        # compare Terraform product with current terraform status
        if self.terraform_product != TerraformProduct(self._configurator):
            raise InfrastructureTestError("Built Terraform product does not match current infrastructure")

    def terraform_apply_vm_template(self) -> None:  # cleanup Terraform
        if self.terraform_product is None:
            self.terraform_product = TerraformProduct(self._configurator)
        terraform_template_builder = TerraformApplyTemplate(self.terraform_product, self._configurator)
        terraform_template_builder.build_product()

        if self.terraform_product != TerraformProduct(self._configurator):
            raise InfrastructureTestError("VM_Template product does not match current infrastructure")

    def fog_infra_setup(self) -> None:
        self.ovirt_product_setup()
        self.ovirt_product_add_template()
        self.terraform_product_setup()

    def fog_infra_cleanup(self) -> None:
        self.terraform_product_cleanup()
        self.ovirt_product_cleanup()
