Installation
=============
**This framework is published at the PyPI, install it with pip:**

1. This package makes it possible to use module methods in synchronous frameworks:

   .. code-block:: bash

      pip install privatbank-api-client[http]

2. This package makes it possible to use module methods in asynchronous frameworks:

   .. code-block:: bash

      pip install privatbank-api-client[aio]

3. This package makes it possible to use ready-made views with a synchronous script based on the Django Rest framework:

   .. code-block:: bash

      pip install privatbank-api-client[drf]

To get started, add the following packages to ``INSTALLED_APPS``:

   .. code-block:: python

      INSTALLED_APPS = [
      ...
      'rest_framework',
      'drf_privat',
      ]

Include ``drf_mono`` urls to your ``urls.py``:

   .. code-block:: python

      urlpatterns = [
          ...
          path('privat/', include('drf_privat.urls', namespace='drf_privat')),
      ]

4. This package makes it possible to use ready-made routers with an asynchronous script based on the FastAPI framework:

   .. code-block:: python

      pip install privatbank-api-client[fastapi]

5. To install all packages at once:

   .. code-block:: python

      pip install privatbank-api-client[all]
