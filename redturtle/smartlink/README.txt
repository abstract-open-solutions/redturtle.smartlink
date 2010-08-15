=====================================
How to use Smart Link - documentation
=====================================

Before beginning our tour, let's configure some underlying stuff.

    >>> from Products.Five.testbrowser import Browser
    >>> from Products.PloneTestCase.setup import portal_owner, default_password
    >>> browser = Browser()
    >>> portal_url = self.portal.absolute_url()
    >>> self.portal.error_log._ignored_exceptions = ()
    >>> browser.open(portal_url)

We have the login portlet, so let's use that.

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

First of all, Smart Link wanna be a replacement of the basic Plone ATLink content type, so
it must work as the ATLlink does.

Use Smart Link as ATLink replacement
------------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
**Link** and click the *Add* button to get to the add form.

    >>> browser.getControl('Link').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Link' in browser.contents
    True

We select **Link** because Smart Link replace the basic ATLink completly, stealing it's name and
underlying type infos.

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Remote link: sample 1'

We can't only provide the content title; even if the Plone UI display only the 'title' as required
field, you can save the link only providing at least a remote or internal link.

    >>> browser.getControl('Save').click()
    >>> 'You must either select an internal link or enter an external link' in browser.contents
    True

In this first example we fill the *External Link* field:

    >>> browser.getControl('External Link').value = portal_url + '/contact-info'
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

Additional fields
-----------------

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

But with Smart Link, if you want to show another customized icon, you can. The icon image choosen as icon will
override the one from the Plone *getIcon* method, so it wil be used in Plone views.

Use this, for example, to show the favicon of the remote site. Let's personalize the icon of our link:

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

To see that the favicon choosen is also used as Plone content icon, let's go on a view that use this
information:

    >>> browser.open(portal_url + '/folder_listing')
    >>> print browser.contents
    <!DOCTYPE html PUBLIC...
    ...
    <img width="16" height="16" src=".../remote-link-sample-1/favicon" alt="Link" />
    ...
    ...</html>
    