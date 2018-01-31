#pragma once

#include<string>
#include<regex>

using namespace std;

regex id("\"_id\":\"\\d+\"");
regex url("\"URL\":\".+\"");
regex city("\"City\":\".+\"");
regex birth("\"Birthday\":\{\"\$date\":\".+\"\}");
regex gender("\"Gender\":\".+\"");
regex province("\"Province\":\".+\"");
regex nickname("\"NickName\":\".+\"");
regex marriage("\"Marriage\":\".+\"");
regex num_fans("\"Num_Fans\":\\d+");
regex num_tweets("\"Num_Tweets\":\\d+");
regex num_follows("\"Num_Follows\":\\d+");
regex signature("\"Signature\":\".+\"");
regex sex_orientation("\"Sex_Orientation\":\".+\"");

class userinfo {
protected:
	string id,nickname,url,signature;
	int num_follows, num_fans,num_tweets;
	bool city, province, birth, gender, marriage, sex_orientation;
public:
	friend istream & operator >>(istream &, userinfo &);
};
istream & operator >>(istream & in, userinfo &);