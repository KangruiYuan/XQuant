
#pragma once

#include "DAMarketApi.h"
using namespace Directaccess;

class CMyMarket : public IMarketEvent
{
private:
	typedef map<string, CMarketRspUserLoginField> CMapAccount;

	// 成员变量
private:
	CLockBool		m_bIsLogin;				// 是否登陆
	CAppConfig		m_appConfig;			// 配置文件
	CMarketApi*		m_pMarketApi;			// 行情接口

	//构造析构
public:
	CMyMarket() {
		m_bIsLogin = false;
		m_pMarketApi = 0;
	}
	virtual ~CMyMarket() {}

	// 创建销毁
public:
	bool Create()
	{
		if (m_pMarketApi) {
			Destroy();
		}
		m_pMarketApi = CMarketApi::CreateMarketApi(true, "TestMarket.log");
		if (m_pMarketApi) {
			COUTTIME << "---------------- API 信息 ----------------" << endl;
			COUTTIME << "API Version: " << m_pMarketApi->GetVersion() << endl;
			COUTTIME << "Server Addr: " << m_appConfig.serverAddress.c_str() << endl;
			COUTTIME << "User ID: " << m_appConfig.userId.c_str() << endl;
			COUTTIME << endl;

			char addr[MAX_PATH];
			snprintf(addr, MAX_PATH, "tcp://%s", m_appConfig.serverAddress.c_str());

			LONG beat = atol(m_appConfig.heartBeat.c_str());

			m_pMarketApi->RegisterSpi(this);
			m_pMarketApi->RegisterNameServer(addr);
			m_pMarketApi->SetHeartBeatTimeout(beat);
			m_pMarketApi->Init();

			COUTTIME << "开始连接行情服务器...." << endl;
			COUTTIME << endl;
			return true;
		}
		return false;
	}
	void Destroy()
	{
		if (m_pMarketApi) {
			if (m_bIsLogin) {
				m_bIsLogin = false;
				CrossSleep(250);
			}

			m_pMarketApi->Release();
			m_pMarketApi = NULL;
			COUTTIME << "销毁 CMyMarket" << endl;
		}
	}
	bool IsLogin()
	{
		return m_bIsLogin;
	}
	bool IsCreate()
	{
		return m_pMarketApi != NULL;
	}

	//一般函数
public:
	string GetDateTime()
	{
#ifdef _WIN32
		SYSTEMTIME st = {};
		GetLocalTime(&st);

		char szBuffer[MAX_PATH];
		snprintf(szBuffer, sizeof(szBuffer), "【%04d-%02d-%02d %02d:%02d:%02d.%03d】",
			st.wYear, st.wMonth, st.wDay, st.wHour, st.wMinute, st.wSecond, st.wMilliseconds);

		return szBuffer;
#else
		char szBuffer[MAX_PATH];

		time_t now;
		time(&now);
		tm *tm_now = localtime(&now);

		timeval tv;
		gettimeofday(&tv, NULL);

		snprintf(szBuffer, sizeof(szBuffer), "【%04d-%02d-%02d %02d:%02d:%02d.%03d】",
			tm_now->tm_year + 1900, tm_now->tm_mon + 1, tm_now->tm_mday,
			tm_now->tm_hour, tm_now->tm_min, tm_now->tm_sec, tv.tv_usec / 1000);

		return szBuffer;
#endif
	}
	void SubscStockBroker()
	{
		CMarketReqBrokerDataField qry = {};

		const char cont[] = "00700.HK";
		safe_cpy(qry.ContCode, cont);
		if (m_pMarketApi->ReqBrokerData(&qry, 0))
			COUTTIME << "订阅股票经济商成功: " << cont << endl;
		else
			COUTTIME << "订阅股票经济商失败: " << cont << endl;
	}
	void UnsubscAllMarket()
	{
		CMarketReqMarketDataField qry = {};

		qry.MarketType = DAF_TYPE_Unknown;
		qry.SubscMode = DAF_SUB_UnsubcribeAll;
		if (m_pMarketApi->ReqMarketData(&qry, 0))
			COUTTIME << "退订全部行情成功" << endl;
		else
			COUTTIME << "退订全部行情失败" << endl;
	}
	void SendLoginRequest()
	{
		CMarketReqUserLoginField req = {};

		COUTTIME << "用户名:" << m_appConfig.userId << endl;
		COUTTIME << "密码:" << "******" << endl;

		safe_cpy(req.UserId, m_appConfig.userId.c_str());
		safe_cpy(req.UserPwd, m_appConfig.password.c_str());
		safe_cpy(req.AuthorCode, m_appConfig.authorCode.c_str());
		safe_cpy(req.MacAddress, m_appConfig.macAddress.c_str());
		safe_cpy(req.ComputerName, m_appConfig.computerName.c_str());
		safe_cpy(req.SoftwareName, m_appConfig.softwareName.c_str());
		safe_cpy(req.SoftwareVersion, m_appConfig.softwareVersion.c_str());
		safe_cpy(req.BrokerIDForMarketPrice, m_appConfig.priceBrokerId.c_str());

		if (m_pMarketApi->ReqUserLogin(&req, 0)) {
			COUTTIME << "开始登录...." << endl;
		}
		else {
			COUTTIME << req.ErrorDescription << endl;
		}
	}
	void SubscStockMarket()
	{
		CMarketReqMarketDataField qry = {};

		qry.MarketType = DAF_TYPE_Stock;
		qry.SubscMode = DAF_SUB_Append;

		static int times = 0;
		
		if (times > 90)
			times = 0;
		char cont[30] = "HKEX,01000.HK";

		int num = 10;

		const char cont0[] = "HKEX,00992.HK";
		const char cont1[] = "NASD,GOOG.US";
		const char cont2[] = "NASD,FB.US";
		const char cont3[] = "NASD,NIO.US";
		const char cont4[] = "NASD,AMZN.US";
		const char cont5[] = "NASD,MSFT.US";
		const char cont6[] = "NASD,IBM.US";
		const char cont7[] = "NASD,AABA.US";
		const char cont8[] = "HKEX,00176.HK";
		const char cont9[] = "HKEX,00070.HK";

		//NASD, AAPL.US; NASD, GBTC.US; NASD, TSLA.US; NASD, IBM.US; NASD, MSFT.US; NASD, AMZN.US; NASD, BILI.US; NASD, NIO.US; NASD, FB.US; NASD, BABA.US; NASD, GOOG.US

		if (times >0)
			qry.MarketCount = 10;
		else
			qry.MarketCount = 20;
		
		for (int i = 0; i < 10; i++)
		{			
			std::string str = std::to_string((num*times + i + 1000));
			
			memcpy(cont+6, str.c_str(), 4);
			safe_cpy(qry.MarketTrcode[i], cont);
		}

		safe_cpy(qry.MarketTrcode[10], cont0);
		safe_cpy(qry.MarketTrcode[11], cont1);
		safe_cpy(qry.MarketTrcode[12], cont2);
		safe_cpy(qry.MarketTrcode[13], cont3);
		safe_cpy(qry.MarketTrcode[14], cont4);
		safe_cpy(qry.MarketTrcode[15], cont5);
		safe_cpy(qry.MarketTrcode[16], cont6);
		safe_cpy(qry.MarketTrcode[17], cont7);
		safe_cpy(qry.MarketTrcode[18], cont8);
		safe_cpy(qry.MarketTrcode[19], cont9);

		times++;

		if (m_pMarketApi->ReqMarketData(&qry, 0)) {
			COUTTIME << "订阅股票行情成功" << endl;
		}
		else {
			COUTTIME << "订阅股票行情失败" << endl;
			COUTTIME << "错误：" <<qry.ErrorDescription<< endl;
		}
	}

	void SubscFutureMarket()
	{
		CMarketReqMarketDataField qry = {};

		qry.SubscMode = DAF_SUB_Replace;
		qry.MarketType = DAF_TYPE_Future;

		qry.MarketCount = 3;
		//safe_cpy(qry.MarketTrcode[0], "SGXQ,CN2302");
		//safe_cpy(qry.MarketTrcode[1], "SGXQ,CN2303");
		//safe_cpy(qry.MarketTrcode[2], "CBOE,VX2303");

		//safe_cpy(qry.MarketTrcode[0], "LME,PB3M");
		//safe_cpy(qry.MarketTrcode[1], "LME,L-ZS3M");
		//safe_cpy(qry.MarketTrcode[2], "SGXQ,CN2303");
        safe_cpy(qry.MarketTrcode[0], "DL-DCE,DL-i2401");
        safe_cpy(qry.MarketTrcode[1], "DCE,DS-i2401");
        //safe_cpy(qry.MarketTrcode[2], "DL-DCE,DL-i2401");
        //safe_cpy(qry.MarketTrcode[1], "LME,PB3M");
        safe_cpy(qry.MarketTrcode[2], "LME,L-ZS3M");

		if (m_pMarketApi->ReqMarketData(&qry, 0))
			COUTTIME << "订阅期货行情成功!" << endl;
		else
			COUTTIME << "订阅期货行情失败, err_message:" << qry.ErrorDescription << endl;
	}
	void UnsubscStockMarket()
	{
		CMarketReqMarketDataField qry = {};

		qry.MarketType = DAF_TYPE_Stock;
		qry.SubscMode = DAF_SUB_Unsubcribe;

		const char cont0[] = "HKEX,00001.HK";
		const char cont1[] = "HKEX,00700.HK";
		const char cont2[] = "HKEX,03333.HK";

		qry.MarketCount = 3;
		safe_cpy(qry.MarketTrcode[0], cont0);
		safe_cpy(qry.MarketTrcode[1], cont1);
		safe_cpy(qry.MarketTrcode[2], cont2);

		if (m_pMarketApi->ReqMarketData(&qry, 0))
			COUTTIME << "退订股票行情成功" << endl;
		else
			COUTTIME << "退订股票行情失败" << endl;
	}
	void UnsubscFutureMarket()
	{
		CMarketReqMarketDataField qry = {};

		qry.MarketType = DAF_TYPE_Future;
		qry.SubscMode = DAF_SUB_Unsubcribe;
		//qry.SubscMode = DAF_SUB_UnsubcribeAll;

		//qry.MarketCount = 6;
		//safe_cpy(qry.MarketTrcode[0], "HKEX,CUS1901");
		//safe_cpy(qry.MarketTrcode[1], "HKEX,CUS1902");
		//safe_cpy(qry.MarketTrcode[2], "HKEX,CUS1903");
		//safe_cpy(qry.MarketTrcode[3], "CME,CL1901");
		//safe_cpy(qry.MarketTrcode[4], "CME,CL1902");
		//safe_cpy(qry.MarketTrcode[5], "CME,CL1903");

		qry.MarketCount = 1;
		//safe_cpy(qry.MarketTrcode[0], "LME,CA*");
		//safe_cpy(qry.MarketTrcode[1], "LME,NI*");
		safe_cpy(qry.MarketTrcode[0], "TOCOM,RSS32212");
		//safe_cpy(qry.MarketTrcode[1], "HKEX,HSI2003");

		if (m_pMarketApi->ReqMarketData(&qry, 0))
			COUTTIME << "退订期货行情成功" << endl;
		else
			COUTTIME << "退订期货行情失败" << endl;
	}


	//虚函数
public:
	virtual void OnFrontConnected()
	{
		COUTTIME << "连接服务器成功" << endl;
		m_bIsLogin = false;
		SendLoginRequest();

	}
	virtual void OnFrontDisconnected(int iReason)
	{
		m_bIsLogin = false;
		COUTTIME << "连接断开, 原因 = " << iReason << "." << endl;
	}
	virtual void OnHeartBeatWarning(int iTimeLapse)
	{
		COUTTIME << "心跳:" << iTimeLapse << endl;
	}
	virtual void OnRspUserLogin(CMarketRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		if (pRspInfo->ErrorID) {
			COUTTIME << "登录行情接口失败！" << endl;
			COUTTIME << "ErrorCode = " << pRspInfo->ErrorID << endl;
			COUTTIME << "ErrorMsg = " << pRspInfo->ErrorMsg << endl;
			m_bIsLogin = false;
		}
		else {
			COUTTIME << "登录行情接口成功，可以订阅行情了...." << endl;
			m_bIsLogin = true;
		}
	}
	virtual void OnRspUserLogout(CMarketRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		if (pRspInfo->ErrorID) {
			COUTTIME << "登出行情接口失败." << endl;
			COUTTIME << "ErrorID = " << pRspInfo->ErrorID << endl;
			COUTTIME << "ErrorMsg = " << pRspInfo->ErrorMsg << endl;
			m_bIsLogin = false;
		}
		else {
			COUTTIME << "登出行情接口成功." << endl;
			m_bIsLogin = true;
		}
		
	}
	virtual void OnRspTradeDate(CMarketRspTradeDateField *pRspTradeDate, CMarketRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		if (pRspInfo->ErrorID) {
			COUTTIME << "ErrorID = " << pRspInfo->ErrorID << endl;
			COUTTIME << "ErrorMsg = " << pRspInfo->ErrorMsg << endl;
		}
		else {
			printf("%s TradeDate=%-10s TradeProduct=%-10s\r\n",
				GetDateTime().c_str(),
				pRspTradeDate->TradeDate,
				pRspTradeDate->TradeProduct);
		}
	}
	virtual void OnRspBrokerData(CMarketRspBrokerDataField *pRspBrokerData, CMarketRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		if (pRspInfo->ErrorID) {
			COUTTIME << "ErrorID = " << pRspInfo->ErrorID << endl;
			COUTTIME << "ErrorMsg = " << pRspInfo->ErrorMsg << endl;
		}
		else {
			COUTTIME << "BrokerData= " << pRspBrokerData->BrokerData << endl;
		}
	}
	virtual void OnRspMarketData(CMarketRspMarketDataField *pRspMarketData, CMarketRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		if (pRspInfo->ErrorID) {
			COUTTIME << "ErrorID = " << pRspInfo->ErrorID << endl;
			COUTTIME << "ErrorMsg = " << pRspInfo->ErrorMsg << endl;
		}
		else {
			printf("%s TrCode=%-10s CurrPrice=%-10s CurrNumber=%-7s FilledNum=%-10s QuoteType=%s\r\n",
				GetDateTime().c_str(), pRspMarketData->TreatyCode, pRspMarketData->CurrPrice,
				pRspMarketData->CurrNumber, pRspMarketData->FilledNum, pRspMarketData->QuoteType);
		}
	}
};

