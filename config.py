#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "baa2585b-2ec3-47bb-bd45-748cd9bdf184")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "GvkevEvmr3SE8dGxRco-N2..0~8_goaVzT")
