TEMPLATES = {
    'new_task': (
        'У вас новая задача:\n'
        'Проект: {task_project}\n'
        'Колонка: {task_column}\n'
        'Задача: {task_title}\n'
        'Описание: {task_description}\n'
    ),
    'deadline': (
        'У одной из ваших задач завтра дедлайн:\n'
        'Проект: {task_project}\n'
        'Колонка: {task_column}\n'
        'Задача: {task_title}\n'
        'Описание: {task_description}\n'
    ),
    'change_task': (
        'Одна из ваших задач была изменена:\n'
        'Проект: {task_project}\n'
        'Колонка: {task_column}\n'
        'Задача: {task_title}\n'
        'Описание: {task_description}\n'
    ),
    'mention': (
        'Вас упомянули в комментарии:\n'
        'Задача: {comment_task}\n'
        'Автор: {comment_author}\n'
        'Текст: {comment_text}\n'
    ),
}
