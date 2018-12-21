🌐⚠️ graphene-django-sentry
-------

*Capture Sentry exceptions in Graphene views*

When using `Graphene Django`_, you sometimes want to raise exceptions and capture them in the API.

However, Graphene Django eats the raised exceptions and you won't see it in Sentry! 😭

This package thinly wraps the normal GraphQLView with a handler that deals with Sentry errors properly.

So the results:

1. Sentry will show the true exceptions.
2. Graphene will continue to work like normal.

Works with:

* Python 3.6+
* Django 2.1+
* graphene-django 2.2+


.. image:: https://img.shields.io/pypi/v/graphene_django_sentry.svg
        :target: https://pypi.org/project/graphene_django_sentry/

.. image:: https://img.shields.io/pypi/pyversions/graphene_django_sentry.svg
        :target: https://pypi.org/project/graphene_django_sentry/

.. image:: https://img.shields.io/pypi/l/graphene_django_sentry.svg
        :target: https://pypi.org/project/graphene_django_sentry/

.. image:: https://img.shields.io/pypi/status/graphene_django_sentry.svg
        :target: https://pypi.org/project/graphene_django_sentry/

.. image:: https://circleci.com/gh/phalt/graphene_django_sentry/tree/master.svg?style=svg
        :target: https://circleci.com/gh/phalt/graphene_django_sentry/tree/master

Installing the project is easy:

.. code-block:: bash

    pip install graphene-django-sentry

Full blown example:

.. code-block:: python

  # urls.py

  from .schema import schema
  from graphene_django_sentry.views import SentryGraphQLView

  urlpatterns = [
      url(
          r'^graphql',
          csrf_exempt(SentryGraphQLView.as_view(schema=schema)),
          name='graphql',
      ),
  ]

📖 What can I do?
--------

- Capture Sentry exceptions properly when they are `raise`-d in Graphene views.

🏗 Status
----------

graphene-django-sentry is currently stable and suitable for use.

🎥 Credits
-----------

This package was created with Cookiecutter_.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _Graphene Django: https://github.com/graphql-python/graphene-django
