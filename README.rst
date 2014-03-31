Introduction
============

collective.portlet.countdown is a simple Plone portlet. It shows a countdown to a given date.


Compatibility
=============

Version 1.0.0 is tested with Plone 4.3.x.


Installation
============

Add this line in the eggs section of your ``buildout.cfg``

.. code:: ini

    eggs =
        ...
        collective.portlet.countdown


Uninstalling
------------

TBD.


Installation as a dependency from another product
-------------------------------------------------

If you want to add operun.crm as a dependency from another products use the profile ``default`` in your ``metadata.xml``.

.. code:: xml

    <metadata>
      <version>1</version>
        <dependencies>
            <dependency>profile-collective.portlet.countdown:default</dependency>
        </dependencies>
    </metadata>


Toubleshooting
==============

Please report issues in the bugtracker at https://github.com/operun/collective.portlet.countdown/issues.


Branches
========

The master-branch supports Plone 4 only. There is a branch image where the image is stored in the portlet assignment itself.


License
=======

GNU General Public License, version 2


Contributors
============

* Stefan Antonelli <stefan.antonelli@operun.de>
* Steffen Lindner <lindner@starzel.de>
