
#pragma once

struct CAppConfig
{
	string	userId;
	string	password;
	string	heartBeat;
	string	authorCode;
	string	macAddress;
	string	computerName;
	string	softwareName;
	string	serverAddress;
	string	softwareVersion;
	string  priceBrokerId;

	CAppConfig()
	{
		
		heartBeat = "180";
		softwareName = "api";
		userId = "025696";
		password = "6Ea6mK";
		softwareVersion = "2";
		macAddress = "song_123";
		computerName = "WJQ-PC";
		//serverAddress = "101.95.12.110:9796";
        serverAddress = "222.73.119.230:7007";
		authorCode = "porl99bbo/jrfib5xxgagza5giggzr/u";
		priceBrokerId = "xxx";

	}
};

