from bot.utils.templates import TEMPLATES
from bot.classes.bot import bot


class Notification():

    def send(self, type=None, user=None, task=None, comment=None):
        bot.send_answer({
            'chat_id': user.chat_id,
            'text': self._get_text(type, task, comment)
        })

    def _get_text(self, type=None, task=None, comment=None):
        if not type:
            return
        text = TEMPLATES.get('type')
        text.replace('{task_project}', task.project)
        text.replace('{task_column}', task.column)
        text.replace('{task_title}', task.title)
        text.replace('{task_description}', task.description)
        text.replace('{comment_task}', comment.task)
        text.replace('{comment_author}', comment.author)
        text.replace('{comment_text}', comment.text)
        return text


notification = Notification()
