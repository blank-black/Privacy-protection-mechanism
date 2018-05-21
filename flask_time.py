# -*- coding:utf-8

from flask import Flask, request, redirect, url_for
from mongoengine import *
from math import *
from sklearn.cluster import KMeans
import re
import math
import sys
import time

DEBUG = 1

max_bias = 0


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


    '''
    获取该用户的所有tweets
    '''
    def get_tweets(self):
        tweets = Tweets.objects(_id__startswith=self._id)
        return tweets

    def if_tweets_less_than_3(self, tweets):
        tweets_num = 0
        for tweet in tweets:
            tweets_num += 1
        if tweets_num < 3:
            return 1
        else:
            return 0

    def tweets_timer_cluster(self, tweets):
        self.tweets_timer = []

        tweets_num=0

        for tweet in tweets:
            # timeObj = re.match('.*(\d{2,}):(\d{2,})',tweet.PubTime)
            # hour = int(timeObj.group(1))
            # minute = int(timeObj.group(2))
            secs = tweet.sec()
            self.tweets_timer.append([secs, 0])
            tweets_num+=1


        # print(self._id,tweets_num)            
        kmeans = KMeans(n_clusters=3).fit(self.tweets_timer)

        if DEBUG:
            for i in range(3):
                h=int(kmeans.cluster_centers_[i][0]//3600)
                m=int((kmeans.cluster_centers_[i][0]-h*3600)//60)
                s=int(kmeans.cluster_centers_[i][0]-h*3600-m*60)
                print('第'+str(i+1)+'个聚类中心为:'+"{:0>2d}".format(h)+':'+"{:0>2d}".format(m)+':'+"{:0>2d}".format(s))
# cluster_centers_ : array, [n_clusters, n_features]
# Coordinates of cluster centers
# labels_ : :
# Labels of each point
# inertia_ : float
# Sum of squared distances of samples to their closest cluster center.
        return kmeans

    def tweets_timer_bias(self,tweets):
        kmeas=self.tweets_timer_cluster(tweets)

        maxbias=0
        bias_arr=[]
        for tweet in tweets:
            secs=tweet.sec()



            bias = 1/((1/abs(kmeas.cluster_centers_[0][0]-secs+0.01))+(1/abs(kmeas.cluster_centers_[1][0]-secs+0.01))+(1/abs(kmeas.cluster_centers_[2][0]-secs+0.01)))

            if bias > maxbias:
                maxbias=bias
            bias_arr.append(bias)

        # for i in range(len(bias_arr)):
        #     bias_arr[i]/=maxbias

        # print(maxbias)

        return bias_arr

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
        if not self.Province is None:
            d["Province"] = self.Province
            d["Province"].encode("utf-8")
        if not self.Num_Tweets is None:
            d["Num_Tweets"] = self.Num_Tweets
        if not self.Num_Follows is None:
            d["Num_Follows"] = self.Num_Follows
        if not self.Num_Fans is None:
            d["Num_Fans"] = self.Num_Fans
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


    def get_follows(self):
        follows = Follows.objects(_id__startswith=self._id)
        return follows

    def get_users(self):
        UserInfo = UserInfo.objects(_id__startswith=self._id)
        return UserInfo


    def if_abnormal_login(self):
        if self.if_tweets_less_than_3(self.get_tweets()):
            return 0

        kmeans=self.tweets_timer_cluster(self.get_tweets())
        now_time=time.localtime(time.time()).tm_hour*3600+time.localtime(time.time()).tm_min*60+time.localtime(time.time()).tm_sec
        bias = 1/((1/abs(kmeans.cluster_centers_[0][0]-now_time+0.01))+(1/abs(kmeans.cluster_centers_[1][0]-now_time+0.01))+(1/abs(kmeans.cluster_centers_[2][0]-now_time+0.01)))
        return if_abnormal_time(bias)

    # def check_before_login(self):
    #     follows=self.get_follows()
    #     user=self.get_users()
    #     follow_user=[]
    #     Followsnum=0
    #     for i in range(len(follows.meta)):
    #         for j in range(len(user._id)):
    #             if follows[i].meta == user[j]._id:
    #                 Followsnum += 1
    #                 follow_user.append(user[j].NickName)
    #     if Followsnum >= 2:#大于两个关注的人
    #         random.randint(0, Followsnum-1)



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
            # print(m3.group(1)[-8:-6]+m3.group(1)[-5:-3]+m3.group(1)[-2:])
        elif m3:
            try:
                a = int(m3.group(1)[-8:-6])*3600+int(m3.group(1)[-5:-3])*60+int(m3.group(1)[-2:])
            except ValueError:
                a=65280
                # print(m3.group(1))
        else:
            try:
                a = int(self.PubTime[-8:-6])*3600+int(self.PubTime[-5:-3])*60+int(self.PubTime[-2:])
            except ValueError:
                a=65280
                # print(a)
        return a



class Follows(DynamicDocument):
    """关注的人信息"""
    _id = StringField()
    meta = {'collection': 'Follows'}



def fisher_cluster(data_list):
    sum_cost = sys.maxsize
    label = 0
    for i in range(1, len(data_list)):
        d1 = 0
        d2 = 0
        avg1 = get_average(data_list[0:i])
        avg2 = get_average(data_list[i:len(data_list)])
        for j in range(i):
            d1 += (data_list[j] - avg1) * (data_list[j] - avg1)# * (data_list[j] - avg1)
        for j in range(i, len(data_list)):
            d2 += (data_list[j] - avg2) * (data_list[j] - avg2)# * (data_list[j] - avg2)
        if d1 + d2 < sum_cost:
            sum_cost = d1 + d2
            label = i
    return label, sum_cost


def get_average(inlist):
    sum_inlist = 0
    for item in inlist:
        sum_inlist += item
    return sum_inlist / len(inlist)


def get_Threshold_label():
    global max_bias
    file_obj_max = open('./time_clo_max.txt','r').read()
    file_obj = open('./time_clo.txt','r').read()
    re_pattern = '\d+'
    match = re.findall(re_pattern,file_obj)
    matchmax = re.findall(re_pattern,file_obj_max)
    max_bias = int(match[0])
    data = []
    for d in match:
        data.append(int(d))
    label = fisher_cluster(data)[0]
    return label

def if_abnormal_time(bias):
    Threshold = get_Threshold_label()*max_bias/100
    if DEBUG:
        print("阈值为:"+str(Threshold))
        print("登录时误差为:"+str(bias))

    if bias > Threshold:
        return 1
    return 0


def write_bias():
    bias=[]
    global max_bias
    for user in UserInfo.objects:
        if user.if_tweets_less_than_3(user.get_tweets()) == 0:
            temp_bias=user.tweets_timer_bias(user.get_tweets())
            for i in range(len(temp_bias)):
                bias.append(temp_bias[i])

    bias_clo=[]
    for i in range(101):
        bias_clo.append(0)

    for i in range(len(bias)):
        if bias[i] > max_bias:
            max_bias=bias[i]

    for i in range(len(bias)):
        bias_clo[int(bias[i]/max_bias/0.01)]+=1

    fw=open('time_clo.txt','w')
    print >> fw,bias_clo

    fwmax=open('time_clo_max.txt','w')
    print >> fwmax,max_bias

app = Flask(__name__)  

lo=list()

@app.route('/')  
def index():  
    return redirect(url_for('username'), code=302)    # URL跳转，默认代码是302，可以省略


# @app.route('/username', methods=['GET', 'POST'])
if __name__ == '__main__': 
    connect('Sina', host='localhost', port=27017)
    # write_bias()
    name='5053317120'
    user=UserInfo.objects(_id=name)
    print('当前系统时间:'+time.asctime( time.localtime(time.time()) ))
    for u in user:
        if u.if_abnormal_login():
            print('登录时误差大于阈值,判断为非正常时间登录')
        else:
            print('登录时误差小于等于阈值,判断为正常时间登录')

