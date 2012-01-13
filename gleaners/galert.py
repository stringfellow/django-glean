#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
import getpass

import galerts


class GAlertConnector(object):
    """Connects to Google Alerts, allows management and retrieves content.
    
    
    """
    def alerts_manager():
        un = raw_input("Email: ")
        pwd = getpass.getpass()
        gam = galerts.GAlertsManager(un, pwd)
        pwd = None  # discard ASAP.
        import pdb; pdb.set_trace()

    def get_data(self):
        """Checks the feed, makes an object for any that don't exist."""
        pass
