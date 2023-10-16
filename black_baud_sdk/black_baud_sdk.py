"""Main module."""
import base64
import json
import os
import time
from dataclasses import asdict
from .models.EducationManagement.School.Academics.AcademicsParams import AcademicsAssignmentsBySectionParams
from .models.EducationManagement.School.Academics.AcademicsParams import AcademicsAssignmentsBySectionResponse
from .utils.session import BlackBaudSession
from .exception import InvalidConfiguration
from .utils.singleton import SingletonMeta


class BlackBaud(metaclass=SingletonMeta):
    def __init__(self, subscription_key=None, host='api.sky.blackbaud.com', version='v1'):
        self.expire = 0
        self._access_token = None
        self._refresh_token = None
        self._subscription_key = subscription_key or os.getenv('BLACKBAUD_SUBSCRIPTION_KEY')
        if not self._subscription_key:
            raise InvalidConfiguration(
                'subscription_key must be provided or set as an environment variable: BLACKBAUD_SUBSCRIPTION_KEY')
        self.host = host
        self.version = version
        self._session = BlackBaudSession(self._subscription_key)
        self.get_access_token()

    def get_access_token(self):
        if os.path.isfile('/tmp/.blackbaud_access_token'):
            with open('/tmp/.blackbaud_access_token', 'r') as f:
                self._access_token = f.read()
                try:
                    if json.loads(base64.b64decode(self._access_token.split('.')[1]))['exp'] > time.time():
                        self._session.headers['Authorization'] = f'Bearer {self._access_token}'
                        return self._access_token
                except Exception:
                    pass
        if os.path.isfile('/tmp/.blackbaud_refresh_token'):
            with open('/tmp/.blackbaud_refresh_token', 'r') as f:
                self._refresh_token = f.read()

        data = {
            "client_id": os.getenv("BLACKBAUD_CLIENT_ID"),
            "client_secret": os.getenv("BLACKBAUD_CLIENT_SECRET"),
            "refresh_token": self._refresh_token or os.getenv('BLACKBAUD_REFRESH_TOKEN'),
            "grant_type": "refresh_token",
        }

        response = self._session.post(url="https://oauth2.sky.blackbaud.com/token", data=data)
        if not response.ok:
            raise response.raise_for_status()
        output = response.json()
        self._access_token = output["access_token"]
        self._session.headers['Authorization'] = f'Bearer {self._access_token}'
        with open('/tmp/.blackbaud_access_token', 'w') as f:
            f.write(self._access_token)
        with open('/tmp/.blackbaud_refresh_token', 'w') as f:
            f.write(output['refresh_token'])
        return self._access_token

    def list_assignments_by_section(self, params: AcademicsAssignmentsBySectionParams) -> \
            AcademicsAssignmentsBySectionResponse:
        if (output := self._session.get(
            f'https://{self.host}/school/{self.version}/academics/sections/{params.section_id}/assignments',
            params=asdict(params)
        )).ok:
            return AcademicsAssignmentsBySectionResponse(**output.json())
        else:
            output.raise_for_status()
