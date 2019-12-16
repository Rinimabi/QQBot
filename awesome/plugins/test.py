from nonebot import on_command, CommandSession
from os import path

@on_command('test', aliases=('测试', '试试', '测一测'))
async def weather(session: CommandSession):
    path = '../../image/man.jpg'
    report = '[CQ:image,file={path}]'
    await session.send(report)
