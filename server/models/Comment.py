from mongoengine import *


class Comment(Document):
    # EFI 引用
    efi = ReferenceField('EFI', required=True)
    # 星数，满分10分
    star = IntField(required=True, default=0)
    # 评论内容
    content = StringField(required=True, default='')
    # 创建时间
    create_time = DateTimeField(required=True)
    # 是否被删除
    deleted = BooleanField(required=True, default=False)