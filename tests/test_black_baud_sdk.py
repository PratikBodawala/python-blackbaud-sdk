#!/usr/bin/env python

"""Tests for `black_baud_sdk` package."""

import pytest


from black_baud_sdk.models.EducationManagement.School.Academics.AcademicsParams import AcademicsAssignmentsBySectionParams
from black_baud_sdk.black_baud_sdk import BlackBaud


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
    bb = BlackBaud()
    data = bb.list_assignments_by_section(AcademicsAssignmentsBySectionParams(section_id=2))
    print(f'{data}')
