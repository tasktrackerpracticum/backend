from bot.utils.templates import TEMPLATES
from bot.classes.bot import bot
from users.models import User


class Notification():

    def send(self, type=None, task=None, **kwargs):
        match type:
            case 'new_task':
                user = kwargs.get('user')
                if task and user:
                    self._send_to_user(type, user, task, None)
            case 'mention':
                if comment := kwargs.get('comment'):
                    if usernames := self._get_all_mentions(comment.text)
                        self._send_to_usernames(type, usernames, comment):
            case 'change_task':
                users = task.users.all()
                if task and users:
                    self._send_to_users(type, users, task):
            case 'deadline':
                pass

    def _send_to_user(self, type, user, task, comment):
        if user.chat_id:
            bot.send_answer({
                'chat_id': user.chat_id,
                'text': self._get_text(type, task, comment)
            })

    def _send_to_usernames(self, type, usernames, comment):
        for username in usernames:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                pass
            self._send_to_user(type, user, None, comment)

    def _send_to_users(self, type, users, task):
        for user in users:
            self._send_to_user(type, user, task, None)

    def _get_text(self, type, task, comment):
        if not type:
            return
        text = TEMPLATES.get('type')
        if task:
            text.replace('{task_project}', task.project)
            text.replace('{task_column}', task.column)
            text.replace('{task_title}', task.title)
            text.replace('{task_description}', task.description)
        if comment:
            text.replace('{comment_task}', comment.task)
            text.replace('{comment_author}', comment.author)
            text.replace('{comment_text}', comment.text)
        return text

    def _get_all_mentions(text):
        mentions = list(filter(lambda x: x.startswith('@'), text.split()))
        for count in range(len(mentions)):
            mentions[count] = mentions[count][1:]
        return mentions


notification = Notification()
