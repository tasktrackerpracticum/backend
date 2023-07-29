import contextlib

import jinja2
from users.models import User

from bot.classes.bot import tgbot
from bot.config import config


class Notification():

    def send(self, type=None, task=None, **kwargs):
        """Рассылаем оповещения разных типов."""
        match type:
            case 'new_task' | 'deadline':
                user = kwargs.get('user')
                if task and user:
                    self._send_to_user(type, user, task, None)
            case 'mention':
                if comment := kwargs.get('comment'):
                    self._send_to_usernames(type, comment)
            case 'change_task':
                if task:
                    self._send_to_users(type, task)

    def _send_to_user(self, type, user, task, comment):
        """Посылаем сообщение юзеру в бот."""
        if user.chat_id:
            text = self._get_text(type, {'task': task, 'comment': comment})
            tgbot.send_answer({
                'chat_id': user.chat_id,
                'text': text
            })

    def _send_to_usernames(self, type, comment):
        """Получаем пользователей по username и отсылаем им сообщения."""
        if usernames := self._get_all_mentions(comment.text):
            for username in usernames:
                with contextlib.suppress(User.DoesNotExist):
                    user = User.objects.get(username=username)
                self._send_to_user(type, user, None, comment)

    def _get_all_mentions(self, text):
        """Получаем упоминания в тексте комментария."""
        mentions = list(filter(lambda x: x.startswith('@'), text.split()))
        for count in range(len(mentions)):
            mentions[count] = mentions[count][1:]
        return mentions

    def _send_to_users(self, type, task):
        """Рассылаем сообщения всем участникам задачи."""
        if users := task.users.all():
            for user in users:
                self._send_to_user(type, user, task, None)

    def _get_template_env(self):
        """Получаем шаблон сообщения."""
        if not getattr(self._get_template_env, 'template_env', None):
            template_loader = jinja2.FileSystemLoader(
                searchpath=config.TEMPLATES_DIR)
            env = jinja2.Environment(
                loader=template_loader,
                trim_blocks=True,
                lstrip_blocks=True,
                autoescape=True,
            )

            self._get_template_env.template_env = env

        return self._get_template_env.template_env

    def _get_text(self, type: str, data: dict):
        """Рендерим шаблон сообщения."""
        if not type or not data:
            return
        template = self._get_template_env().get_template(type)
        return template.render(**data)


notification = Notification()
