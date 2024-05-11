from nonebot.plugin import on_command
from nonebot import logger
from nonebot.adapters.onebot.v11 import MessageSegment
import httpx
from nonebot.plugin import PluginMetadata
from nonebot.adapters import Message
from nonebot.params import CommandArg

__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-RanFurryPic",
    description="基于NoneBot2进行适配的兽云随机毛图插件",
    usage="预设指令有furry、来只毛、毛毛三种指令，发送后将会调用兽云的随即图片API并返回图片及基本介绍",

    type="application",
    # 发布必填，当前有效类型有：`library`（为其他插件编写提供功能），`application`（向机器人用户提供功能）。

    homepage="https://github.com/Ekac00/nonebot-plugin-RanFurryPic/",
    # 发布必填。

    supported_adapters={"~onebot.v11"},
    # 支持的适配器集合，其中 `~` 在此处代表前缀 `nonebot.adapters.`，其余适配器亦按此格式填写。
    # 若插件可以保证兼容所有适配器（即仅使用基本适配器功能）可不填写，否则应该列出插件支持的适配器。
)

furry = on_command("来只毛", aliases={"毛毛", "furry"}, priority=9, block=True)

async def handle_get_pic():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    # 发送图片ID请求
    id_url = "https://cloud.foxtail.cn/api/function/random?name=&type="
    pic_id = ""
    async with httpx.AsyncClient() as client:
        id_response = await client.get(id_url, headers=headers)
        if id_response.status_code == 200:
            pic_json = id_response.json()
            pic_id = pic_json["picture"]["picture"]
            logger.success(f"状态码：{id_response.status_code}\n原始内容：{id_response.text}\n图片ID:{pic_id}")
        else:
            logger.error(f"请求失败！\n状态码：{id_response.status_code}")
            return f"请求失败！\n状态码：{id_response.status_code}"

    # 发送图片请求
    pic_url = "https://cloud.foxtail.cn/api/function/pictures?picture=" + pic_id
    pic_id_url = ""
    async with httpx.AsyncClient() as client:
        pic_response = await client.get(pic_url, headers=headers)
        if pic_response.status_code == 200:
            url_json = pic_response.json()
            pic_id_url = url_json["url"]
            logger.success(f"状态码：{pic_response.status_code}\n原始内容：{pic_response.text}\n图片url:{pic_id_url}")
        else:
            logger.error(f"请求失败！\n状态码：{pic_response.status_code}")
            return f"请求失败！\n状态码：{pic_response.status_code}"

    # 发送图片
    name = pic_json["picture"]["name"]
    suggest = pic_json["picture"]["suggest"]
    return MessageSegment.image(pic_id_url) + f"好的嗷呜～\n毛毛名称：{name}\n留言：{suggest}\n图片UID:{pic_id}"

@furry.handle()
async def handle_furry():
    result = await handle_get_pic()
    await furry.finish(result)

furry_check = on_command("来只", priority=10, block=True)

@furry_check.handle()
async def handle_get_pic(args: Message = CommandArg()):
    location = args.extract_plain_text()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    # 发送图片ID请求
    id_url = "https://cloud.foxtail.cn/api/function/random?name=" + location
    pic_id = ""
    async with httpx.AsyncClient() as client:
        id_response = await client.get(id_url, headers=headers)
        if id_response.status_code == 200:
            pic_json = id_response.json()
            pic_id = pic_json["picture"]["picture"]
            logger.success(f"状态码：{id_response.status_code}\n原始内容：{id_response.text}\n图片ID:{pic_id}")
        else:
            logger.error(f"请求失败！
状态码：{id_response.status_code}")
            return f"请求失败！
状态码：{id_response.status_code}"

    # 发送图片请求
    pic_url = "https://cloud.foxtail.cn/api/function/pictures?picture=" + pic_id
    pic_id_url = ""
    async with httpx.AsyncClient() as client:
        pic_response = await client.get(pic_url, headers=headers)
        if pic_response.status_code == 200:
            url_json = pic_response.json()
            pic_id_url = url_json["url"]
            logger.success(f"状态码：{pic_response.status_code}\n原始内容：{pic_response.text}\n图片url:{pic_id_url}")
        else:
            logger.error(f"请求失败！\n状态码：{pic_response.status_code}")
            return f"请求失败！\n状态码：{pic_response.status_code}"

    # 发送图片
    name = pic_json["picture"]["name"]
    suggest = pic_json["picture"]["suggest"]
    return MessageSegment.image(pic_id_url) + f"好的嗷呜～\n毛毛名称：{name}\n留言：{suggest}\n图片UID:{pic_id}"

@furry_check.handle()
async def handle_furry_check(args: Message = CommandArg()):
    result = await handle_get_pic(args)
    await furry_check.finish(result)
