from mongoengine import *
import json
import collections

Info = {'addr': '127.0.0.1',
        'port': 27017,
        'database': 'Sina'}


class UserInfo(Document):
    """ 个人信息 """
    _id = StringField()  # 用户ID
    NickName = StringField()  # 昵称
    Gender = StringField()  # 性别
    Province = StringField()  # 所在省
    City = StringField()  # 所在城市
    Signature = StringField()  # 个性签名
    Birthday = DateTimeField()  # 生日
    Num_Tweets = IntField()  # 微博数
    Num_Follows = IntField()  # 关注数
    Num_Fans = IntField()  # 粉丝数
    Sex_Orientation = StringField()  # 性取向
    Marriage = StringField()  # 婚姻状况
    URL = StringField()  # 首页链接
    meta = {'collection': 'Information'}

    def get_id(self):
        return self._id


class Fans(DynamicDocument):
    """粉丝信息"""
    _id = StringField()
    meta = {'collection': 'Fans'}

    def get_id(self):
        return self._id

    def get_items(self):
        """返回所有Fans的列表，第一个值是_id"""
        items = [self._id]
        for i in range(1, 200):
            try:
                items.append(self[str(i)])
            except KeyError:
                break
        return items


class Follows(DynamicDocument):
    """关注的人信息"""
    _id = StringField()
    meta = {'collection': 'Follows'}

    def get_id(self):
        return self._id

    def get_items(self):
        """返回所有Follows的列表，第一个值是_id"""
        items = [self._id]
        for i in range(1, 200):
            try:
                items.append(self[str(i)])
            except KeyError:
                break
        return items


class Tweets(Document):
    """ 微博信息 """
    _id = StringField()  # 用户ID-微博ID
    ID = StringField()  # 用户ID
    Content = StringField()  # 微博内容
    PubTime = DateTimeField()  # 发表时间
    Co_oridinates = StringField()  # 定位坐标
    Tools = StringField()  # 发表工具/平台
    Like = IntField()  # 点赞数
    Comment = IntField()  # 评论数
    Transfer = IntField()  # 转载数

    def get_id(self):
        return self._id


if __name__ == '__main__':
    connect(
        Info['database'],
        host=Info['addr'],
        port=Info['port'],
    )
    fanfan = open("newfans", "w+")
    for fan in Fans.objects:
        itemList = fan.get_items()
        dump = collections.OrderedDict()
        i = 1
        dump['_id'] = fan.get_id()
        for item in itemList[1:]:
            if not UserInfo.objects(_id=item):
                itemList.remove(item)
                continue
            dump[str(i)] = item
            i += 1
            # fanlist.append(json.dumps(dump))
        json.dump(dump, fanfan)
        fanfan.write('\n')
    fanfan.close()
    fol = open("newfollows", "w+")
    for foll in Follows.objects:
        itemList = foll.get_items()
        dump = collections.OrderedDict()
        i = 1
        dump['_id'] = foll.get_id()
        for item in itemList[1:]:
            if not UserInfo.objects(_id=item):
                itemList.remove(item)
                continue
            dump[str(i)] = item
            i += 1
            # fanlist.append(json.dumps(dump))
        json.dump(dump, fol)
        fanfan.write('\n')
    fol.close()
