from zope.formlib import form
from plone.app.controlpanel.form import ControlPanelForm
from redturtle.smartlink.interfaces.utility import ISmartlinkConfig
from redturtle.smartlink import smartlinkMessageFactory as _

class SmartlinkConfigForm(ControlPanelForm):
    """Smartlink Control Panel Form"""

    form_fields = form.Fields(ISmartlinkConfig)

    label = _(u"Smartlink Configuration Panel")
    description = _(u"Prova.")
    form_name = _("Smartlink Settings")
    

#    @form.action("Update the existing internal links")
#    def action_update(self, action, data):
#        print "ciao"
#        return
