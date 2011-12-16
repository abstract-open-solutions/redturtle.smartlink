# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

from redturtle.smartlink.interfaces.link import ISmartLink

class FixFakeInternalLinkView(BrowserView):
    """
    A view that look for all Smart Link content types defined as external link
    but that contain URL's that point to internal contents.
    """
    
    def __call__(self):
        request = self.request
        request.set('disable_border', True)
        
        if not request.get('path', []):
            return self.index()
        return "Ciao"
    
    @property
    def status(self):
        return None

    def _transformURL(self, url):
        """
        Given an URL, check all Smart Link configuration options to be sure that
        we refer to the right hostname
        """ 
        return url

    def _findInternalByURL(self, url):
        """
        Given a valid site URL, return the linked internal content, if any
        """
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')
        portal_url = getToolByName(context, 'portal_url')
        site_url = portal_url()
        portal = portal_url.getPortalObject()
        path = url.replace(site_url, '', 1)
        brain = catalog(path={'query': "/%s%s" % (portal.getId(), path),
                              'depth': 0})
        return path and brain and brain[0].getObject() or None

    def getFakeLinks(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        portal_url = getToolByName(self.context, 'portal_url')()
        links = catalog(object_provides=ISmartLink.__identifier__,
                        sort_on='sortable_title')
        results = []
        for x in links:
            obj = x.getObject()
            # Sometimes you can loose all internal/external data, but the original
            # remoteUrl value always keep the up-to-date copy of the URL
            external_link = obj.getExternalLink() or \
                        (not obj.getInternalLink() and obj.getField('remoteUrl').get(obj))
            if external_link:
                external_link = self._transformURL(obj.getExternalLink())
                if external_link.startswith(portal_url):
                    internalObj = self._findInternalByURL(external_link)
                    results.append({'path': '/'.join(obj.getPhysicalPath()),
                                    'title': obj.Title(),
                                    'absolute_url_path': obj.absolute_url_path(), 
                                    'url': obj.absolute_url(),
                                    'external_link': obj.getExternalLink(),
                                    'internal_obj': internalObj,
                                    })
        return results
