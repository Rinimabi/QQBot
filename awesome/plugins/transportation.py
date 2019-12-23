import requests
import json
from nonebot import on_command, CommandSession

way_url = 'http://api.map.baidu.com/directionlite/v1/transit'
search_url = 'http://api.map.baidu.com/place/v2/search'
ak = 'M4jyogC1C6iZnbIcF3pt7jx7fYkhS4UW'


@on_command('transportation', aliases=('way', 'road', '路线'))
async def transportation(session: CommandSession):
    order = session.get('order', prompt='输入关键字')
    result = await get_transportation(order)
    await session.send(result)


@transportation.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state['order'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('传值不能为空')

    session.state[session.current_key] = stripped_arg


async def get_transportation(order: str) -> str:
    items = order.split('###')
    if(len(items) < 2 or len(items) > 3):
        return '传值错误'
    if(len(items) == 2):
        result = get_way(items[0], items[1])
    if(len(items) == 3):
        result = get_way(items[0], items[1], items[2])
    return result


def get_way(start, end, region='广州'):
    try:
        paramas = {
            'origin': get_start_position(start, region),
            'destination': get_end_position(end, region),
            'ak': ak,
        }
        response = requests.get(way_url, paramas)
        jsonResponse = response.json()  # 获得返回的结果，结果为json格式
        result = ""
        for route in jsonResponse["result"]["routes"]:
            result += "路线：\n"
            for step in route["steps"]:
                result += "   "+str(step[0]["instruction"])+"\n"
            result += "\n"
        return result
    except Exception as e:
        print(e)


def get_start_position(address, region):
    try:
        paramas = {
            'query': address,
            'region': region,
            'output': 'json',
            'ak': ak,
        }
        response = requests.get(search_url, paramas)
        jsonResponse = response.json()  # 获得返回的结果，结果为json格式
        position = str(jsonResponse["results"][0]["location"]["lat"]) + ","\
            + str(jsonResponse["results"][0]["location"]["lng"])
        return position
    except Exception as e:
        print(e)


def get_end_position(address, region):
    try:
        paramas = {
            'query': address,
            'region': region,
            'output': 'json',
            'ak': ak,
        }
        response = requests.get(search_url, paramas)
        jsonResponse = response.json()  # 获得返回的结果，结果为json格式
        position = str(jsonResponse["results"][0]["location"]["lat"]) + ","\
            + str(jsonResponse["results"][0]["location"]["lng"])
        return position
    except Exception as e:
        print(e)
