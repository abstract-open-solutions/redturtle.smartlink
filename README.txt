========================
Smart Link Documentation
========================

An enhanced version of the base Plone link content type.

After intalling this you'll see that the Plone link will have a new *image* and *caption* fields
like the News Item content type.

Also the new Link type can handle internal (to Plone contents) and external links. You can use the
internal link field to automatically attach the link value to an internal content of the portal
(in a similar way used for related contents).

An event-based system will also keep URLs updated even when you move/rename target document.

Handle backend/frontend URLs
----------------------------

The Smart Link structure is nothing more that a ATLink content, so the way used to store URL
in the object or in the portal_catalog is the same as Plone does. There is no magic behind.

For this reason, when you are using Smart Link for internal references, the *static* URL is
stored and used.

This will lead to problems when you are using this product for site where you have different
backend/frontend URLs. For this reason you must use the "*Configure Smart Link*" control panel
to handle URL transformation.

You can also use an option that says to Smart Link to store relative URLs, but this will also
include the Plone site id in every link (and you must rewrite this from Apache if you don't
like this). 

Warning 1
---------

Smart Link shapechange itself to be the Link content type, and hide the basic Plone Link type.

Warning 2
---------

**Pay attention** when you update the whole portal_catalog using ZMI from URLs different from
backend or frontend ones (for example: using a tunnel).

If you run the update from (for example) "localhost:8090/site" and this URL is not the public
or backend URL, all your internal links will be changed to this hostname!
Another catalog update (from the right URL) will fix this.

FileSystemStorage
-----------------

The product try to register the link image field onto `iw.fss`__ if it's installed.

__ http://pypi.python.org/pypi/iw.fss

TODO
----

* Fix this ugly error: *WARNING SecurityInfo Conflicting security declarations for setId*

Credits
=======

Developed with the support of:

* `Camera di Commercio di Ferrara`__
  
  .. image:: http://www.fe.camcom.it/logo_cciafe.jpg
     :alt: CCIAA Ferrara logo

* `Azienda USL Ferrara`__
  
  .. image:: http://www.ausl.fe.it/logo_ausl.gif
     :alt: Azienda USL's logo
  
All of them supports the `PloneGov initiative`__.

__ http://www.fe.camcom.it/
__ http://www.ausl.fe.it/
__ http://www.plonegov.it/

Authors
=======

This product was developed by RedTurtle Technology team.

.. image:: http://www.redturtle.net/redturtle_banner.png
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.net/

Special thanks to *Mauro Amico* (mamico) for providing support and fixing issues.

Before this: ComboLink
----------------------

Part of the code of Smart Link was taken from the `ComboLink`__ Plone (and Plonegov) product.
This project was giving the same internal link feature in old 2.1/2.5 Plone releases.

__ http://plone.org/products/combolink/

