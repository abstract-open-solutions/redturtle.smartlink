# -*- coding: utf-8 -*-

import logging
from Products.CMFCore.utils import getToolByName

PROFILE_ID = 'profile-redturtle.smartlink:default'

def setupVarious(context):
    portal = context.getSite()

    if context.readDataFile('redturtle.smartlink_various.txt') is None:
        return

def migrateTo1002(context, logger=None):
    if logger is None:
        logger = logging.getLogger('redturtle.smartlink')
    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runImportStepFromProfile(PROFILE_ID, 'rolemap')
    setup_tool.runImportStepFromProfile(PROFILE_ID, 'controlpanel')
    setup_tool.runImportStepFromProfile(PROFILE_ID, 'action-icons')
    logger.info("Migrated to 1.1.0")
