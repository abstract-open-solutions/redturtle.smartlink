# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView

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