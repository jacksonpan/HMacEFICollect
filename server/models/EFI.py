from mongoengine import *


class EFI(Document):
    # User 引用
    user = ReferenceField('User', required=True)
    # CPU 型号
    cpu_model = StringField(required=True, default='')
    # 主板型号
    mb_model = StringField(required=True,  default='')
    # 显卡型号
    gpu_model = StringField(required=True, default='')
    # 无线网卡型号
    wc_model = StringField(required=True, default='')
    # 用户主机配置说明
    computer_info = StringField(required=True, default='')
    # EFI下载地址
    download_url = StringField(required=True, default='')
    # EFI使用说明
    instruction_url = StringField(required=True, default='')
    # 创建时间
    create_time = DateTimeField(required=True)
    # 是否被删除
    deleted = BooleanField(required=True, default=False)