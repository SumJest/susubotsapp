import json
import traceback
import typing
from datetime import datetime
from django.contrib.sessions.models import Session

from .models import Bot, CustomUser, Token, Task

from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt


# CustomUser = settings.AUTH_USER_MODEL

def is_ingroup(user: CustomUser, group_name: str):
    return user.groups.filter(name=group_name).exists()


class APIpost:
    @staticmethod
    def task(**kwargs):
        if 'token' not in kwargs.keys():
            return {"ok": False, "reason": "You should specify your token"}
        bot: Bot = None
        token = None

        token_name = kwargs['token'][0]
        bot_name = kwargs['name'][0]
        try:
            token = Token.objects.get(name=token_name)
            if not token.is_supertoken:
                return {"ok": False, "reason": "Permission denied!"}
            bot = Bot.objects.get(name=bot_name)
        except Exception as ex:
            print(traceback.format_exc())
        if bot is None:
            return {"ok": False, "reason": "Bad request data token or bot"}

        data = None
        if 'data' in kwargs.keys():
            data = kwargs['data']

        if 'task_name' in data.keys():
            task_name = data['task_name']

            tasks_raw = Task.objects.filter(name=task_name, to_bot=bot)

            if not tasks_raw.count():
                return {"ok": False, "reason": "Task Not Found"}
        else:
            return {"ok": False, "reason": "You should put task"}

        # if 'received' in data.keys():
        #     received = data['received']
        #     if received:
        #         task.delivered = True
        #         task.save()

        if 'completed' in data.keys():
            completed = data['completed']
            if completed:
                for task in tasks_raw:
                    task.delete()

        return {"ok": True}

    @staticmethod
    def botStatus(**kwargs):
        if 'token' not in kwargs.keys():
            return {"ok": False, "reason": "You should specify your token"}
        if 'name' not in kwargs.keys():
            return {"ok": False, "reason": "Wrong parameters."}

        bot: Bot = None
        data = kwargs['data']
        token_name = kwargs['token'][0]
        bot_name = kwargs['name'][0]
        try:
            token = Token.objects.get(name=token_name)
            if not token.is_supertoken:
                return {"ok": False, "reason": "Permission denied!"}
            bot = Bot.objects.get(name=bot_name)
        except Exception as ex:
            pass
        if bot is None:
            return {"ok": False, "reason": "Bad request data token or bot"}

        if 'status' not in data.keys():
            return {"ok": False, "reason": "No status data"}
        status = data['status']

        bot.status = status
        bot.last_update = datetime.now().timestamp()
        bot.save()

        return {"ok": True}

    @staticmethod
    def createtask(**kwargs):
        if 'session_id' not in kwargs.keys() and 'token' not in kwargs.keys():
            return {"ok": False, "reason": "You should specify your token"}
        if 'bot_name' not in kwargs.keys():
            return {"ok": False, "reason": "Wrong parameters."}

        bot_name: str = kwargs['bot_name'][0]
        bot: Bot = None
        token = None
        if 'token' in kwargs.keys():

            token_name = kwargs['token'][0]
            try:
                token = Token.objects.get(name=token_name)
                bot_object = None
                if token.is_supertoken:
                    bot_object = Bot.objects
                else:
                    bot_object = token.bots

                bot = bot_object.get(name=bot_name)
            except Exception:
                return {"ok": False, "reason": "Bad bot_name or api token"}

        elif 'session_id' in kwargs.keys():
            try:
                session_data = Session.objects.get(session_key=kwargs['session_id']).get_decoded()
                user = CustomUser.objects.get(id=session_data['_auth_user_id'])
                bot_object = None
                if user.is_superuser or is_ingroup(user, "Admin"):
                    bot_object = Bot.objects
                else:
                    bot_object = user.bots

                bot = bot_object.get(name=bot_name)
            except Exception:
                return {"ok": False, "reason": "Bad request"}

        if "data" not in kwargs.keys():
            return {"ok": False, "reason": "No data"}
        data = kwargs['data']

        if 'task' not in data.keys():
            return {"ok": False, "reason": "No task"}

        taskname = data['task']
        task = Task.objects.create(name=taskname, to_bot=bot)
        task.save()
        return {'ok': True}


class APIget:
    @staticmethod
    def gettime(**kwargs):
        return {"ok": True,
                "result": {
                    "time": datetime.now().timestamp()
                }}

    @staticmethod
    def bot_update(**kwargs):
        if 'session_id' not in kwargs.keys() and 'token' not in kwargs.keys():
            return {"ok": False, "reason": "You should specify your token"}
        if 'bot_name' not in kwargs.keys():
            return {"ok": False, "reason": "Wrong parameters."}

        bot_name: str = kwargs['bot_name'][0]
        bot: Bot = None
        token = None
        if 'token' in kwargs.keys():

            token_name = kwargs['token'][0]
            try:
                token = Token.objects.get(name=token_name)
                bot_object = None
                if token.is_supertoken:
                    bot_object = Bot.objects
                else:
                    bot_object = token.bots

                bot = bot_object.get(name=bot_name)
            except Exception:
                print(traceback.format_exc())
                return {"ok": False, "reason": "Bad bot_name or api token"}

        elif 'session_id' in kwargs.keys():
            try:
                session_data = Session.objects.get(session_key=kwargs['session_id']).get_decoded()
                user = CustomUser.objects.get(id=session_data['_auth_user_id'])
                bot_object = None
                if user.is_superuser or is_ingroup(user, "Admin"):
                    bot_object = Bot.objects
                else:
                    bot_object = user.bots

                bot = bot_object.get(name=bot_name)
            except Exception:
                return {"ok": False, "reason": "Bad request"}

        tasks = Task.objects.filter(to_bot=bot)
        bot.last_update = datetime.now().timestamp()
        bot.save()
        tasks_list = []
        for task in tasks:
            if task.delivered or task.completed:
                continue
            tasks_list.append(task.get_dict())
            task.sended = True
            task.save()
        response = {"ok": True, "tasks": tasks_list}
        return response

    @staticmethod
    def getbot(**kwargs):
        if 'session_id' not in kwargs.keys() and 'token' not in kwargs.keys():
            return {"ok": False, "reason": "You should specify your token"}
        if 'name' not in kwargs.keys():
            return {"ok": False, "reason": "Wrong parameters."}

        bot_name: str = kwargs['name'][0]

        bot: Bot = None

        if 'token' in kwargs.keys():

            token_name = kwargs['token'][0]
            try:
                token = Token.objects.get(name=token_name)
                bot_object = None
                if token.is_supertoken:
                    bot_object = Bot.objects
                else:
                    bot_object = token.bots

                bot = bot_object.get(name=bot_name)
            except Exception:
                print(traceback.format_exc())
                return {"ok": False, "reason": "Bad bot name or api token"}

        elif 'session_id' in kwargs.keys():
            try:
                session_data = Session.objects.get(session_key=kwargs['session_id']).get_decoded()
                user = CustomUser.objects.get(id=session_data['_auth_user_id'])
                bot_object = None
                if user.is_superuser or is_ingroup(user, "Admin"):
                    bot_object = Bot.objects
                else:
                    bot_object = user.bots

                bot = bot_object.get(name=bot_name)
            except Exception:
                return {"ok": False, "reason": "Bad request"}

        response = {"ok": True}
        response.update({'result': bot.get_dict('name', 'last_update')})
        return response

    @staticmethod
    def getbots(**kwargs):
        if 'session_id' not in kwargs.keys() and 'token' not in kwargs.keys():
            return {"ok": False, "reason": "You should specify your token"}
        bots = Bot.objects.none()
        if 'token' in kwargs.keys():

            token_name = kwargs['token'][0]
            try:
                token = Token.objects.get(name=token_name)
                if token.is_supertoken:
                    bots = Bot.objects.all()
                else:
                    bots = token.bots.all()
            except Exception:
                print(traceback.format_exc())
                return {"ok": False, "reason": "Bad token"}

        elif 'session_id' in kwargs.keys():
            try:
                session_data = Session.objects.get(session_key=kwargs['session_id']).get_decoded()
                user = CustomUser.objects.get(id=session_data['_auth_user_id'])
                if user.is_superuser or is_ingroup(user, "Admin"):
                    bots = Bot.objects.all()
                else:
                    bots = user.bots.all()
            except Exception:
                return {"ok": False, "reason": "Bad request"}
        bot_list = []
        for bot in bots:
            bot_list.append(bot.get_dict('name', 'last_update', 'status'))
        response = {"ok": True, "result": bot_list}
        return response

    @staticmethod
    def getUpdates(**kwargs):
        if 'session_id' not in kwargs.keys() and 'token' not in kwargs.keys():
            return {"ok": False, "reason": "You should specify your token"}

        if 'token' in kwargs.keys():
            token_name = kwargs['token']
            token = None
            try:
                token = Token.objects.get(name=token_name[0])
            except Exception:
                pass
            if token is None:
                return {"ok": False, "reason": "Invalid token"}
            if not token.is_supertoken:
                return {"ok": False, "reason": "Permission denied"}
        elif 'session_id' in kwargs.keys():
            try:
                session_data = Session.objects.get(session_key=kwargs['session_id']).get_decoded()
                user = CustomUser.objects.get(id=session_data['_auth_user_id'])
                if not user.is_superuser and not is_ingroup(user, "Admin"):
                    return {"ok": False, "reason": "Permission denied"}
            except Exception:
                return {"ok": False, "reason": "Bad request"}

        tasks = Task.objects.filter(sended=False)
        response_data = []
        for task in tasks:
            response_data.append(task.get_dict())
            task.sended = True
            task.save()
        return {"ok": True, "response": response_data}


# Create your views here.
@csrf_exempt
def api(request: HttpRequest, function: str):
    to_call: typing.Callable = None
    session_id = None
    try:
        session_id = request.COOKIES['sessionid']
    except Exception:
        pass
    try:
        if request.method == 'GET':
            to_call = getattr(APIget, function)
            data = to_call(session_id=session_id, **request.GET)
        elif request.method == 'POST' and request.content_type == "application/json":
            to_call = getattr(APIpost, function)
            data = to_call(session_id=session_id, **request.GET, data=json.loads(request.body))
    except:
        print(traceback.format_exc())

    if to_call is None:
        return JsonResponse({"ok": False,
                             "error_code": 404,
                             "description": "Function not found"})
    return JsonResponse(data)
