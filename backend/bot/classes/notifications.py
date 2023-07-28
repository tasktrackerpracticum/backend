from bot.utils.templates import TEMPLATES
from bot.classes.bot import bot
from users.models import User


class Notification():

    def send(self, type=None, task=None, **kwargs):
        match type:
            case 'new_task':
                user = kwargs.get('user')
                if user and task:
                    self._send_to_user(type, user, task, None)
            case 'mention':
                comment = kwargs.get('comment')
                if comment:
                    usernames = _get_all_mentions(comment.text)
                    if usernames:
                        _send_to_users(type, usernames, comment):
            case 'change_task':
                pass
            case 'deadline':
                pass

    def _send_to_user(self, type, user, task, comment):
        bot.send_answer({
            'chat_id': user.chat_id,
            'text': self._get_text(type, task, comment)
        })

    def _send_to_users(self, type, usernames, comment):
        for username in usernames:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                pass
            self._send_to_user(type, user, comment.task, comment)

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
