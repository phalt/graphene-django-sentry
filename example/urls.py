from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from graphene_django_sentry import SentryGraphQLView

from .schema import schema  # Your graphQL schema

urlpatterns = [
    url(
      r'^graphql',
      csrf_exempt(SentryGraphQLView.as_view(schema=schema)),
      name='graphql',
    ),
]
