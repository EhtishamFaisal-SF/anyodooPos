
Odoo14
============

Connection
==========

        .. code-block:: php

            require_once('ripcord.php');
            $info = ripcord::client('https://demo.odoo.com/start')->start();
            list($url, $db, $username, $password) =
              array($info['host'], $info['database'], $info['user'], $info['password']);
            $common = ripcord::client("$url/xmlrpc/2/common");
            $uid = $common->authenticate($db, $username, $password, array());
            $models = ripcord::client("$url/xmlrpc/2/object");


Configuration
-------------

If you already have an Odoo server installed, you can just use its
parameters

    .. code-block:: php

        $url = <insert server URL>;
        $db = <insert database name>;
        $username = "admin";
        $password = <insert password for your admin user (default: admin)>;


API Keys
''''''''

        .. code-block:: php

            require_once('ripcord.php');
            $info = ripcord::client('https://demo.odoo.com/start')->start();
            list($url, $db, $username, $password) =
              array($info['host'], $info['database'], $info['user'], $info['password']);

        .. note::

            These examples use the `Ripcord <https://code.google.com/p/ripcord/>`_
            library, which provides a simple XML-RPC API. Ripcord requires that
            `XML-RPC support be enabled
            <https://php.net/manual/en/xmlrpc.installation.php>`_ in your PHP
            installation.

            Since calls are performed over
            `HTTPS <https://en.wikipedia.org/wiki/HTTP_Secure>`_, it also requires that
            the `OpenSSL extension
            <https://php.net/manual/en/openssl.installation.php>`_ be enabled.


Logging in
----------

Odoo requires users of the API to be authenticated before they can query most
data.

The ``xmlrpc/2/common`` endpoint provides meta-calls which don't require
authentication, such as the authentication itself or fetching version
information. To verify if the connection information is correct before trying
to authenticate, the simplest call is to ask for the server's version. The
authentication itself is done through the ``authenticate`` function and
returns a user identifier (``uid``) used in authenticated calls instead of
the login.

    .. code-block:: php

        $common = ripcord::client("$url/xmlrpc/2/common");
        $common->version();

    .. code-block:: php

        $uid = $common->authenticate($db, $username, $password, array());


Calling methods
===============

The second endpoint is ``xmlrpc/2/object``, is used to call methods of odoo
models via the ``execute_kw`` RPC function.

Each call to ``execute_kw`` takes the following parameters:

* the database to use, a string
* the user id (retrieved through ``authenticate``), an integer
* the user's password, a string
* the model name, a string
* the method name, a string
* an array/list of parameters passed by position
* a mapping/dict of parameters to pass by keyword (optional)

        .. code-block:: php

            $models = ripcord::client("$url/xmlrpc/2/object");
            $models->execute_kw($db, $uid, $password,
                'res.partner', 'check_access_rights',
                array('read'), array('raise_exception' => false));

List records
------------

Records can be listed and filtered via :meth:`~odoo.models.Model.search`.

:meth:`~odoo.models.Model.search` takes a mandatory
:ref:`domain <reference/orm/domains>` filter (possibly empty), and returns the
database identifiers of all records matching the filter. To list customer
companies for instance:

        .. code-block:: php

            $models->execute_kw($db, $uid, $password,
                'res.partner', 'search', array(
                    array(array('is_company', '=', true))));



Count records
-------------

Rather than retrieve a possibly gigantic list of records and count them,
:meth:`~odoo.models.Model.search_count` can be used to retrieve
only the number of records matching the query. It takes the same
:ref:`domain <reference/orm/domains>` filter as
:meth:`~odoo.models.Model.search` and no other parameter.

        .. code-block:: php

            $models->execute_kw($db, $uid, $password,
                'res.partner', 'search_count',
                array(array(array('is_company', '=', true))));


.. warning::

    calling ``search`` then ``search_count`` (or the other way around) may not
    yield coherent results if other users are using the server: stored data
    could have changed between the calls


Search and read
---------------

Because it is a very common task, Odoo provides a
:meth:`~odoo.models.Model.search_read` shortcut which as its name suggests is
equivalent to a :meth:`~odoo.models.Model.search` followed by a
:meth:`~odoo.models.Model.read`, but avoids having to perform two requests
and keep ids around.

Its arguments are similar to :meth:`~odoo.models.Model.search`'s, but it
can also take a list of ``fields`` (like :meth:`~odoo.models.Model.read`,
if that list is not provided it will fetch all fields of matched records):


        .. code-block:: php

            $models->execute_kw($db, $uid, $password,
                'res.partner', 'search_read',
                array(array(array('is_company', '=', true))),
                array('fields'=>array('name', 'country_id', 'comment'), 'limit'=>5));



Create records
--------------

Records of a model are created using :meth:`~odoo.models.Model.create`. The
method will create a single record and return its database identifier.

:meth:`~odoo.models.Model.create` takes a mapping of fields to values, used
to initialize the record. For any field which has a default value and is not
set through the mapping argument, the default value will be used.

        .. code-block:: php

            $id = $models->execute_kw($db, $uid, $password,
                'res.partner', 'create',
                array(array('name'=>"New Partner")));

Update records
--------------

Records can be updated using :meth:`~odoo.models.Model.write`, it takes
a list of records to update and a mapping of updated fields to values similar
to :meth:`~odoo.models.Model.create`.

Multiple records can be updated simultaneously, but they will all get the same
values for the fields being set. It is not currently possible to perform
"computed" updates (where the value being set depends on an existing value of
a record).

        .. code-block:: php

            $models->execute_kw($db, $uid, $password, 'res.partner', 'write',
                array(array($id), array('name'=>"Newer partner")));
            // get record name after having changed it
            $models->execute_kw($db, $uid, $password,
                'res.partner', 'name_get', array(array($id)));

Delete records
--------------

Records can be deleted in bulk by providing their ids to
:meth:`~odoo.models.Model.unlink`.

        .. code-block:: php

            $models->execute_kw($db, $uid, $password,
                'res.partner', 'unlink',
                array(array($id)));
            // check if the deleted record is still in the database
            $models->execute_kw($db, $uid, $password,
                'res.partner', 'search',
                array(array(array('id', '=', $id))));
