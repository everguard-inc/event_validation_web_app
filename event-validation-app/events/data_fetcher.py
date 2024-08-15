import json
import os

import requests
from celery.utils.log import get_task_logger
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from events.models import Event, Project
from utils.exceptions import TokenNotFoundError, TokenRequestError


logger = get_task_logger(__name__)


class DataFetcher:

    _EVENT_LINK_BASE_URL = os.environ.get("EVENT_LINK_BASE_URL", 'https://www.sentri360.ai')
    _USERNAME = os.environ.get("EVENTS_USERNAME", 'test')
    _PASSWORD = os.environ.get("EVENTS_PASSWORD", 'pwd')

    def __init__(self, url):
        self.url = url
        self.access_token = None
        self.refresh_token = None
        self.end_datetime = timezone.now()
        self.start_datetime = self.end_datetime - timezone.timedelta(days=2)


    @property
    def username(self):
        return self._USERNAME

    @property
    def password(self):
        return self._PASSWORD

    @property
    def headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}"
        }

    def get_default_params(self) -> dict:
        return {
            'start_datetime': self.start_datetime,
            'end_datetime': self.end_datetime
        }

    def build_url(self, path: str) -> str:
        return f'{self.url}/{path}'

    def build_event_link(self, uid) -> str:
        return f'{self._EVENT_LINK_BASE_URL}/{uid}/'

    def token_obtain(self) -> None:
        token_url = self.build_url('api/token/')
        response = requests.post(url=token_url, data={'username': self.username, 'password': self.password})

        if response.status_code == 200:
            access_token = response.json().get('access')
            refresh_token = response.json().get('refresh')
            self.access_token, self.refresh_token = access_token, refresh_token
            if not access_token:
                raise TokenNotFoundError('Access token not found in the response')

        else:
            raise TokenRequestError(f'Token request failed with status code: {response.status_code}')

        self.access_token, self.refresh_token = access_token, refresh_token

    def fetch_data(self, project_name: str) -> list:
        events_url = self.build_url('api/get_events')
        params = self.get_default_params()
        params.update({'project_name': project_name})

        response = requests.get(events_url, params=params, headers=self.headers)
        data = response.json()

        return data

    def get_existed_events_uids(self) -> set:
        event_uids_set = set(
            Event.objects.filter(datetime__range=[self.start_datetime, self.end_datetime]).values_list('uid', flat=True)
        )
        return event_uids_set

    def migrate_data(self, data: list) -> None:
        existed_events_uids = self.get_existed_events_uids()

        for item in data:
            if item.get('uid') in existed_events_uids:
                continue

            if datetime := item.get('datetime'):
                parsed_datetime = parse_datetime(datetime)
                datetime = parsed_datetime if timezone.is_aware(parsed_datetime) else timezone.make_aware(parsed_datetime)

            event_uid = item.get('uid')
            link = self.build_event_link(event_uid)

            event_obj = Event(
                datetime=datetime,
                link=link,
                uid=event_uid,
                cam_uid=item.get('cam_uid'),
                zone_uid=item.get('zone_uid'),
                area_uid=item.get('area_uid'),
                portal_comment=item.get('comment'),
                portal_status=item.get('status'),
            )
            event_obj.save()

    def process_migration(self) -> None:

        self.token_obtain()  # Obtain tokens
        projects_list = Project.objects.values_list('name', flat=True)

        for project_name in projects_list:
            try:
                data = self.fetch_data(project_name)
                self.migrate_data(data)

            except Exception as e:
                logger.info(f'Migration Failed: Project - {project_name}; Error: {e}')
