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
#define DEBUGUSER 0

userinfo user[MAXUSER];

int read_data_information()
{
	ifstream data_infor("/data/sc_project/MongoDB_Data_Information");
	char buffer[MAXCHAR];
	for(int i=0;i<10;i++)
	{
		int substrlen;
		cmatch id_match,nickname_match,url_match,signature_match,num_follows_match,num_fans_match,num_tweets_match,
				city_match,province_match,birth_match,gender_match,marriage_match,sex_orientation_match;
		data_infor.getline(buffer,MAXCHAR-1);
		regex_search(buffer,id_match,id);
		user[i].id=id_match.str().substr(7,10);

		regex_search(buffer,nickname_match,nickname);
		substrlen = nickname_match.str().substr(12).length();
		user[i].nickname=(nickname_match.str().substr(12)).substr(0,substrlen-1);

		regex_search(buffer,url_match,url);
		substrlen = url_match.str().substr(7).length();
		user[i].url=(url_match.str().substr(7)).substr(0,substrlen-1);

		regex_search(buffer,signature_match,signature);
		if(user[i].if_signature=regex_match(buffer, signature))
		{
			substrlen = signature_match.str().substr(13).length();
			user[i].signature=(signature_match.str().substr(13)).substr((0,substrlen-1));
		}

		regex_search(buffer,num_follows_match,num_follows);
		user[i].num_follows=atoi(num_follows_match.str().substr(14).c_str());

		regex_search(buffer,num_fans_match,num_fans);
		user[i].num_fans=atoi(num_fans_match.str().substr(11).c_str());

		regex_search(buffer,num_tweets_match,num_tweets);
		user[i].num_tweets=atoi(num_tweets_match.str().substr(13).c_str());

		regex_search(buffer,city_match,city);
		user[i].city=regex_search(buffer, city);

		regex_search(buffer,province_match,province);
		user[i].province=regex_search(buffer, province);

		regex_search(buffer,birth_match,birth);
		user[i].birth=regex_search(buffer, birth);

		regex_search(buffer,gender_match,gender);
		user[i].gender=regex_search(buffer, gender);

		regex_search(buffer,marriage_match,marriage);
		user[i].marriage=regex_search(buffer, marriage);

		regex_search(buffer,sex_orientation_match,sex_orientation);
		user[i].sex_orientation=regex_search(buffer, sex_orientation);
	}
}

int read_data_fans()
{

}

int read_data_follows()
{

}

int count_fans_follows()
{

}

int main()
{
	read_data_information();

	if(DEBUG)
	{
		cout << "id:"<<user[DEBUGUSER].id << endl;
		cout << "url:"<<user[DEBUGUSER].url << endl;
		cout << "ifcity:"<<user[DEBUGUSER].city << endl;
		cout << "ifbirth:"<<user[DEBUGUSER].birth << endl;
		cout << "ifgender:"<<user[DEBUGUSER].gender << endl;
		cout << "ifprovince:"<<user[DEBUGUSER].province << endl;
		cout << "nickname:"<<user[DEBUGUSER].nickname << endl;
		cout << "ifmarriage:"<<user[DEBUGUSER].marriage << endl;
		cout << "num_fans:"<<user[DEBUGUSER].num_fans << endl;
		cout << "num_tweets:"<<user[DEBUGUSER].num_tweets << endl;
		cout << "num_follows:"<<user[DEBUGUSER].num_follows << endl;
		cout << "ifsignature:"<<user[DEBUGUSER].if_signature << endl;
		if (user[DEBUGUSER].if_signature)
			cout << "signature:"<<user[DEBUGUSER].signature << endl;
		cout << "sex_orientation:"<<user[DEBUGUSER].sex_orientation << endl;
	}
	return 0;
}