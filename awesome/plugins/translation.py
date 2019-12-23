from nonebot import on_command, CommandSession
import hashlib
import random
import openpyxl
from openpyxl import Workbook
import requests


# set baidu develop parameter
apiurl = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
appid = '20191216000366578'
secretKey = 'i3pjXzZIbB4rXcZdbKcW'


@on_command('transla_en', aliases=('en', '英文'))
async def transla_en(session: CommandSession):
    content = session.get('content', prompt='说，你想翻译什么内容？')
    result = await get_translation_of_content(content)
    await session.send(result)


@on_command('transla_zh', aliases=('zh', '中文'))
async def transla_zh(session: CommandSession):
    content = session.get('content', prompt='说，你想翻译什么内容？')
    result = await get_translation_of_content(content, fromLang='zh', toLang='en')
    await session.send(result)


@transla_zh.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        if stripped_arg:
            session.state['content'] = stripped_arg
        return
    if not stripped_arg:
        session.pause('nmsl，浪费我的流量')
    session.state[session.current_key] = stripped_arg


@transla_en.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        if stripped_arg:
            session.state['content'] = stripped_arg
        return
    if not stripped_arg:
        session.pause('nmsl，浪费我的流量')
    session.state[session.current_key] = stripped_arg


async def get_translation_of_content(content: str, fromLang='en', toLang='zh') -> str:
    result = translateBaidu(content, fromLang, toLang)
    return f'{result}'


def translateBaidu(content, fromLang='en', toLang='zh'):
    salt = str(random.randint(32768, 65536))
    sign = appid + content + salt + secretKey
    sign = hashlib.md5(sign.encode("utf-8")).hexdigest()

    try:
        paramas = {
            'appid': appid,
            'q': content,
            'from': fromLang,
            'to': toLang,
            'salt': salt,
            'sign': sign
        }
        response = requests.get(apiurl, paramas)
        jsonResponse = response.json()  # 获得返回的结果，结果为json格式
        dst = str(jsonResponse["trans_result"]
                  [0]["dst"])  # 取得翻译后的文本结果
        return dst
    except Exception as e:
        print(e)
