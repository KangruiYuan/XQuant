
#pragma once

#include "DAFutureApi.h"

using namespace Directaccess;

static int traderQuryCounter;

class CMyFuture : public IFutureEvent
{
private:
	typedef map<string, CFutureRspAccountField> CMapAccount;

	// ��Ա����
private:
	string				m_orderNo;				// ���ص���
	CLockBool			m_bIsLogin;				// �Ƿ��½
	string				m_systemNo;				// ϵͳ����
	LONG				m_iQryPage;				// ��ҳ��־
	CAppConfig			m_appConfig;			// �����ļ�
	CFutureApi*			m_pFutureApi;			// �ڻ��ӿ�
	CMapAccount			m_mapAccounts;			// �����˺�

	// ��������
public:
	CMyFuture() {
		m_iQryPage = 0;
		m_bIsLogin = false;
		m_pFutureApi = 0;
	}
	virtual ~CMyFuture() {}

	// ��������
public:
	bool Create()
	{
		if (m_pFutureApi) {
			Destroy();
		}

		
		m_pFutureApi = CFutureApi::CreateFutureApi(true, "TestFuture.log","");
		if (m_pFutureApi) {
			COUTTIME << "---------------- API ��Ϣ ----------------" << endl;
			COUTTIME << "API Version: " << m_pFutureApi->GetVersion() << endl;
			COUTTIME << "Server Addr: " << m_appConfig.serverAddress.c_str() << endl;
			COUTTIME << "User ID: " << m_appConfig.userId.c_str() << endl;
			COUTTIME << endl;

			char addr[MAX_PATH];
			snprintf(addr, MAX_PATH, "tcp://%s", m_appConfig.serverAddress.c_str());

			LONG beat = atol(m_appConfig.heartBeat.c_str());

			m_pFutureApi->RegisterSpi(this);
			m_pFutureApi->RegisterNameServer(addr);
			m_pFutureApi->SetHeartBeatTimeout(beat);
			m_pFutureApi->Init();

			COUTTIME << "��ʼ�����ڻ����׷�����...." << endl;
			return true;
		}
		else {
			COUTTIME << "�ڻ��ӿڳ�ʼ��ʧ��." << endl;
		}
		return false;
	}
	void Destroy()
	{
		if (m_pFutureApi) {
			if (m_bIsLogin) {
				m_bIsLogin = false;
				CFutureReqUserLogoutField req = {};
				safe_cpy(req.UserId, m_appConfig.userId.c_str());
				m_pFutureApi->ReqUserLogout(&req, 0);
				CrossSleep(250);
			}

			m_pFutureApi->Release();
			m_pFutureApi = NULL;
			COUTTIME << "���� CMyFuture" << endl;
		}
	}
	bool IsLogin()
	{
		return m_bIsLogin;
	}
	bool IsCreate()
	{
		return m_pFutureApi != NULL;
	}

	// һ�㺯��
private:
	string GetDateTime()
	{
		SYSTEMTIME st = {};
		GetLocalTime(&st);

		char szBuffer[MAX_PATH];
		snprintf(szBuffer, sizeof(szBuffer), "��%04d-%02d-%02d %02d:%02d:%02d.%03d��",
			st.wYear, st.wMonth, st.wDay, st.wHour, st.wMinute, st.wSecond, st.wMilliseconds);

		return szBuffer;
	}
	string BuildLocalID(LONG step)
	{
		LONG iLocalID = ReadLocalId("LocalID", 0);
		if (iLocalID < 10000) { iLocalID = 10000; }

		if (step > 0) {
			iLocalID += step;
			SaveLocalId("LocalID", iLocalID);
		}

		char buffer[MAX_PATH];
		snprintf(buffer, sizeof(buffer), "%d", iLocalID);
		return buffer;
	}
	void QryInstrument(LONG iQryPage)
	{
		COUTTIME << "�����Լ�� " << iQryPage * 1000 << " �� " << iQryPage * 1000 + 999 << " ��" << endl;

		CFutureQryInstrumentField qry = {};
		safe_cpy(qry.ExchangeNo, "CME");
		safe_cpy(qry.CommodityNo, "");
		qry.PageIndex = 1000 * iQryPage;

		if (!m_pFutureApi->ReqQryInstrument(&qry, 0)) {
			COUTTIME << qry.ErrorDescription << endl;
		}
	}
	LONG ReadLocalId(const char* lpszKey, LONG iDefault)
	{
#ifdef _WIN32
		char szBuffer[MAX_PATH];
		if (::GetPrivateProfileStringA(APP_NAME, lpszKey, NULL, szBuffer, MAX_PATH, LOCALID_FILE) > 0)
		{
			if (szBuffer[0] == L'0' && (szBuffer[1] == L'x' || szBuffer[1] == L'X')) {
				return strtoul(szBuffer, NULL, 16);
			}
			else {
				return atoi(szBuffer);
			}
		}
		return iDefault;
#else
		char szBuffer[MAX_PATH];
		if (::ini_gets(APP_NAME, lpszKey, "", szBuffer, MAX_PATH, LOCALID_FILE) > 0)
		{
			if (szBuffer[0] == L'0' && (szBuffer[1] == L'x' || szBuffer[1] == L'X')) {
				return strtoul(szBuffer, NULL, 16);
			}
			else {
				return atoi(szBuffer);
			}
		}
		return iDefault;
#endif
	}
	void SaveLocalId(const char* lpszKey, LONG iValue, BOOL bHex = FALSE)
	{
		char szBuffer[MAX_PATH];
		snprintf(szBuffer, MAX_PATH, bHex ? "0x%X" : "%d", iValue);

#ifdef _WIN32
		::WritePrivateProfileStringA(APP_NAME, lpszKey, szBuffer, LOCALID_FILE);
#else
		ini_puts(APP_NAME, lpszKey, szBuffer, LOCALID_FILE);
#endif
	}

	// ��ѯ����
public:
	//�����ĵ��÷�����Ҫ���Ӳ�ѯ�����һ���û��ɽ��ţ���һ�β�֪������ɽ��ſ��Բ����룩��
	//������������������󣬾�Ĭ�Ϸ���ǰ500����Ϣ//update 2020.04.29 ywh
	void ReqQryTrade()
	{
		/*while (1)
		{
			CrossSleep(1000);
			ReqQryVersion();
		}*/
		traderQuryCounter = 0;
		CFutureQryTradeField qry = {};		

		safe_cpy(qry.UserId, m_appConfig.userId.c_str());
		char buf[100];
		int temp = TRADE_MAX_NUM_ONE_PAGE;
		snprintf(buf, sizeof(buf), "%d", temp);
		safe_cpy(qry.maxItemNumOnePage, buf);
		safe_cpy(qry.lastFilledNo, "");

		if (!m_pFutureApi->ReqQryTrade(&qry, 0)) {
			COUTTIME << qry.ErrorDescription << endl;
		}
	}
	void ReqQryOrder()
	{
		CFutureQryOrderField qry = {};
		safe_cpy(qry.UserId, m_appConfig.userId.c_str());

		if (!m_pFutureApi->ReqQryOrder(&qry, 0)) {
			COUTTIME << qry.ErrorDescription << endl;
		}
		//while (1)
		//{
		//	CrossSleep(1000);
		//	//m_pFutureApi->SendCommand("TEST001@@@@@@@@@@&");
		//	
		//}
		
	}
	void ReqUserLogin()
	{
		CFutureReqUserLoginField req = {};

		COUTTIME << "�û���:" << m_appConfig.userId << endl;
		COUTTIME << "����:" << "******" << endl;

		safe_cpy(req.UserId, m_appConfig.userId.c_str());
		safe_cpy(req.UserPwd, m_appConfig.password.c_str());
		safe_cpy(req.AuthorCode, m_appConfig.authorCode.c_str());
		safe_cpy(req.MacAddress, m_appConfig.macAddress.c_str());
		safe_cpy(req.ComputerName, m_appConfig.computerName.c_str());
		safe_cpy(req.SoftwareName, m_appConfig.softwareName.c_str());
		safe_cpy(req.SoftwareVersion, m_appConfig.softwareVersion.c_str());

		if (m_pFutureApi->ReqUserLogin(&req, 0)) {
			COUTTIME << "��ʼ��¼...." << endl;
		}
		else {
			COUTTIME << req.ErrorDescription << endl;
		}
	}
	void ReqUserLogout()
	{
		CFutureReqUserLogoutField req = {};
		safe_cpy(req.UserId, m_appConfig.userId.c_str());

		if (!m_pFutureApi->ReqUserLogout(&req, 0)) {
			COUTTIME << req.ErrorDescription << endl;
		}
	}
	void ReqQryVersion()
	{
		CFutureQryVersionField qry = {};
		if (!m_pFutureApi->ReqQryVersion(&qry, 0)) {
			COUTTIME << qry.ErrorDescription << endl;
		}
	}
	void ReqQryCapital()
	{
		CFutureQryCapitalField qry = {};
		if (!m_pFutureApi->ReqQryCapital(&qry, 0)) {
			COUTTIME << qry.ErrorDescription << endl;
		}
	}
	void ReqVerifyCode()
	{
		CFutureReqVerifyCodeField qry = {};
		safe_cpy(qry.UserId, m_appConfig.userId.c_str());
		safe_cpy(qry.UserPwd, m_appConfig.password.c_str());
		safe_cpy(qry.Type, "I");
		safe_cpy(qry.Question, "1");
		safe_cpy(qry.Answer, "2");
		safe_cpy(qry.MobileNumber, "18621908120");
		safe_cpy(qry.VerifyCode, "0");

		if (!m_pFutureApi->ReqVerifyCode(&qry, 0)) {
			COUTTIME << qry.ErrorDescription << endl;
		}
	}
	void ReqSafeVerify()
	{
		CFutureReqSafeVerifyField qry = {};
		safe_cpy(qry.UserId, m_appConfig.userId.c_str());
		safe_cpy(qry.UserPwd, m_appConfig.password.c_str());
		safe_cpy(qry.Type, "1");
		safe_cpy(qry.Question, "1");
		safe_cpy(qry.Answer, "song_pass_1234");
		safe_cpy(qry.SaveMac, "1");
		safe_cpy(qry.MacAddress, m_appConfig.macAddress.c_str());

		if (!m_pFutureApi->ReqSafeVerify(&qry, 0)) {
			COUTTIME << qry.ErrorDescription << endl;
		}
	}
	void ReqQryPosition()
	{
		CFutureQryPositionField qry = {};
		if (!m_pFutureApi->ReqQryPosition(&qry, 0)) {
			COUTTIME << qry.ErrorDescription << endl;
		}
	}
	void ReqQryCurrency()
	{
		CFutureQryCurrencyField qry = {};
		if (!m_pFutureApi->ReqQryCurrency(&qry, 0)) {
			COUTTIME << qry.ErrorDescription << endl;
		}
	}
	void ReqQryStrategy()
	{
		CFutureQryStrategyField qry = {};
		safe_cpy(qry.ExchangeNo, "CME");
		if (!m_pFutureApi->ReqQryStrategy(&qry, 0)) {
			COUTTIME << qry.ErrorDescription << endl;
		}
	}
	void ReqOrderInsert()
	{
		auto find = m_mapAccounts.find("NY-USD");
		if (find == m_mapAccounts.end())
			return;

		CFutureReqOrderInsertField req = {0};
		string localID = BuildLocalID(1);

		safe_cpy(req.UserId, m_appConfig.userId.c_str());
		safe_cpy(req.AccountNo, find->second.AccountNo);
		safe_cpy(req.LocalNo, localID.c_str());
		safe_cpy(req.ExchangeCode, "DL-DCE");
		safe_cpy(req.ContractCode, "DL-i2401");
		safe_cpy(req.TIF, DERIVATIVE_GTC_TIF);
        safe_cpy(req.BidAskFlag, DERIVATIVE_BID);
		safe_cpy(req.OrderQty, "1");
        safe_cpy(req.OpenCloseFlag, DERIVATIVE_CLOSE_POS_FLAG)
		//safe_cpy(req.Tag50, "LIKAN");
		//safe_cpy(req.OrgOrderLocationID, "CN");
		//safe_cpy(req.TreatyCode, "A-UC2009");
		safe_cpy(req.OrderPrice, "974.5");
        safe_cpy(req.OrderType, DERIVATIVE_LIMIT_ORDER);

		
		for (int i = 0; i < 1; i++) {
			if (!m_pFutureApi->ReqOrderInsert(&req, 0)) {
				COUTTIME << req.ErrorDescription << endl;
			}
		}

	}
	void ReqOrderModify()
	{
		if (m_systemNo.size() == 0 || m_orderNo.size() == 0) {
			COUTTIME << "ϵͳ�ţ������Ų���Ϊ��" << endl;
			return;
		}

		auto find = m_mapAccounts.find("USD");
		if (find == m_mapAccounts.end())
			return;

		string localID = BuildLocalID(1);

		CFutureReqOrderModifyField req = {0};
		safe_cpy(req.SystemNo, m_systemNo.c_str());
		safe_cpy(req.UserId, m_appConfig.userId.c_str());
		//safe_cpy(req.UserType, "1");
		safe_cpy(req.LocalNo, localID.c_str());
		safe_cpy(req.AccountNo, find->second.AccountNo);
		//safe_cpy(req.TradePwd, find->second.TradePwd);
		safe_cpy(req.OrderNo, m_orderNo.c_str());
		safe_cpy(req.ExchangeCode, "CME");
		safe_cpy(req.ContractCode, "6B2306");
		safe_cpy(req.BidAskFlag, DERIVATIVE_ASK);
		safe_cpy(req.OrderQty, "10");
		safe_cpy(req.OrderPrice, "70.88");
		//safe_cpy(req.FilledNumber, "0");
		safe_cpy(req.ModifyQty, "14");
		safe_cpy(req.ModifyPrice, "0.3");
		//safe_cpy(req.TradeType, "1");
		safe_cpy(req.OrderType, DERIVATIVE_MARKET_ORDER);
		safe_cpy(req.TriggerPrice, "0.000");
		//safe_cpy(req.OrgOrderLocationID, "CN");


		if (!m_pFutureApi->ReqOrderModify(&req, 0)) {
			COUTTIME << req.ErrorDescription << endl;
		}
	}
	void ReqOrderCancel()
	{
		//if (m_systemNo.size() == 0 || m_orderNo.size() == 0) {
		//	COUTTIME <<"ϵͳ�ţ������Ų���Ϊ��" << endl;
		//	return;
		//}

		auto find = m_mapAccounts.find("NY-USD");
		if (find == m_mapAccounts.end())
			return;

		CFutureReqOrderCancelField req = {0};
		string localID = BuildLocalID(1);

		safe_cpy(req.UserId, m_appConfig.userId.c_str());
		safe_cpy(req.LocalNo, localID.c_str());
		safe_cpy(req.AccountNo, find->second.AccountNo);
		//safe_cpy(req.TradePwd, find->second.TradePwd);
		safe_cpy(req.SystemNo, m_systemNo.c_str());
        safe_cpy(req.OrderNo, "127460358");
        safe_cpy(req.ExchangeCode, "DL-DCE");
        safe_cpy(req.ContractCode, "DL-i2401");
        safe_cpy(req.BidAskFlag, DERIVATIVE_ASK);
        //safe_cpy(req.OpenCloseFlag, DERIVATIVE_CLOSE_POS_FLAG);
		//safe_cpy(req.Tag50, "ywh2");
		//safe_cpy(req.OrgOrderLocationID, "CN");

		if (!m_pFutureApi->ReqOrderCancel(&req, 0)) {
			COUTTIME << req.ErrorDescription << endl;
		}
	}
	void ReqQryExchange()
	{
		CFutureQryExchangeField qry = {};
		if (!m_pFutureApi->ReqQryExchange(&qry, 0)) {
			COUTTIME << qry.ErrorDescription << endl;
		}
	}
	void ReqGetQuestion()
	{
		CFutureReqGetQuestionField qry = {};
		if (!m_pFutureApi->ReqGetQuestion(&qry, 0)) {
			COUTTIME << qry.ErrorDescription << endl;
		}
	}
	void ReqSetVerifyQA()
	{
		CFutureReqSetVerifyQAField qry = {};
		safe_cpy(qry.UserId, m_appConfig.userId.c_str());
		safe_cpy(qry.UserPwd, m_appConfig.password.c_str());
		safe_cpy(qry.Type, "1");
		safe_cpy(qry.Question, "1");
		safe_cpy(qry.Answer, "song_pass_1234");
		safe_cpy(qry.SaveMac, "1");

		if (!m_pFutureApi->ReqSetVerifyQA(&qry, 0)) {
			COUTTIME << qry.ErrorDescription << endl;
		}
	}
	void ReqQryCommodity()
	{
		CFutureQryCommodityField qry = {};
		safe_cpy(qry.UpdateDate, "");
		safe_cpy(qry.ExchangeNo, "");

		if (!m_pFutureApi->ReqQryCommodity(&qry, 0)) {
			COUTTIME << qry.ErrorDescription << endl;
		}
	}
	void ReqQryInstrument()
	{
		m_iQryPage = 0;
		QryInstrument(m_iQryPage);
	}
	void ReqChangePassword()
	{
		CFutureReqPasswordUpdateField req = {};
		safe_cpy(req.UserId, m_appConfig.userId.c_str());
		safe_cpy(req.OldPassword, "888888");
		safe_cpy(req.NewPassword, "222222");
		if (!m_pFutureApi->ReqPasswordUpdate(&req, 0)) {
			COUTTIME << req.ErrorDescription << endl;
		}
	}
	void ReqQryExchangeTime()
	{
		CFutureQryExchangeTimeField qry = {};
		if (!m_pFutureApi->ReqQryExchangeTime(&qry, 0)) {
			COUTTIME << qry.ErrorDescription << endl;
		}
	}
	void ReqQryCommodityTime()
	{
		CFutureQryCommodityTimeField qry = {};
		safe_cpy(qry.ExchangeNo, "CME");
		safe_cpy(qry.CommodityNo, "");

		if (!m_pFutureApi->ReqQryCommodityTime(&qry, 0)) {
			COUTTIME << qry.ErrorDescription << endl;
		}
	}
	void ReqQryTotalPosition()
	{
		CFutureQryTotalPositionField qry = {};
		safe_cpy(qry.AccountNo, m_appConfig.userId.c_str());

		if (!m_pFutureApi->ReqQryTotalPosition(&qry, 0)) {
			COUTTIME << qry.ErrorDescription << endl;
		}
	}
	void ReqQryStrategyDetail()
	{
		CFutureQryStrategyDetailField qry = {};
		safe_cpy(qry.StartegyCommodityNo, "CL-BZ");

		if (!m_pFutureApi->ReqQryStrategyDetail(&qry, 0)) {
			COUTTIME << qry.ErrorDescription << endl;
		}
	}

	// ���Ӻ���
public:
	virtual void OnFrontConnected()
	{
		COUTTIME << "���ӷ������ɹ�" << endl;
		m_bIsLogin = false;
		ReqUserLogin();
	}
	virtual void OnFrontDisconnected(int iReason)
	{
		m_bIsLogin = false;
		COUTTIME << "���ӶϿ�, ԭ�� = " << iReason << "." << endl;
	}
	virtual void OnHeartBeatWarning(int iTimeLapse)
	{
		COUTTIME << "����:" << iTimeLapse << endl;
	}

	// ���ͺ���
public:
	virtual void OnRtnTrade(CFutureRtnTradeField *pRtnTrade, CFutureRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		COUTTIME << "UserId= " << pRtnTrade->UserId << 
			", OrderNo= " << pRtnTrade->OrderNo << 
			", FilledPrice= " << pRtnTrade->FilledPrice << endl;
		if (bIsLast) { COUTTIME << "-----------Over------------" << endl; }
	}
	virtual void OnRtnOrder(CFutureRtnOrderField *pRtnOrder, CFutureRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		COUTTIME << "OrderNo= " << pRtnOrder->OrderNo << 
			", FilledQty= " << pRtnOrder->FilledQty <<
			", FilledAvgPrice= " << pRtnOrder->FilledAvgPrice << endl;
		if (bIsLast) { COUTTIME << "-----------Over------------" << endl; }
	}
	virtual void OnRtnCapital(CFutureRtnCapitalField *pRtnCapital, CFutureRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		COUTTIME << "AccountNo= " << pRtnCapital->AccountNo << 
			", OrderNo= " << pRtnCapital->OrderNo << endl;
		if (bIsLast) { COUTTIME << "-----------Over------------" << endl; }
	}
	virtual void OnRtnPosition(CFutureRtnPositionField *pRtnPosition, CFutureRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		COUTTIME << "AccountNo= " << pRtnPosition->AccountNo << 
			", OrderNo= " << pRtnPosition->OrderNo << endl;
		if (bIsLast) { COUTTIME << "-----------Over------------" << endl; }
	}

	// ��ͨ����
public:
	virtual void OnRspNeedVerify(bool bFirstLogin, bool bHasSetQA)
	{
		m_bIsLogin = true;
		if (bFirstLogin) {
			COUTTIME << "���ǵ�һ�ε�¼����Ҫ���ڽ���˫����֤" << endl;
			ReqSetVerifyQA();
		}

		if (bHasSetQA) {
			COUTTIME << "�Ѿ����ù�����" << endl;
		}
	}
	virtual void OnRspUserLogin(CFutureRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		if (pRspInfo->ErrorID) {
			COUTTIME << "��¼�ڻ����׷�����ʧ��." << endl;
			COUTTIME << "ErrorID = " << pRspInfo->ErrorID << endl;
			COUTTIME << "ErrorMsg = " << pRspInfo->ErrorMsg << endl;
			m_bIsLogin = false;
		}
		else {
			COUTTIME << "��¼�ڻ����׷������ɹ�." << endl;
			COUTTIME << "�ʽ��˺�: ";
			m_bIsLogin = true;
		}
	}
	virtual void OnRspUserLogout(CFutureRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		COUTTIME << "ErrorID = " << pRspInfo->ErrorID << endl;
		COUTTIME << "ErrorMsg = " << pRspInfo->ErrorMsg << endl;

		COUTTIME << "���9527��\n";
		m_bIsLogin = false;
	}
	virtual void OnRspSafeVerify(CFutureRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		COUTTIME << "ErrorID = " << pRspInfo->ErrorID << endl;
		COUTTIME << "ErrorMsg = " << pRspInfo->ErrorMsg << endl;
		COUTTIME << "Save verify\n";
	}
	virtual void OnRspVerifyCode(CFutureRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		COUTTIME << "ErrorID = " << pRspInfo->ErrorID << endl;
		COUTTIME << "ErrorMsg = " << pRspInfo->ErrorMsg << endl;
	}
	virtual void OnRspSetVerifyQA(CFutureRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		COUTTIME << "ErrorID = " << pRspInfo->ErrorID << endl;
		COUTTIME << "ErrorMsg = " << pRspInfo->ErrorMsg << endl;
		ReqSafeVerify();
	}
	virtual void OnRspAccount(CFutureRspAccountField *pRspAccount, CFutureRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		if (pRspInfo->ErrorID) {
			COUTTIME << "ErrorID = " << pRspInfo->ErrorID << endl;
			COUTTIME << "ErrorMsg = " << pRspInfo->ErrorMsg << endl;
		}
		else {
			cout << pRspAccount->CurrencyNo << (bIsLast ? ".\r\n" : ";");
			m_mapAccounts.insert(make_pair(pRspAccount->CurrencyNo, *pRspAccount));
			if (bIsLast) {
				COUTTIME << "��ȡ�ʽ��˻����." << endl;
				COUTTIME << endl;
			}
		}
	}
	virtual void OnRspQuestion(CFutureRspQuestionField *pRspQuestion, CFutureRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		COUTTIME << "QuestionId= " << pRspQuestion->QuestionId << 
			", QuestionCN= " << pRspQuestion->QuestionCN << 
			", QuestionEN= " << pRspQuestion->QuestionEN << endl;
	}
	virtual void OnRspOrderInsert(CFutureRspOrderInsertField *pRspOrderInsert, CFutureRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		COUTTIME << "ErrorID = " << pRspInfo->ErrorID << endl;
		COUTTIME << "SystemNo = " << pRspOrderInsert->SystemNo << endl;
		COUTTIME << "LocalNo = " << pRspOrderInsert->LocalNo << endl;

		if (pRspInfo->ErrorID) {
			m_systemNo = "";
			m_orderNo = "";
			COUTTIME << "����ԭ��"<< pRspInfo->ErrorMsg<<endl;
		}
		else {
			m_systemNo = pRspOrderInsert->SystemNo;
			m_orderNo = pRspOrderInsert->OrderNo;
		}
	}
	virtual void OnRspOrderModify(CFutureRspOrderModifyField *pRspOrderModify, CFutureRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		COUTTIME << "ErrorID = " << pRspInfo->ErrorID << endl;
		COUTTIME << "UserId = " << pRspOrderModify->UserId << endl;
		if (pRspInfo->ErrorID) {
			m_systemNo = "";
			m_orderNo = "";
			COUTTIME << "����ԭ��" << pRspInfo->ErrorMsg << endl;
		}
	}
	virtual void OnRspOrderCancel(CFutureRspOrderCancelField *pRspOrderCancel, CFutureRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		COUTTIME << "ErrorID = " << pRspInfo->ErrorID << endl;
		COUTTIME << "SystemNo = " << pRspOrderCancel->SystemNo << endl;
		if (pRspInfo->ErrorID) {
			m_systemNo = "";
			m_orderNo = "";
			COUTTIME << "����ԭ��" << pRspInfo->ErrorMsg << endl;
		}
	}
	virtual void OnRspPasswordUpdate(CFutureRspPasswordUpdateField *pRspPasswordUpdate, CFutureRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		COUTTIME << "ErrorID = " << pRspInfo->ErrorID << endl;
		COUTTIME << "UserId = " << pRspPasswordUpdate->UserId << endl;
	}

	// ��ѯ����
public:
	virtual void OnRspQryOrder(CFutureRspOrderField *pRspOrder, CFutureRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		COUTTIME << "UserId= " << pRspOrder->UserId <<
			", OrderNo= " << pRspOrder->OrderNo << 
			", OrderPrice=" << pRspOrder->OrderPrice << 
			", BidAskFlag=" << pRspOrder->BidAskFlag << endl;
		if (bIsLast) { COUTTIME << "-----------Over------------" << endl; }
	}
	virtual void OnRspQryTrade(CFutureRspTradeField *pRspTrade, CFutureRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		
		
		COUTTIME << "FilledNo=" << pRspTrade->FilledNo <<
			", FilledPrice= " << pRspTrade->FilledPrice << endl;
		traderQuryCounter++;
		// ...


		if (bIsLast)
		{ 
			if (traderQuryCounter == TRADE_MAX_NUM_ONE_PAGE )
			{
				traderQuryCounter = 0;

				// query next page
				CFutureQryTradeField qry = {};
				safe_cpy(qry.UserId, m_appConfig.userId.c_str());
				safe_cpy(qry.lastFilledNo, pRspTrade->FilledNo);

				

				char buf[100];
				int temp = TRADE_MAX_NUM_ONE_PAGE;
				snprintf(buf, sizeof(buf), "%d", temp);

				safe_cpy(qry.maxItemNumOnePage, buf);
				
				CrossSleep(1500);

				if (!m_pFutureApi->ReqQryTrade(&qry, 0)) {
					COUTTIME << qry.ErrorDescription << endl;
				}
				COUTTIME << "\n";
				

			}
			else
				COUTTIME << "-----------All Over------------" << endl; }
	}
	virtual void OnRspQryVersion(CFutureRspVersionField *pRspVersion, CFutureRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		COUTTIME << "Version= " << pRspVersion->Version <<
			", MustUpdate= " << pRspVersion->MustUpdate << endl;
	}
	virtual void OnRspQryCapital(CFutureRspCapitalField *pRspCapital, CFutureRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		COUTTIME << "CurrencyNo= " << pRspCapital->CurrencyNo <<
			", TodayAmount= " << pRspCapital->TodayInitialBalance <<
			", CanCashOut= " << pRspCapital->CanCashOutMoneyAmount << endl;
		if (bIsLast) { COUTTIME << "-----------Over------------" << endl; }
	}
	virtual void OnRspQryPosition(CFutureRspPositionField *pRspPosition, CFutureRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		COUTTIME << "ContractNo= " << pRspPosition->ClientNo <<
			", ContractNo= " << pRspPosition->ContractNo << 
			", CurrencyNo= " << pRspPosition->CurrencyNo << 
			", HoldVol= " << pRspPosition->HoldVol << 
			", HoldPrice= " << pRspPosition->HoldPrice << endl;
		if (bIsLast) { COUTTIME << "-----------Over------------" << endl; }
	}
	virtual void OnRspQryExchange(CFutureRspExchangeField *pRspExchange, CFutureRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		COUTTIME << "ExchangeNo= " << pRspExchange->ExchangeNo <<
			", ExchangeName= " << pRspExchange->ExchangeName << endl;
		if (bIsLast) { COUTTIME << "-----------Over------------" << endl; }
	}
	virtual void OnRspQryCurrency(CFutureRspCurrencyField *pRspCurrency, CFutureRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		COUTTIME << "CurrencyNo= " << pRspCurrency->CurrencyNo <<
			", CurrencyName= " << pRspCurrency->CurrencyName << endl;
		if (bIsLast) { COUTTIME << "-----------Over------------" << endl; }
	}
	virtual void OnRspQryStrategy(CFutureRspStrategyField *pStrategyField, CFutureRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		COUTTIME << "CommodityCode= " << pStrategyField->CommodityCode <<
			", ExchangeNo= " << pStrategyField->ExchangeNo << 
			", ContractNo= " << pStrategyField->ContractNo <<
			", ContractFName= " << pStrategyField->ContractFName << endl;
		if (bIsLast) { COUTTIME << "-----------Over------------" << endl; }
	}
	virtual void OnRspQryCommodity(CFutureRspCommodityField *pRspCommodity, CFutureRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		COUTTIME << "ExchangeNo= " << pRspCommodity->ExchangeNo 
			<< ", ExchangeNo2= " << pRspCommodity->ExchangeNo2 
			<< ", Name= " << pRspCommodity->Name 
			<< ", RegDate= " << pRspCommodity->RegDate
			<< endl;
	}
	virtual void OnRspQryInstrument(CFutureRspInstrumentField *pRspInstrument, CFutureRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		if (pRspInfo->ErrorID) {
			COUTTIME << "ErrorID= " << pRspInfo->ErrorID << endl;
			COUTTIME << "-----------Over------------" << endl;
		}
		else {
			COUTTIME << "ExchangeName= " << pRspInstrument->ExchangeNo <<
				", CommodityCode= " << pRspInstrument->CommodityCode << endl;
			if (bIsLast) {
				m_iQryPage++;
				QryInstrument(m_iQryPage);
			}
		}
	}
	virtual void OnRspQryExchangeTime(CFutureRspExchangeTimeField *pRspExchangeTime, CFutureRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		COUTTIME << "ExchangeNo= " << pRspExchangeTime->ExchangeNo <<
			", SummerBegin= " << pRspExchangeTime->SummerBegin << 
			", WinterBegin= " << pRspExchangeTime->WinterBegin << endl;
		if (bIsLast) { COUTTIME << "-----------Over------------" << endl; }
	}
	virtual void OnRspQryCommodityTime(CFutureRspCommodityTimeField *pRspCommodityTime, CFutureRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		COUTTIME << "ExchangeNo= " << pRspCommodityTime->ExchangeNo <<
			", CommodityNo= " << pRspCommodityTime->CommodityNo <<
			", Summer= " << pRspCommodityTime->Summer <<
			", CrossTrade= " << pRspCommodityTime->CrossTrade <<
			", Opendate= " << pRspCommodityTime->Opendate << 
			", Closingdate= " << pRspCommodityTime->Closingdate << endl;
		if (bIsLast) { COUTTIME << "-----------Over------------" << endl; }
	}
	virtual void OnRspQryTotalPosition(CFutureRspTotalPositionField *pRspTotalPosition, CFutureRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		COUTTIME << "AccountNo= " << pRspTotalPosition->AccountNo <<
			", CurrPrice= " << pRspTotalPosition->CurrPrice <<
			", FilledQty= " << pRspTotalPosition->FilledQty <<
			", ProfitLoss= " << pRspTotalPosition->ProfitLoss <<
			", OrderNo= " << pRspTotalPosition->OrderNo << endl;

		if (bIsLast) { COUTTIME << "-----------Over------------" << endl; }
	}
	virtual void OnRspQryStrategyDetail(CFutureRspStrategyDetailField* pRspStrategyDetail, CFutureRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		COUTTIME << "ContractNo= " << pRspStrategyDetail->ContractNo <<
			", CommodityNo= " << pRspStrategyDetail->CommodityNo << endl;
		if (bIsLast) { COUTTIME << "-----------Over------------" << endl; }
	}
};


