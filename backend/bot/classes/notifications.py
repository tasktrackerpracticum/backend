import contextlib

import jinja2

from bot.classes.bot import tg_bot
from bot.config import config
from tasks.models import Comment, Task
from users.models import User


def _get_template_env():
    """Получаем шаблон сообщения."""
    if not getattr(_get_template_env, 'template_env', None):
        template_loader = jinja2.FileSystemLoader(
            searchpath=config.TEMPLATES_DIR)
        env = jinja2.Environment(
            loader=template_loader,
            trim_blocks=True,
            lstrip_blocks=True,
            autoescape=True,
        )
        _get_template_env.template_env = env
    return _get_template_env.template_env


class Notification():
    """Notification class."""

    def send(
        self, type_: str | None = None, task: Task | None = None, **kwargs,
    ) -> None:
        """Рассылаем оповещения разных типов."""
        match type_:
            case 'new_task' | 'deadline':
                user = kwargs.get('user')
                if task and user:
                    self._send_to_user(type_, user, task, None)
            case 'mention':
                if comment := kwargs.get('comment'):
                    self._send_to_usernames(type_, comment)
            case 'change_task':
                if task:
                    self._send_to_users(type_, task)

    def _send_to_user(
        self, type_: str, user: User, task: Task, comment: Comment,
    ) -> None:
        """Посылаем сообщение юзеру в бот."""
        if user.chat_id:
            text = self._get_text(type_, {'task': task, 'comment': comment})
            tg_bot.send_answer({
                'chat_id': user.chat_id,
                'text': text,
            })

    def _send_to_usernames(self, type_: str, comment: Comment) -> None:
        """Получаем пользователей по username и отсылаем им сообщения."""
        if usernames := self._get_all_mentions(comment.text):
            for username in usernames:
                with contextlib.suppress(User.DoesNotExist):
                    user = User.objects.filter(username=username)
                if user.exists():
                    self._send_to_user(type_, user[0], None, comment)

    def _get_all_mentions(self, text: str) -> list[str]:
        """Получаем упоминания в тексте комментария."""
        mentions = list(filter(lambda x: x.startswith('@'), text.split()))
        for count in range(len(mentions)):
            mentions[count] = mentions[count][1:]
        return mentions

    def _send_to_users(self, type_: str, task: Task) -> None:
        """Рассылаем сообщения всем участникам задачи."""
        for user in task.users.all():
            self._send_to_user(type_, user, task, None)

    def _get_text(self, type_: str, data: dict[str, Task | Comment]):
        """Рендерим шаблон сообщения."""
        if not type_ or not data:
            return
        template = _get_template_env().get_template(f'{type_}.j2')
        return template.render(**data)


notification = Notification()
