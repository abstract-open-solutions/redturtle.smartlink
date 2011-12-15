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
        
        if not request.get('aaa'):
            return self.index()
    
    @property
    def status(self):
        return None

    def _transformURL(self, url):
        """
        Given an URL, check all Smart Link configuration options to be sure that
        we refer to the right hostname
        """
 
        return url

    def getFakeLinks(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        links = catalog(object_provides=ISmartLink.__identifier__,
                        sort_on='sortable_title')
        results = []
        for x in links:
            obj = x.getObject()
            if obj.getExternalLink():
                external_link = self._transformURL(obj.getExternalLink())
                results.append({'path': '/'.join(obj.getPhysicalPath()),
                                'title': obj.Title(),
                                'absolute_url_path': obj.absolute_url_path(), 
                                'url': obj.absolute_url(),
                                'external_link': obj.getExternalLink(),
                                })
        return results
