from nonebot import on_command
from nonebot import logger, get_plugin_config
import httpx
from nonebot.plugin import PluginMetadata, inherit_supported_adapters
from nonebot.params import CommandArg
from nonebot import require
require("nonebot_plugin_saa")
from nonebot_plugin_saa import Text, Image, MessageFactory
from .config import Config


__plugin_meta__ = PluginMetadata(
    name="随机毛图",
    description="基于NoneBot2进行适配的兽云随机毛图插件",
    usage="预设指令有furry、来只毛、毛毛三种指令，发送后将会调用兽云的随即图片API并返回图片及基本介绍",

    type="application",

    homepage="https://github.com/Ekac00/nonebot-plugin-RanFurryPic/",

    supported_adapters=inherit_supported_adapters("nonebot_plugin_session")
)

#读取配置
config = get_plugin_config(Config)
msg = config.ranfurrypic_msg


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

    name = pic_json["picture"]["name"]
    suggest = pic_json["picture"]["suggest"]

    #使用saa构建消息
    return pic_id_url, name, suggest, pic_id

@furry.handle()
async def handle_furry():
    pic_id_url, name, suggest, pic_id = await handle_get_pic()
    text = msg.replace('[NAME]',name).replace('[SUGGEST]',suggest).replace('[PICID]',pic_id)
    await MessageFactory([Text(text), Image(pic_id_url)]).send()
