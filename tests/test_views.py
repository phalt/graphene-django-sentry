#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from http.client import OK
from io import BytesIO
from unittest.mock import MagicMock, patch
from urllib.parse import urlencode

import graphene_django.views as views
from django.http import HttpResponse
from django.test import Client
from django.urls import reverse
from graphql import GraphQLError
from graphql.error import GraphQLLocatedError


test_phrase = 'THIS IS TEEEEEEEEST!'


class CustomException(Exception):
    """ Boom! """


def get_query_string():
    path = reverse('graphql')
    query = urlencode({'query': 'query {test}'})
    path = f'{path}?{query}'
    return path


def run_file_upload_request(client: Client, test_phrase: str) -> HttpResponse:
    file = BytesIO(bytes(test_phrase, 'utf8'))

    file.seek(0)

    query = 'mutation TestFileUpload($file: Upload!){' \
            'testFileUpload(file: $file){' \
            'success, content' \
            '}' \
            '}'

    # For request structure see spec:
    # https://github.com/jaydenseric/graphql-multipart-request-spec
    return client.post(reverse('file_graphql'), {
        'operations': json.dumps({
            'query': query,
            'variables': {
                'file': None
            }}),
        'map': json.dumps({'file': ["variables.file"]}),
        'file': file
    }, HTTP_ACCEPT='application/json;q=0.8, text/html;q=0.9')


def test_view(client):
    result = client.get(
        get_query_string(),
        HTTP_ACCEPT="application/json;q=0.8, text/html;q=0.9",
    )
    assert result.status_code == OK


def test_file_upload_view(client: Client):
    result = run_file_upload_request(client, test_phrase)

    data = result.json()

    success = data.get('data', {}).get('testFileUpload', {}).get('success')
    content = data.get('data', {}).get('testFileUpload', {}).get('content')

    assert result.status_code == OK
    assert success == True
    assert content == test_phrase


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
def test_execute_graphql_file_upload_request(
    mocked_capture_exception,
    mocked_method,
    client,
):
    error = CustomException('Boom')
    errors = [GraphQLLocatedError([], error)]

    mocked_return_value = MagicMock()
    mocked_return_value.errors = errors

    mocked_method.return_value = mocked_return_value
    result = run_file_upload_request(client, test_phrase)

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


@patch.object(views.GraphQLView, 'execute_graphql_request')
@patch('sentry_sdk.capture_exception')
def test_execute_graphql_file_upload_request_raises_raw_graphql_exceptions(
        mocked_capture_exception,
        mocked_method,
        client: Client
):
    error = GraphQLError(message='Syntax error in GraphQL query')

    mocked_return_value = MagicMock()
    mocked_return_value.errors = [error]

    mocked_method.return_value = mocked_return_value

    result = run_file_upload_request(client, test_phrase)

    assert result.status_code == 400
    assert result.json()['errors'][0]['message'] == (
        'Syntax error in GraphQL query'
    )
    mocked_capture_exception.assert_called_with(error)

def test_graphiql_render(client: Client):
    result = client.get(reverse('graphiql'), HTTP_ACCEPT='text/html')

    assert result.status_code == OK

    result = client.get(reverse('file_graphiql'), HTTP_ACCEPT='text/html')

    assert result.status_code == OK
