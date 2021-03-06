# -*- coding:utf-8

from flask import Flask, request, redirect, url_for
from mongoengine import *
import json
import re

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
    def to_json(self):
        d = {
            "_id": str(self._id),
            "NickName": self.NickName
        }
        if not self.Gender is None:
            d["Gender"] = self.Gender
        if not self.Province is None:
            d["Province"] = self.Province
        if not self.City is None:
            d["City"] = self.City
        if not self.Signature is None:
            d["Signature"] = self.Signature
        if not self.Birthday is None:
            d["Birthday"] = self.Birthday.isoformat()
        if not self.Num_Tweets is None:
            d["Num_Tweets"] = self.Num_Tweets
        if not self.Num_Follows is None:
            d["Num_Follows"] = self.Num_Follows
        if not self.Num_Fans is None:
            d["Num_Fans"] = self.Num_Fans
        if not self.Marriage is None:
            d["Marriage"] = self.Marriage
        if not self.URL is None:
            d["URL"] = self.URL
        return d


class Tweets(Document):
    """ 微博信息 """
    _id = StringField()  # 用户ID-微博ID
    ID = StringField()  # 用户ID
    Content = StringField()  # 微博内容
    PubTime = StringField()  # 发表时间
    Co_oridinates = StringField()  # 定位坐标
    Tools = StringField()  # 发表工具/平台
    Like = IntField()  # 点赞数
    Comment = IntField()  # 评论数
    Transfer = IntField()  # 转载数
    meta = {'collection': 'Tweets'}

    def to_json(self):
        datepat1 = re.compile(u'今天 (.*)')
        datepat2 = re.compile(u'(\d+)月(\d+)日(.*)')
        datepat3 = re.compile(u'(.*)(\u00A0|\u200B)(.*)')
        m1 = datepat1.match(self.PubTime)
        m2 = datepat2.match(self.PubTime)
        if m1:
            self.PubTime="2018-1-1 "+m1.group(1)+":00 "
        if m2:
            self.PubTime="2017-"+m2.group(1)+"-"+m2.group(2)+m2.group(3)+":00 "
        m3 = datepat3.match(self.PubTime)
        if m3:
            self.PubTime=m3.group(1)+m3.group(2)      
        d = {
            '_id': self._id,
            'ID': self.ID,
            'Content': self.Content,
            'PubTime': self.PubTime,
            'Like': self.Like,
            'Comment': self.Comment,
            'Transfer': self.Transfer,
        }
        if self.Co_oridinates is not None:
            d['Co_oridinates'] = self.Co_oridinates
        if self.Tools is not None:
            d['Tools'] = self.Tools
        return d


class Follows(DynamicDocument):
    """关注的人信息"""
    _id = StringField()
    meta = {'collection': 'Follows'}


app = Flask(__name__)  


@app.route('/')  
def index():  
    return redirect(url_for('username'), code=302)    # URL跳转，默认代码是302，可以省略  


@app.route('/username', methods=['GET', 'POST'])  
def username():
    if request.method == 'GET':  
        return "<h1>Bad Request</h1>", 400
    elif request.method == 'POST':  
        if request.form['username']:
            connect('Sina', host='localhost', port=27017)
            name = request.form['username']
            if request.form['action']=='getinfo':
                info = UserInfo.objects(_id=name)
                data = dict()
                for i in info:
                    data = i.to_json()
                return json.dumps(data), 200
            elif request.form['action']=='getbloc':
                bloc = list()
                follows = Follows.objects()[:2]# 这个地方如果取的太多，会造成延迟太大的问题
                for follow in follows:
                    tweets = Tweets.objects(ID=follow._id)[:15]
                    for tweet in tweets:
		    	bloc.append(json.dumps(tweet.to_json()))
                print(type(bloc))
                return ','.join(bloc), 200
        else:  
            return "<h1>No Request</h1>",401 


if __name__ == '__main__':  
    app.run(host='0.0.0.0', port=5000)  
