from pydantic import BaseModel

class Config(BaseModel):
    #消息发送结果(详见README.md)
    ranfurrypic_msg: str = """
    好的嗷呜～
    毛毛名称：[NAME]
    留言：[SUGGEST]
    图片UID:[PICID]
    """