=====================================
How to use Smart Link - documentation
=====================================

.. contents:: **Table of contents**

Before beginning our tour, let's configure some of the underlying stuff.

    >>> from Products.Five.testbrowser import Browser
    >>> from Products.PloneTestCase.setup import portal_owner, default_password
    >>> browser = Browser()
    >>> portal_url = self.portal.absolute_url()
    >>> self.portal.error_log._ignored_exceptions = ()
    >>> browser.open(portal_url)

We have the login portlet, so let's use it.

    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()

We then test that we are still on the portal front page:

    >>> browser.url == portal_url
    True

And we ensure that we get the friendly logged-in message:

    >>> "You are now logged in" in browser.contents
    True

Basic use of Smart Link
=======================

First of all, explore the Smart Link features as new Plone content type.

Use Smart Link as ATLink replacement
------------------------------------

We use the "*Add new*" menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
**Link** and click the *Add* button to get to the add form.

    >>> browser.getControl('Link').click()
    >>> browser.getControl(name='form.button.Add').click()

We select **Link** because Smart Link replace the basic ATLink completely, stealing it's name and
underlying type infos.

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Remote link: sample 1'

We can't only provide the content title; even if the Plone UI display only the "*Title*" as required
field, you can save the link only providing at least a remote or internal link.

    >>> browser.getControl('Save').click()
    >>> 'You must either select an internal link or enter an external link' in browser.contents
    True

In this first example we fill the *External link* field:

    >>> browser.getControl('External link').value = portal_url + '/contact-info'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Another important ATLink (and so Smart Link) feature is the auto-redirection in some cases. Now we are
site manager and also we can modify the link, so we are only warned.

    >>> "You see this page because you have permission to edit this link." in browser.contents
    True
    >>> browser.url == portal_url + '/remote-link-sample-1'
    True

We aren't redirected to the link target now, and we will not also if we click again on the link.

    >>> browser.getLink('Remote link: sample 1').click()
    >>> browser.url == portal_url + '/remote-link-sample-1'
    True

To test this feature we need a different user, and visit the link with this user.
Let's publish the link, then change user.

    >>> browser.getLink('Publish').click()
    >>> 'Item state changed.' in browser.contents
    True
    >>> browser.getLink('Log out').click()
    >>> 'You are now logged out' in browser.contents
    True
    >>> browser.getControl('Login Name').value = 'contributor'
    >>> browser.getControl('Password').value = default_password
    >>> browser.getControl('Log in').click()
    >>> 'You are now logged in' in browser.contents
    True

Let's now move to the link:

    >>> browser.getLink('Remote link: sample 1').click()
    >>> browser.url == portal_url + '/contact-info'
    True

We can now continue all other tests with our Manager user.

    >>> browser.getLink('Log out').click()
    >>> browser.getControl('Login Name').value = portal_owner
    >>> browser.getControl('Password').value = default_password
    >>> browser.getControl('Log in').click()
    >>> 'You are now logged in' in browser.contents
    True

Additional image fields
-----------------------

Smart link give to the contributor some additional fields, better described in the `product documentation`__.

__ http://pypi.python.org/pypi/redturtle.smartlink
    
Here we simply test the usage of those new fields.

First of all, Smart Link give a new **image** and **image caption** field as *Plone "News Item"* does.

Let's add a new image and caption to our link.

    >>> browser.getLink('Remote link: sample 1').click()
    >>> browser.getLink('Edit').click()
    >>> import cStringIO
    >>> imagefile = cStringIO.StringIO(self.getImage())
    >>> image_control = browser.getControl(name='image_file')
    >>> image_control.add_file(imagefile, 'image/png', 'plone_logo.png')
    >>> browser.getControl('Image Caption').value = "A not-so-remote link to our contact info form"
    >>> browser.getControl('Save').click()
    >>> 'Changes saved.' in browser.contents
    True
    
We need also to test if our link really behave an image now:
    
    >>> contactinfo_link = portal['remote-link-sample-1']
    >>> contactinfo_link.unrestrictedTraverse('image_large')
    <Image at .../remote-link-sample-1/image_large>

Now the Smart Link view also display the image and the caption under it in the item's view:

    >>> browser.url == portal_url + '/remote-link-sample-1'
    True
    >>> print  browser.contents
    <!DOCTYPE html PUBLIC...
    ...
    <img src=".../remote-link-sample-1/image_mini" alt="Remote link: sample 1" title="A not-so-remote link to our contact info form" ... />
    ...
    ...</html>

The link icon
-------------

Another minor feature is related to the customization of the link icon. Normally a Plone ATLink will show a
standard type image for all links, and the same is for Smart Link contents.

But with Smart Link, if you want to show another customized icon, you can. The icon image chosen as icon
will override the one from the Plone *getIcon* method, so it will be used in Plone views.

Use this, for example, to show the *favicon* of the remote site. Let's personalize the icon of our link:

    >>> browser.getLink('Edit').click()
    >>> imagefile = cStringIO.StringIO(self.getImage())
    >>> image_control = browser.getControl(name='favicon_file')
    >>> image_control.add_file(imagefile, 'image/png', 'plone_logo.png')
    >>> browser.getControl('Save').click()
    >>> favicon = contactinfo_link.unrestrictedTraverse('favicon')
    >>> favicon
    <Image at .../remote-link-sample-1/favicon>

As the image here is used for replace an icon (where in Plone is 16x16px sized), the uploaded image will be
replaced and saved with a 16x16 ones. Smart Link will not allow you to put there bigger images.

    >>> favicon.width
    16
    >>> favicon.height
    16

To see that the favicon chosen is also used as Plone content icon, let's go on a view that use this
information:

    >>> browser.open(portal_url + '/folder_listing')
    >>> print browser.contents
    <!DOCTYPE html PUBLIC...
    ...
    <img width="16" height="16" src=".../remote-link-sample-1/favicon" alt="Link" />
    ...
    ...</html>

Smart Link main feature: internal link
======================================

The new features above are only minor features that cover some specific needs. The main feature of Smart
Link (that lead to it's name, so a Plone Link that is smart, because it maintain the linked URL) is when
it's used for *internal link to the Plone site*.

You can use your Link content type and reference (without manually write down its URL) another content
of the site.

First of all we need a new content, and we will put it inside a Folder:

    >>> browser.getLink('Add new').click()
    >>> browser.getControl('Folder').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> browser.getControl('Title').value = 'Foo folder'
    >>> browser.getControl('Save').click()
    >>> browser.url == portal_url + '/foo-folder/'
    True
    >>> browser.getLink('Publish').click()
    >>> browser.getLink('Add new').click()
    >>> browser.getControl('Page').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> browser.getControl('Title').value = 'My manual'
    >>> browser.getControl('Body Text').value = """<h2>Welcome!</h2>
    ... <h3><a name="section-1"></a>Section 1</h3>
    ... <p>Lorem ipsum...</p>"""
    >>> browser.getControl('Save').click()
    >>> browser.url == portal_url + '/foo-folder/my-manual'
    True
    >>> browser.getLink('Publish').click()

Use the internal link
---------------------

Now we can create a new internal link to our page:

    >>> browser.open(portal_url)
    >>> browser.getLink('Add new').click()
    >>> browser.getControl('Link').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> browser.getControl(name='title').value = 'Internal link: sample 2'

In a Javascript-enabled browser you can use the **Internal link** field to navigate the site and find
what you want to link.

    >>> mmanual = portal.unrestrictedTraverse("foo-folder/my-manual")
    >>> browser.getControl('Internal link').value = mmanual.UID()
    >>> browser.getControl('Save').click()
    >>> 'Changes saved.' in browser.contents
    True
    >>> mmanual.absolute_url() in browser.contents
    True
    >>> browser.getLink('Publish').click()

Keep the internal link reference
--------------------------------

In early releases Smart Link wanted only to help users to create internal links without manually copy/paste
URLs, so if the referenced document was deleted or moved after the linking action, you were not helped
in keeping this reference.

Recently a more permanent relation is kept between the two contents. To prove this let's first create
another Smart Link that refer to the same document, but in a different way:

    >>> browser.open(portal_url)
    >>> browser.getLink('Add new').click()
    >>> browser.getControl('Link').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> browser.getControl(name='title').value = 'Almost internal link: sample 3'
    >>> browser.getControl('External link').value = portal_url + '/foo-folder/my-manual'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved.' in browser.contents
    True
    >>> mmanual.absolute_url() in browser.contents
    True
    >>> browser.getLink('Publish').click()

We created an internal link in the basic Plone way, creating an external link to a site content's URL.
Apart the boring procedure you must follow doing this, we can have broken link problem.

To prove that, from the visitor point of view, this don't change anything, we can log-off then test links
as anonymous user.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getLink('Internal link: sample 2').click()
    >>> browser.url == portal_url + '/foo-folder/my-manual'
    True
    >>> browser.getLink('Almost internal link: sample 3').click()
    >>> browser.url == portal_url + '/foo-folder/my-manual'
    True

Ok, but what really change also is a mechanism thats keep a sort of link integrity. Let's log-in again
as site administrator.

    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()

First of all, when a site content is "*smart linked*" from a Smart Link, it's marked with a special
interface.

    >>> from redturtle.smartlink.interfaces import ISmartLinked
    >>> ISmartLinked.providedBy(mmanual)
    True

This marker make some of the magic. A set of events are related to actions taken on contents that
behave those markers.

For example what's happen when you move (or rename, it's the same...) the referenced content?

    >>> browser.open(portal_url + '/foo-folder/my-manual')
    >>> browser.getLink('Rename').click()
    >>> browser.getControl('New Short Name').value = 'my-foo-manual'
    >>> browser.getControl('Rename All').click()
    >>> "Renamed 'my-manual' to 'my-foo-manual'." in browser.contents
    True

See that Smart Link keep the relation alive:

    >>> browser.getLink('Internal link: sample 2').click()
    >>> slink = portal['internal-link-sample-2']
    >>> slink.getRemoteUrl() == portal_url + '/foo-folder/my-foo-manual'
    True
    >>> slink.getField('remoteUrl').get(slink) == portal_url + '/foo-folder/my-foo-manual'
    True

But before test this as anonymous, let me do something I will explain later.
I create a new fake content with the same id of the one we renamed:

    >>> browser.open(portal_url + '/foo-folder')
    >>> browser.getLink('Add new').click()
    >>> browser.getControl('Page').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> browser.getControl('Title').value = 'My manual'
    >>> browser.getControl('Body Text').value = "<p>I'm not the REAL manual, just a fake!</p>"
    >>> browser.getControl('Save').click()
    >>> browser.getLink('Publish').click()

Ok. Now: to show what can be bad with basic Plone ATLink used for internal link (or also with Smart Link,
but used in a bad way), we log-off again.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getLink('Internal link: sample 2').click()
    >>> browser.url == portal_url + '/foo-folder/my-foo-manual'
    True

Wow, the first test is ok. The internal link has kept the URL change of the linked page!
And the "normal link"?

    >>> browser.getLink('Almost internal link: sample 3').click()
    >>> browser.url == portal_url + '/foo-folder/my-foo-manual'
    False
    >>> browser.url == portal_url + '/foo-folder/my-manual'
    True
    >>> "I'm not the REAL manual, just a fake!" in browser.contents
    True

As expected, it not works. We are now on the new content, the fake document.

But why we created it?

In facts, the normal links approach *can* work normally even for internal link and if the target object
is moved, because Plone has an internal mechanism that automatically make aliases for content that changed
their URLs (the `plone.app.redirector`__ package manage this feature).

__ http://pypi.python.org/pypi/plone.app.redirector

This is a good solution that Plone give us, but it's not perfect:

* you will have problems if you loose the data inside the Redirection utility
* more probable, you will have problem if another content will use the same URL in future.

For a good reason, if you old URL will be taken by a new content, the URL will be taken and used to
reach this content. Obviously the *real* object with the same URL wins on *fake* object that held this
URL some time ago...

The relation from the linked content back to the Smart Link
-----------------------------------------------------------

Some action are taken also when you touch Smart Link. If you delete a Smart Link that held an internal
link to a site's content, the referenced object is "cleaned", and the marker interface removed.

    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.getLink('Internal link: sample 2').click()
    >>> browser.getLink('Delete').click()
    >>> browser.getControl('Delete').click()
    >>> 'Internal link: sample 2 has been deleted.' in browser.contents
    True
    >>> ISmartLinked.providedBy(mmanual)
    False

In the same way, if I create a Smart Link for an internal reference, then I change it to link another
content or to a remote URL, all interfaces must always be removed.

XXX