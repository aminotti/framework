.. _using-datetime:

Using date and time
===================

With time zone
--------------

1. On client side, local date is either converted to UTC or must contain UTC offset before been sent to the API.
2. The API deals only with UTC date (storage is done in UTC format and return UTC to client app).
3. The client convert the UTC date to a local date.

.. note::

    For client with unknow local date (e.g. a mail where you don't know the recipient local date), use global API settings to select the correct local date and sent it with UTC offset.

With JavaScrip the syntax for local date is either ``<AAAA:>-<MM>-<JJ>T<HH>:<MM>[:SS]+\|-<HH>:00`` or ``<AAAA>-<MM>-<JJ>T<HH>:<MM>[:SS]Z``.

.. code:: javascript

    dt = new Date(Date.UTC(2005, 12, 30, 0, 0, 0, 0));
    nbminutes = dt.getTimezoneOffset();

Without time zone
-----------------

Just send a local time ending with **Z** : ``<AAAA>-<MM>-<JJ>T<HH>:<MM>Z``.
