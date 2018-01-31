#include <iostream>
#include <stdio.h>
#include <string>
#include <string.h>
#include <fstream>
#include <stdlib.h>
#include "data_pretreatment.h"
using namespace std;
#define MAXCHAR 10000
#define MAXUSER 5000
#define DEBUG 1
#define DEBUGUSER 2

regex id("\"_id\":\"(\\d+)\"");
regex url("\"URL\":\"([^\"]+)\"");
regex city("\"City\":\"([^\"]+)\"");
regex birth("\"Birthday\":\\{\"\\$date\":\"([^\"]+)\"\\}");
regex gender("\"Gender\":\"([^\"]+)\"");
regex province("\"Province\":\"([^\"]+)\"");
regex nickname("\"NickName\":\"([^\"]+)\"");
regex marriage("\"Marriage\":\"([^\"]+)\"");
regex num_fans("\"Num_Fans\":(\\d+)");
regex num_tweets("\"Num_Tweets\":(\\d+)");
regex num_follows("\"Num_Follows\":(\\d+)");
regex signature("\"Signature\":\"([^\"]+)\"");
regex sex_orientation("\"Sex_Orientation\":\"(.+)\"");

userinfo user[MAXUSER];

int read_data_information()
{
	ifstream data_infor("/data/sc_project/MongoDB_Data_Information");
	char buffer[MAXCHAR];
	for (int i = 0; !data_infor.eof(); i++)
	{
		int substrlen;
		cmatch id_match, nickname_match, url_match, signature_match, num_follows_match, num_fans_match, num_tweets_match,
				city_match, province_match, birth_match, gender_match, marriage_match, sex_orientation_match;
		data_infor.getline(buffer, MAXCHAR - 1);
		regex_search(buffer, id_match, id);
		user[i].id = id_match.str(1);

		regex_search(buffer, nickname_match, nickname);
		if (user[i].if_nickname = regex_search(buffer, nickname))
			user[i].nickname = nickname_match.str(1);

		regex_search(buffer, url_match, url);
		user[i].url = url_match.str(1);

		regex_search(buffer, signature_match, signature);
		if (user[i].if_signature = regex_search(buffer, signature))
			user[i].signature = signature_match.str(1);

		regex_search(buffer, num_follows_match, num_follows);
		user[i].num_follows = atoi(num_follows_match.str(1).c_str());

		regex_search(buffer, num_fans_match, num_fans);
		user[i].num_fans = atoi(num_fans_match.str(1).c_str());

		regex_search(buffer, num_tweets_match, num_tweets);
		user[i].num_tweets = atoi(num_tweets_match.str(1).c_str());

		regex_search(buffer, city_match, city);
		user[i].city = regex_search(buffer, city);

		regex_search(buffer, province_match, province);
		user[i].province = regex_search(buffer, province);

		regex_search(buffer, birth_match, birth);
		user[i].birth = regex_search(buffer, birth);

		regex_search(buffer, gender_match, gender);
		user[i].gender = regex_search(buffer, gender);

		regex_search(buffer, marriage_match, marriage);
		user[i].marriage = regex_search(buffer, marriage);

		regex_search(buffer, sex_orientation_match, sex_orientation);
		user[i].sex_orientation = regex_search(buffer, sex_orientation);
	}
	return 0;
}

int read_data_fans()
{
	return 0;
}

int read_data_follows()
{
	return 0;
}

int count_fans_follows()
{
	return 0;
}

int main()
{
	read_data_information();

	if (DEBUG)
	{
		cout << "id:" << user[DEBUGUSER].id << endl;
		cout << "url:" << user[DEBUGUSER].url << endl;
		cout << "ifcity:" << user[DEBUGUSER].city << endl;
		cout << "ifbirth:" << user[DEBUGUSER].birth << endl;
		cout << "ifgender:" << user[DEBUGUSER].gender << endl;
		cout << "ifprovince:" << user[DEBUGUSER].province << endl;
		cout << "nickname:" << user[DEBUGUSER].nickname << endl;
		cout << "ifmarriage:" << user[DEBUGUSER].marriage << endl;
		cout << "num_fans:" << user[DEBUGUSER].num_fans << endl;
		cout << "num_tweets:" << user[DEBUGUSER].num_tweets << endl;
		cout << "num_follows:" << user[DEBUGUSER].num_follows << endl;
		cout << "ifsignature:" << user[DEBUGUSER].if_signature << endl;
		if (user[DEBUGUSER].if_signature)
			cout << "signature:" << user[DEBUGUSER].signature << endl;
		cout << "sex_orientation:" << user[DEBUGUSER].sex_orientation << endl;
	}
	system("pause");
	return 0;
}