# -*- coding:utf-8

from flask import Flask, request, redirect, url_for
from mongoengine import *
import json
import re


Info = {'addr': '127.0.0.1',
        'port': 27017,
        'database': 'Sina'}

from aip import AipNlp

""" 你的 APPID AK SK """
APP_ID = '10799517'
API_KEY = 'xzMsCEd2ZkGwEEa8aiyRWGO8'
SECRET_KEY = 'QtCUG2sBHSvp4LegMO7XzsEwBOhhXGBe '
client = AipNlp(APP_ID, API_KEY, SECRET_KEY)


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

        d["cut"]='1'
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
        d["cut"]='0'
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


    def tweet_sim_cal(self,tweet,tweets):
        ''''''
        #构造随机数
        text1 = tweet.Content.encode('GBK','ignore')
        print('文本一:'+text1.decode('GBK'))
        num_of_tweets = tweets.count()
        if num_of_tweets < 5:
            cycles = num_of_tweets
        else:
            cycles = 5
        for i in range(cycles):
            ran = floor(random.random()*100) % num_of_tweets
            text2 = tweets[ran].Content.encode('GBK','ignore')
            print('文本二:'+text2.decode('GBK'))
            res = client.simnet(text1.decode('GBK'),text2.decode('GBK'))
            print(res)
            tweet.SimScore += res['score']
            print('和 "{}" 的相似度为{}'.format(text2.decode('GBK'),res['score']))
        tweet.SimScore /= cycles
        return tweet.SimScore
    def score_of_behave(self,tweet,tweets):
        '''计算用户微博行为得分'''
        score_b = 0
        zpz = tweet.Comment*1.5 + tweet.Transfer*2 + tweet.Like +2
        score_b += log(zpz)
        score_b*=(1-self.tweet_sim_cal(tweet,tweets))

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

    def get_info(self):
        Info = UserInfo.objects(_id__startswith=self.ID)
        return Info


    def to_json(self):
        datepat1 = re.compile(u'今天 (.*)')
        datepat2 = re.compile(u'(\d+)月(\d+)日(.*)')
        datepat3 = re.compile(u'(.*)(\u00A0|\u200B)(.*)')
        m1 = datepat1.match(self.PubTime)
        m2 = datepat2.match(self.PubTime)
        Info=self.get_info()
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
            'cut':'0',
            'NickName': Info[0].NickName,
        }
        if self.Co_oridinates is not None:
            d['Co_oridinates'] = self.Co_oridinates
        if self.Tools is not None:
            d['Tools'] = self.Tools
        return d
    def to_json_cut(self):
        datepat1 = re.compile(u'今天 (.*)')
        datepat2 = re.compile(u'(\d+)月(\d+)日(.*)')
        datepat3 = re.compile(u'(.*)(\u00A0|\u200B)(.*)')
        Info=self.get_info()
        m1 = datepat1.match(self.PubTime)
        m2 = datepat2.match(self.PubTime)
        if m1:
            self.PubTime="2018"
        if m2:
            self.PubTime="2017"
        m3 = datepat3.match(self.PubTime)
        if m3:
            self.PubTime=m3.group(1)[:4]
        d = {
            '_id': self._id,
            'ID': self.ID,
            'Content': self.Content,
            'PubTime': self.PubTime,
            'Like': self.Like,
            'Comment': self.Comment,
            'Transfer': self.Transfer,
            'NickName': Info[0].NickName,
            'cut':'1',
        }
        return d


class Follows(DynamicDocument):
    """关注的人信息"""
    _id = StringField()
    meta = {'collection': 'Follows'}


app = Flask(__name__)  

lo=list()

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
            name = request.form['username']#['username']
	    print("username:"+name+"\n")
	    print(request.form['action'])
            if request.form['action']=='login':
                pwd = request.form['password']
                imei = request.form['tools']
                count = int(request.form['count'])
                info = UserInfo.objects(_id=name)
                data = dict()
                json0 = {"status":"0"}
                json1 = {"status":"2","count":"0"}
                json2 = {"status":"1","count":6-count}
                json3 = {"status":"2","count":"0"}
                json4 = {"status":"1","count":4-count}
                for i in info:
                    data = i.to_json()
                if not ("IMEI" in data):
                    data["IMEI"]="0"
                if pwd == '12345':
                    info.IMEI = imei
		    info.update(IMEI=imei)
                    return json.dumps(json0),200
                elif imei == data["IMEI"]:
                    if count >= 6:
                        return json.dumps(json1),200
                    else:
                        return json.dumps(json2),200
                else:
                    info.IMEI = imei
                    info.update(IMEI=imei)
                    if count >= 4:
		    	print(json3)
                        return json.dumps(json3),200
                    else:
		    	print(json4)
                        return json.dumps(json4),200

            elif request.form['action']=='getbloc':
	    	#name=request.form['getid']
                bloc = {}
                info=UserInfo.objects(_id=request.form['getid'])
		print(request.form['getid'])
                follows = Follows.objects(_id=request.form['getid'])# 这个地方如果取的太多，会造成延迟太大的问题
                #for follow in follows:
		    #print(follow['1'])
		s=request.form['getid']
		print(s)
		tweets = Tweets.objects(ID=s)[:15]#follow['1'])[:15]
		for i,tweet in enumerate(tweets):
		    print(i)
		    print(tweet.to_json())
                    if float(info[0].Trust_Value)>5:
		    	bloc[str(i)]=json.dumps(tweet.to_json());
		    else:
			bloc[str(i)]=json.dumps(tweet.to_json_cut());
		#ret=','.join(bloc)
		#print(type(ret))
		#print(ret)
		print(str(bloc).decode("unicode-escape"))
                return str(bloc).decode("unicode-escape"), 200#ret.decode("unicode-escape"), 200

    	    elif request.form['action']=='getinfo':
                getid = request.form['getid']
    	    	info=UserInfo.objects(_id=request.form['username'])
        	uid = request.form['getid']
        	uinfo=UserInfo.objects(_id=getid)
		for i in info:
		    jsonValue={}
        	    if float(i.Trust_Value)>5:
		        for u in uinfo:
			    #global jsonValue
        		    jsonValue=u.to_json_ncut()
                    else:
			for u in uinfo:
			    #global jsonValue
                	    jsonValue=uinfo.to_json_cut()
		    print(jsonValue)
                    return json.dumps(jsonValue).decode("unicode-escape"),200
        else:  
            return "<h1>No Request</h1>",401 


if __name__ == '__main__': 
	app.run(host='0.0.0.0', port=5000)  
