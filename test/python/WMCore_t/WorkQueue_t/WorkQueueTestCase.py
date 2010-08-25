"""
_File_t_

Unit tests for the WMBS File class.
"""

__revision__ = "$Id: WorkQueueTestCase.py,v 1.3 2009/09/03 13:19:50 swakef Exp $"
__version__ = "$Revision: 1.3 $"

import unittest
import logging
import os
import threading

from WMQuality.TestInit import TestInit
# pylint: disable-msg = W0611
import WMCore.WMLogging # needed to bring in logging.SQLDEBUG
# pylint: enable-msg = W0611

class WorkQueueTestCase(unittest.TestCase):
    _setup = False
    _teardown = False

    def setUp(self):
        """
        _setUp_

        Setup the database and logging connection.  Try to create all of the
        WMBS tables.  Also add some dummy locations.
        """
        if self._setup:
            return

        self.testInit = TestInit(__file__, os.getenv("DIALECT"))
        self.testInit.setLogging() # logLevel = logging.SQLDEBUG
        self.testInit.setDatabaseConnection()
        self.testInit.setSchema(customModules = ["WMCore.WMBS"],
                                useDefault = False)
        self.testInit.setSchema(customModules = ["WMCore.WorkQueue.Database"],
                                useDefault = False)

        self._setup = True
        return

    def tearDown(self):
        """
        _tearDown_
        
        Drop all the WMBS tables.
        """
        myThread = threading.currentThread()

        if self._teardown:
            return

        if myThread.transaction == None:
            myThread.transaction = Transaction(self.dbi)

        myThread.transaction.begin()

        self.testInit.clearDatabase(modules = ["WMCore.WorkQueue.Database"])
        self.testInit.clearDatabase(modules = ["WMCore.WMBS"])
        self._teardown = True
