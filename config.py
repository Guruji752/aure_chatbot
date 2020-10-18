#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "37ce05ea-ce11-424d-9f56-8a90fc928a9c")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "7c120zQa.ly-Ow2v~5a2_RfyivvfO04zN~")
