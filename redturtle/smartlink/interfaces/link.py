from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from redturtle.smartlink import smartlinkMessageFactory as _

class ILink(Interface):
    """A link to an internal or external resource."""
    
    # -*- schema definition goes here -*-
