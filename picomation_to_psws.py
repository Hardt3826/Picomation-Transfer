# ----------------------------------------------------------------------------
# Copyright (c) 2024 University of Alabama
# All rights reserved.
#
# Distributed under the terms of the BSD 3-clause license.
#
# The full license is in the LICENSE file, distributed with this software.
# ----------------------------------------------------------------------------

import os

from paramiko import AutoAddPolicy, SSHClient


def main():
    client= SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    PSWS= client.connect('pswsnetwork.caps.ua.edu', username='echardt', password='H@rdtCompSc!')

if __name__ == "__main__":
    main()