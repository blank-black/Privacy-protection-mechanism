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
    IMEI = StringField() # 设备标识号
    Trust_Value= StringField()
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
        if not self.IMEI is None:
            d["IMEI"] = self.IMEI
	if not self.Trust_Value is None:
	    d["Trust_Value"] = self.Trust_Value
        return d

    def to_json_cut(self):
        d = {
            "_id": str(self._id),
            "NickName": self.NickName
        }
        # if not self.Gender is None:
        #     d["Gender"] = self.Gender
        if not self.Province is None:
            d["Province"] = self.Province
            d["Province"].encode("utf-8")
        # if not self.City is None:
        #     d["City"] = self.City
        # if not self.Signature is None:
        #     d["Signature"] = self.Signature
        # if not self.Birthday is None:
        #     d["Birthday"] = self.Birthday.isoformat()
        if not self.Num_Tweets is None:
            d["Num_Tweets"] = self.Num_Tweets
        if not self.Num_Follows is None:
            d["Num_Follows"] = self.Num_Follows
        if not self.Num_Fans is None:
            d["Num_Fans"] = self.Num_Fans
        # if not self.Marriage is None:
        #     d["Marriage"] = self.Marriage
        # if not self.URL is None:
        #     d["URL"] = self.URL
        # if not self.IMEI is None:
        #     d["IMEI"] = self.IMEI
        return d

    def to_json_ncut(self):
        d = {
            "_id": str(self._id),
            "NickName": self.NickName
        }
        if not self.Gender is None:
            d["Gender"] = self.Gender
        if not self.Province is None:
            d["Province"] = self.Province
            d["Province"].encode("utf-8")
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

    def Get_Trust_Value(self):
        self.Trust_value=0
        if str(self.NickName).isdigit():
            self.Trust_value -= 0.5
        if self.Gender:
            self.Trust_value += 0.3
        if self.Province:
            self.Trust_value += 0.3
        if self.City:
            self.Trust_value += 0.3
        if self.Signature:
            self.Trust_value += 0.5
        if self.Birthday:
            self.Trust_value += 0.5
        if self.Num_Tweets >= 20:
            self.Trust_value += log(int(self.Num_Tweets)) / 8 * 2.3
        if self.Num_Follows >= 20:
            self.Trust_value += log(int(self.Num_Follows)) / 7 * 2.3
        if self.Num_Fans >= 20:
            self.Trust_value += log(int(self.Num_Fans)) / 10 * 2.3
        if self.Sex_Orientation:
            self.Trust_value += 0.3
        if self.Marriage:
            self.Trust_value += 0.3
        return self.Trust_value

    def get_tweets(self):
        tweets = Tweets.objects(_id__startswith=self._id)
        return tweets

    def score_of_behave(self,tweet,tweets):
        '''计算用户微博行为得分'''
        score_b = 0
        zpz = tweet.Comment + tweet.Transfer + tweet.Like
        score_b += log(zpz)*0.33
        if self.is_common_tool(tweet.Tool):
            score_b += 0.15
        if self.tweet_sim_cal(tweet,tweets)<0.7:
            score_b += 0.2

        return score_b

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
    def sec(self):
        datepat1 = re.compile(u'今天 (.*)')
        datepat2 = re.compile(u'(\d+)月(\d+)日 (.*)(\xa0)')
        datepat3 = re.compile(u'(.*)(\u00A0|\u200B)(.*)')
        m1 = datepat1.match(self.PubTime)
        m2 = datepat2.match(self.PubTime)
        m3 = datepat3.match(self.PubTime)
        if m1:
            self.PubTime=m1.group(1)+":00"
            a = int(m1.group(1)[0:2])*3600+int(m1.group(1)[3:5])*60
            # print(a)
        elif m2:
            self.PubTime=m2.group(3)+":00"
            a = int(m2.group(3)[0:2])*3600+int(m2.group(3)[3:5])*60
            # print(a)
        elif m3:
            self.PubTime=(m3.group(1)+m3.group(2))[-9:-1]
            # print(m3.group(1)[-8:-6]+m3.group(1)[-5:-3]+m3.group(1)[-2:])
            a = int(m3.group(1)[-8:-6])*3600+int(m3.group(1)[-5:-3])*60+int(m3.group(1)[-2:])
            # print(a)
        else:
            a=65280
        
        return a

class Follows(DynamicDocument):
    """关注的人信息"""
    _id = StringField()
    meta = {'collection': 'Follows'}


app = Flask(__name__)  

lo=list()

@app.route('/')  
def index():  
    return redirect(url_for('username'), code=302)    # URL跳转，默认代码是302，可以省略  


# @app.route('/username', methods=['GET', 'POST'])  
# def username():
    

if __name__ == '__main__': 
    connect('Sina', host='localhost', port=27017)
    for tweet in Tweets.objects[:15000]:
        print(tweet.sec())
        # tweet.to_json_cut()
	# app.run(host='0.0.0.0', port=5000)  