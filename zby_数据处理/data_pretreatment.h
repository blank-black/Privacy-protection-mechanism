#pragma once

#include<string>
#include<regex>

#define MAXFANS 200
#define MAXFOLLOWS 200

using namespace std;

class userinfo {
public:
	string id, nickname, url, signature;
	int num_follows, num_fans, num_tweets;
	bool city, province, birth, gender, marriage, sex_orientation, if_signature, if_nickname;

	int num_follows_match, num_fans_match, num_tweets_match;
	string follows_id[MAXFOLLOWS], fans_id[MAXFANS];


	friend istream &operator>>(istream &, userinfo &);
};
istream & operator >>(istream & in, userinfo &);