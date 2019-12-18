import pymysql
from nonebot import on_command, CommandSession


@on_command('search', aliases=('sh', '搜索', '查找'))
async def search(session: CommandSession):
    order = session.get('order', prompt='输入关键字')
    result = await get_website(order)
    await session.send(result)


@on_command('insert', aliases=('inst', '插入', '添加'))
async def insert(session: CommandSession):
    order = session.get('order', prompt='输入关键字')
    result = await insert_website(order)
    await session.send(result)


@search.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state['order'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('传值不能为空')

    session.state[session.current_key] = stripped_arg


@insert.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state['order'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('传值不能为空')

    session.state[session.current_key] = stripped_arg


async def get_website(order: str) -> str:
    db = pymysql.connect()
    cursor = db.cursor()
    sql = "SELECT * FROM web_collection WHERE name LIKE '%#NAME%' AND style=1"
    sql = sql.replace('#NAME', order)
    cursor.execute(sql)
    values = cursor.fetchall()
    result = ''
    for row in values:
        result = result + row[0] + "：" + row[1] + '\n'
    db.close()
    if(len(values) == 0):
        return '查询结果为空'
    return result


async def insert_website(order: str) -> str:
    items = order.split('###')
    if(len(items) < 2 or len(items) > 3):
        return '传值错误'
    if(len(items) == 2):
        items.append('1')
    # 这里简单返回一个字符串
    db = pymysql.connect()
    cursor = db.cursor()
    sql = "INSERT INTO web_collection(name, website, style) VALUES ('%s', '%s', %s)" % (
        items[0], items[1], items[2])
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
        return '插入失败'
    db.close()
    return '插入成功'
