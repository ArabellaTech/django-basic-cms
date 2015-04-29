==============================
Django Basic CMS reference API
==============================

.. contents::
    :local:
    :depth: 1

The application model
======================

Django Basic CMS declare rather simple models: :class:`Page <basic_cms.models.Page>`
:class:`Content <basic_cms.models.Content>` and :class:`PageAlias <basic_cms.models.PageAlias>`.

Those Django models have the following relations:

.. aafig::
    :aspect: 60
    :scale: 150
    :proportional:

              +------------+
              |PageAlias   |
              +-----+------+
                    |
                foreign key
                    |
                +---v---+
        +------>+ Page  +
        |       +---+---+
        |           |
        |          use
        |           |
        |     +-----v-----+       +-------+---------------+
        |     | Template 1+------>+ Placeholder Node title|
        |     +-----+-----+       +-------+---------------+
        |           |
     foreign key  contains
        |           |
        |   +-------v--------------+
        |   | Placeholder Node body|
        |   +-------+--------------+
        |           |
        |           |
        |  +--------+--------+-------------+
        |  |                 |             |
      +-+--v------+    +-----v-----+       v
      | Content   |    | Content   |     SSSSS
      | english   |    | french    |     SSSSS
      +-----------+    +-----------+


Placeholders
============

.. automodule:: basic_cms.placeholders
    :members:
    :undoc-members:

Template tags
=============

.. automodule:: basic_cms.templatetags.pages_tags
    :members:

Widgets
=======

.. automodule:: basic_cms.widgets
    :members:
    :undoc-members:

Page Model
==========

.. autoclass:: basic_cms.models.Page
    :members:

Page Manager
============

.. autoclass:: basic_cms.managers.PageManager
    :members:
    :undoc-members:

Page view
==========

.. autoclass:: basic_cms.views.Details
    :members:

Content Model
=============

.. autoclass:: basic_cms.models.Content
    :members:
    :undoc-members:

Content Manager
===============

.. autoclass:: basic_cms.managers.ContentManager
    :members:
    :undoc-members:

PageAlias Model
===============

.. autoclass:: basic_cms.models.PageAlias
    :members:
    :undoc-members:

PageAlias Manager
=================

.. autoclass:: basic_cms.managers.PageAliasManager
    :members:
    :undoc-members:

Utils
=====

.. automodule:: basic_cms.utils
    :members:
    :undoc-members:

Http
====

.. automodule:: basic_cms.http
    :members:
    :undoc-members:

Admin views
===========

.. automodule:: basic_cms.admin.views
    :members:
    :undoc-members:
