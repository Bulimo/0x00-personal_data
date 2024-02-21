#!/usr/bin/env python3
""" End-to-end integration test module"""
import requests


def register_user(email: str, password: str) -> None:
    """ Test user is registered """
    data = {'email': email, 'password': password}
    r = requests.post('http://localhost:5000/users', data=data)
    msg = {"email": email, "message": "user created"}
    assert r.status_code == requests.codes.ok
    assert r.json() == msg


def log_in_wrong_password(email: str, password: str) -> None:
    """ Test login with incorrect credentials """
    data = {'email': email, 'password': password}
    r = requests.post('http://localhost:5000/sessions', data=data)
    assert r.status_code == 401


def log_in(email: str, password: str) -> str:
    """ Test log in with correct credentials """
    data = {'email': email, 'password': password}
    r = requests.post('http://localhost:5000/sessions', data=data)
    msg = {"email": email, "message": "logged in"}
    assert r.status_code == requests.codes.ok
    assert r.json() == msg
    session_id = r.cookies.get('session_id')
    return session_id


def profile_unlogged() -> None:
    """ Get profile if not logged in """
    cookies = {'session_id': ''}
    r = requests.get('http://localhost:5000/profile', cookies=cookies)
    assert r.status_code == 403


def profile_logged(session_id: str) -> None:
    """ Get profile for logged in user """
    cookies = {'session_id': session_id}
    r = requests.get('http://localhost:5000/profile', cookies=cookies)
    assert r.status_code == 200


def log_out(session_id: str) -> None:
    """ test logout function """
    cookies = {'session_id': session_id}
    r = requests.delete('http://localhost:5000/sessions', cookies=cookies)
    assert r.status_code == 200
    msg = {"message": "Bienvenue"}
    assert r.json() == msg


def reset_password_token(email: str) -> str:
    """ Test reset password method """
    data = {'email': email}
    r = requests.post('http://localhost:5000/reset_password', data=data)
    token = r.json().get('reset_token')
    msg = {"email": email, "reset_token": token}
    assert r.status_code == 200
    assert r.json() == msg
    return token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ Test password reset """
    data = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password
    }
    r = requests.put('http://localhost:5000/reset_password', data=data)
    msg = {"email": email, "message": "Password updated"}
    assert r.status_code == 200
    assert r.json() == msg


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
