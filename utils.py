#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
import getpass

import galerts


def alerts_manager():
    un = raw_input("Email: ")
    pwd = getpass.getpass()
    gam = galerts.GAlertsManager(un, pwd)
    pwd = None  # discard ASAP.
    import pdb; pdb.set_trace()
