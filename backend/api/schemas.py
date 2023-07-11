from drf_yasg import openapi


pk_param = openapi.Parameter(
    'id', openapi.IN_PATH, type=openapi.TYPE_INTEGER)
user_id_param = openapi.Parameter(
    'user_id', openapi.IN_PATH, type=openapi.TYPE_INTEGER)
project_id_param = openapi.Parameter(
    'project_id', openapi.IN_PATH, type=openapi.TYPE_INTEGER)
organization_id_param = openapi.Parameter(
    'organization_id', openapi.IN_PATH, type=openapi.TYPE_INTEGER)
project_id_in_query = openapi.Parameter(
    'project_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=True)
task_id_param = openapi.Parameter(
    'task_id', openapi.IN_PATH, type=openapi.TYPE_INTEGER)
current_password = openapi.Parameter(
    'current_password', openapi.IN_BODY, type=openapi.TYPE_STRING
)
