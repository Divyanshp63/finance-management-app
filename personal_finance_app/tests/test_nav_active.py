import pytest
from flask import request

# tests rely on client fixture from conftest

def check_active_class(html, url):
    # look for <a href="url" class="...">
    pattern = f'<a href="{url}"'
    # naive check for active class
    lines = html.splitlines()
    for line in lines:
        if pattern in line:
            return 'class="active"' in line
    return False


def test_dashboard_active(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert check_active_class(rv.get_data(as_text=True), '/')


def test_expense_active(client):
    rv = client.get('/expense/', follow_redirects=True)
    assert rv.status_code == 200
    assert check_active_class(rv.get_data(as_text=True), '/expense')


def test_budget_active(client):
    rv = client.get('/budget/', follow_redirects=True)
    assert rv.status_code == 200
    assert check_active_class(rv.get_data(as_text=True), '/budget')


def test_saving_active(client):
    rv = client.get('/saving/', follow_redirects=True)
    assert rv.status_code == 200
    assert check_active_class(rv.get_data(as_text=True), '/saving')


def test_investment_active(client):
    rv = client.get('/investment/', follow_redirects=True)
    assert rv.status_code == 200
    assert check_active_class(rv.get_data(as_text=True), '/investment')


def test_reports_active(client):
    rv = client.get('/reports')
    assert rv.status_code == 200
    assert check_active_class(rv.get_data(as_text=True), '/reports')
