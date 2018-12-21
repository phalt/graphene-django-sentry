#!/usr/bin/env python
# -*- coding: utf-8 -*-

from http.client import OK
from unittest.mock import MagicMock, patch
from urllib.parse import urlencode

import graphene_django.views as views
from django.urls import reverse
from graphql import GraphQLError
from graphql.error import GraphQLLocatedError


class CustomException(Exception):
    """ Boom! """


def get_query_string():
    path = reverse('graphql')
    query = urlencode({'query': 'query {test}'})
    path = f'{path}?{query}'
    return path


def test_view(client):
    result = client.get(
        get_query_string(),
        HTTP_ACCEPT="application/json;q=0.8, text/html;q=0.9",
    )
    assert result.status_code == OK


@patch.object(views.GraphQLView, 'execute_graphql_request')
@patch('sentry_sdk.capture_exception')
def test_execute_graphql_request(
    mocked_capture_exception,
    mocked_method,
    client,
):
    error = CustomException('Boom')
    errors = [GraphQLLocatedError([], error)]

    mocked_return_value = MagicMock()
    mocked_return_value.errors = errors

    mocked_method.return_value = mocked_return_value
    result = client.get(
        get_query_string(),
        HTTP_ACCEPT="application/json;q=0.8, text/html;q=0.9",
    )
    assert result.status_code == 400
    assert result.json()['errors'][0]['message'] == 'Boom'
    mocked_capture_exception.assert_called_with(error)


@patch.object(views.GraphQLView, 'execute_graphql_request')
@patch('sentry_sdk.capture_exception')
def test_execute_graphql_request_raises_raw_graphql_exceptions(
    mocked_capture_exception,
    mocked_method,
    client,
):
    error = GraphQLError(message='Syntax error in GraphQL query')

    mocked_return_value = MagicMock()
    mocked_return_value.errors = [error]

    mocked_method.return_value = mocked_return_value
    result = client.get(
        reverse('graphql'),
        {'query': '{__schema{types{name}}}'},
    )
    assert result.status_code == 400
    assert result.json()['errors'][0]['message'] == (
        'Syntax error in GraphQL query'
    )
    mocked_capture_exception.assert_called_with(error)
