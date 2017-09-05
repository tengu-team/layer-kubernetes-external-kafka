#!/usr/bin/env python3
# Copyright (C) 2017  Ghent University
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import os
from charmhelpers.core import hookenv, unitdata
from charmhelpers.core.hookenv import status_set, log
from charms.reactive import when, when_not, set_state, remove_state
from charms.layer.externalservicehelpers import configure_headless_service


@when_not('kafka.joined')
def no_kafka_connected():
    status_set('blocked', 'Please connect the application to Kafka.')


@when('kafka.ready')
@when_not('service.requested')
def kafka_connected(kafka):
    status_set('maintenance', 'Kafka connection found.')
    kafka_brokers = kafka.kafkas()
    if kafka_brokers:
        ips = []
        for broker in kafka_brokers:
            port = broker['port']
            ips.append(broker['host'])
        configure_headless_service(ips, int(port))
        set_state('service.requested')
