"""
Copyright 2013 Rackspace

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

import time

from cafe.drivers.unittest.decorators import tags
from cloudcafe.compute.common.datagen import rand_name
from cloudcafe.compute.common.types import NovaServerRebootTypes
from test_repo.compute.fixtures import ComputeFixture


class RebootServerHardTests(ComputeFixture):

    @classmethod
    def setUpClass(cls):
        super(RebootServerHardTests, cls).setUpClass()
        cls.key = cls.keypairs_client.create_keypair(rand_name("key")).entity
        response = cls.server_behaviors.create_active_server(key_name=cls.key.name)
        cls.server = response.entity
        cls.resources.add(cls.server.id, cls.servers_client.delete_server)

    @classmethod
    def tearDownClass(cls):
        super(RebootServerHardTests, cls).tearDownClass()

    @tags(type='smoke', net='yes')
    def test_reboot_server_hard(self):
        """ The server should be power cycled """
        remote_instance = self.server_behaviors.get_remote_instance_client(
            self.server, config=self.servers_config, key=self.key.private_key)
        uptime_start = remote_instance.get_uptime()
        start = time.time()

        self.server_behaviors.reboot_and_await(self.server.id, NovaServerRebootTypes.HARD)
        remote_client = self.server_behaviors.get_remote_instance_client(
            self.server, config=self.servers_config, key=self.key.private_key)
        finish = time.time()
        uptime_post_reboot = remote_client.get_uptime()
        self.assertLess(uptime_post_reboot, (uptime_start + (finish - start)))

