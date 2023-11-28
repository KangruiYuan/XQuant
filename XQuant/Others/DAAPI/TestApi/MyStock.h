
#pragma once

#include "DAStockApi.h"

using namespace Directaccess;

class CMyStock : public IStockEvent
{
private:
	typedef map<string, CStockRspAccountField> CMapAccount;

	// ��Ա����
private:
	string			m_orderNo;				// ���ص���
	CLockBool		m_bIsLogin;				// �Ƿ��½
	string			m_systemNo;				// ϵͳ����
	LONG			m_iQryPage;				// ��ҳ��־
	CStockApi*		m_pStockApi;			// ��Ʊ�ӿ�
	CAppConfig		m_appConfig;			// �����ļ�
	CMapAccount		m_mapAccounts;			// �����˺�

	// ��������
public:
	CMyStock() {
		m_iQryPage = 0;
		m_pStockApi = 0;
		m_bIsLogin = false;
	}
	virtual ~CMyStock() {}

	// ��������
public:
	bool IsLogin()
	{
		return m_bIsLogin;
	}
	bool IsCreate()
	{
		return m_pStockApi != NULL;
	}
	bool Create()
	{
		if (m_pStockApi) {
			Destroy();
		}
		m_pStockApi = CStockApi::CreateStockApi(true, "TestStock.log");
		if (m_pStockApi) {
			COUTTIME << "---------------- API ��Ϣ ----------------" << endl;
			COUTTIME << "API Version: " << m_pStockApi->GetVersion() << endl;
			COUTTIME << "Server Addr: " << m_appConfig.serverAddress.c_str() << endl;
			COUTTIME << "User ID: " << m_appConfig.userId.c_str() << endl;
			COUTTIME << endl;

			char addr[MAX_PATH];
			snprintf(addr, MAX_PATH, "tcp://%s", m_appConfig.serverAddress.c_str());

			LONG beat = atol(m_appConfig.heartBeat.c_str());

			m_pStockApi->RegisterSpi(this);
			m_pStockApi->RegisterNameServer(addr);
			m_pStockApi->SetHeartBeatTimeout(beat);
			m_pStockApi->Init();


			/*Sleep(3000);
			ReqUserLogin();*/
			COUTTIME << "��ʼ���ӹ�Ʊ���׷�����...." << endl;
			COUTTIME << endl;

			return true;
		}
		return false;
	}
	void Destroy()
	{
		if (m_pStockApi) {
			if (m_bIsLogin) {
				m_bIsLogin = false;
				CStockReqUserLogoutField req = {};
				safe_cpy(req.UserId, m_appConfig.userId.c_str());
				m_pStockApi->ReqUserLogout(&req, 0);
				CrossSleep(250);
			}

			m_pStockApi->Release();
			m_pStockApi = NULL;
			COUTTIME << "���� CMyStock" << endl;
		}
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
	void QryInstrument(LONG iQryPage)
	{
		COUTTIME << "�����Լ�� " << iQryPage * 1000 << " �� " << iQryPage * 1000 + 999 << " ��" << endl;

		CStockQryInstrumentField qry = {};
		safe_cpy(qry.ExchangeNo, "HKEX");
		safe_cpy(qry.ModifyDay, "20200808");
		qry.PageIndex = 1000 * iQryPage;
		if (!m_pStockApi->ReqQryInstrument(&qry, 0)) {
			COUTTIME << qry.ErrorDescription << endl;
		}
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
	void ReqQryTick()
	{
		CStockQryTickField qry = {};
		if (!m_pStockApi->ReqQryTick(&qry, 0)) {
			COUTTIME << qry.ErrorDescription << endl;
		}
	}
	void ReqQryOrder()
	{
		CStockQryOrderField qry = {};
		safe_cpy(qry.UserId, m_appConfig.userId.c_str());
		if (!m_pStockApi->ReqQryOrder(&qry, 0)) {
			COUTTIME << qry.ErrorDescription << endl;
		}
	}

	void ReqQryTrade()
	{
		CStockQryTradeField qry = {};
		safe_cpy(qry.UserId, m_appConfig.userId.c_str());
				

		if (!m_pStockApi->ReqQryTrade(&qry, 0)) {
			COUTTIME << qry.ErrorDescription << endl;
		}
	}
	void ReqUserLogin()
	{
		CStockReqUserLoginField req = {};

		COUTTIME << "�û���:" << m_appConfig.userId << endl;
		COUTTIME << "����:" << "******" << endl;

		safe_cpy(req.UserId, m_appConfig.userId.c_str());
		safe_cpy(req.UserPwd, m_appConfig.password.c_str());
		safe_cpy(req.AuthorCode, m_appConfig.authorCode.c_str());
		safe_cpy(req.MacAddress, m_appConfig.macAddress.c_str());
		safe_cpy(req.ComputerName, m_appConfig.computerName.c_str());
		safe_cpy(req.SoftwareName, m_appConfig.softwareName.c_str());
		safe_cpy(req.SoftwareVersion, m_appConfig.softwareVersion.c_str());

		if (m_pStockApi->ReqUserLogin(&req, 0)) {
			COUTTIME << "��ʼ��¼...." << endl;
		}
		else {
			COUTTIME << req.ErrorDescription << endl;
		}
	}
	void ReqVerifyCode()
	{
		CStockReqVerifyCodeField req = {};

		safe_cpy(req.Type, "I");
		safe_cpy(req.Question, "1");
		safe_cpy(req.Answer, "1");
		safe_cpy(req.VerifyCode, "0");
		safe_cpy(req.MobileNumber, "18621908120");
		safe_cpy(req.UserId, m_appConfig.userId.c_str());
		safe_cpy(req.UserPwd, m_appConfig.password.c_str());

		if (!m_pStockApi->ReqVerifyCode(&req, 0)) {
			COUTTIME << req.ErrorDescription << endl;
		}
	}
	void ReqSafeVerify()
	{
		CStockReqSafeVerifyField req = {};

		safe_cpy(req.Type, "1");
		safe_cpy(req.Answer, "a");
		safe_cpy(req.SaveMac, "1");
		safe_cpy(req.Question, "1");
		safe_cpy(req.UserId, m_appConfig.userId.c_str());
		safe_cpy(req.UserPwd, m_appConfig.password.c_str());
		safe_cpy(req.MacAddress, m_appConfig.macAddress.c_str());

		if (!m_pStockApi->ReqSafeVerify(&req, 0)) {
			COUTTIME << req.ErrorDescription << endl;
		}
	}
	void ReqQryCapital()
	{
		CStockQryCapitalField qry = {};
		if (!m_pStockApi->ReqQryCapital(&qry, 0)) {
			COUTTIME << qry.ErrorDescription << endl;
		}
	}
	void ReqQryVersion()
	{
		CStockQryVersionField qry = {};
		if (!m_pStockApi->ReqQryVersion(&qry, 0)) {
			COUTTIME << qry.ErrorDescription << endl;
		}
	}
	void ReqGetQuestion()
	{
		CStockReqGetQuestionField req = {};
		if (!m_pStockApi->ReqGetQuestion(&req, 0)) {
			COUTTIME << req.ErrorDescription << endl;
		}
	}
	void ReqSetVerifyQA()
	{
		CStockReqSetVerifyQAField req = {};
		safe_cpy(req.UserId, m_appConfig.userId.c_str());
		safe_cpy(req.UserPwd, m_appConfig.password.c_str());
		safe_cpy(req.Type, "1");
		safe_cpy(req.Question, "1");
		safe_cpy(req.Answer, "a");
		safe_cpy(req.SaveMac, "1");

		if (!m_pStockApi->ReqSetVerifyQA(&req, 0)) {
			COUTTIME << req.ErrorDescription << endl;
		}
	}
	void ReqQryPosition()
	{
		CStockQryPositionField qry = {};
		if (!m_pStockApi->ReqQryPosition(&qry, 0)) {
			COUTTIME << qry.ErrorDescription << endl;
		}
	}
	void ReqQryExchange()
	{
		CStockQryExchangeField qry = {};
		if (!m_pStockApi->ReqQryExchange(&qry, 0)) {
			COUTTIME << qry.ErrorDescription << endl;
		}
	}
	void ReqQryCurrency()
	{
		CStockQryCurrencyField qry = {};
		if (!m_pStockApi->ReqQryCurrency(&qry, 0)) {
			COUTTIME << qry.ErrorDescription << endl;
		}
	}
	void ReqOrderInsert()
	{
		auto find = m_mapAccounts.find("HKD");
		if (find == m_mapAccounts.end())
			return;

		CStockReqOrderInsertField req = {};

		string localID = BuildLocalID(1);

		safe_cpy(req.UserId, m_appConfig.userId.c_str());
		safe_cpy(req.AccountNo, find->second.AccountNo);
		safe_cpy(req.LocalNo, localID.c_str());
		//safe_cpy(req.TradePwd, find->second.TradePwd);
		//safe_cpy(req.IsRiskOrder, "Y");
		safe_cpy(req.ExchangeCode, "HKEX");
		safe_cpy(req.ContractCode, "00004.HK");
		safe_cpy(req.TIF, STOCK_TDY_TIF);
		safe_cpy(req.BidAskFlag, STOCK_BID);
		safe_cpy(req.OrderQty, "1000");
		safe_cpy(req.OrderPrice, "17.560");
		safe_cpy(req.OrderType, STOCK_LIMIT_ORDER);

		if (!m_pStockApi->ReqOrderInsert(&req, 0)) {
			COUTTIME << req.ErrorDescription << endl;
		}
	}
	void ReqOrderModify()
	{

		if (m_systemNo.size() == 0 || m_orderNo.size() == 0) {
			COUTTIME << "ϵͳ�ţ������Ų���Ϊ��" << endl;
			return;
		}

		auto find = m_mapAccounts.find("HKD");//HKD USD
		if (find == m_mapAccounts.end())
			return;

		string localID = BuildLocalID(1);

		CStockReqOrderModifyField req = {};

		safe_cpy(req.SystemNo, m_systemNo.c_str());
		safe_cpy(req.UserId, m_appConfig.userId.c_str());
		//safe_cpy(req.UserType, "1");
		safe_cpy(req.LocalNo, localID.c_str());
		safe_cpy(req.AccountNo, find->second.AccountNo);
		//safe_cpy(req.TradePwd, find->second.TradePwd);
		safe_cpy(req.OrderNo, m_orderNo.c_str());
		safe_cpy(req.ExchangeCode, "HKEX");
		safe_cpy(req.ContractCode, "00004.HK");
		safe_cpy(req.BidAskFlag, STOCK_BID);
		safe_cpy(req.OrderQty, "1000");
		safe_cpy(req.OrderPrice, "17.560");
		//safe_cpy(req.FilledNumber, "0");
		safe_cpy(req.ModifyQty, "1000");
		safe_cpy(req.ModifyPrice, "17.580");
		//safe_cpy(req.TradeType, "1");
		safe_cpy(req.OrderType, STOCK_LIMIT_ORDER);
		safe_cpy(req.TriggerPrice, "0.000");

		if (!m_pStockApi->ReqOrderModify(&req, 0)) {
			COUTTIME << req.ErrorDescription << endl;
		}
	}
	void ReqOrderCancel()
	{
		if (m_systemNo.size() == 0 || m_orderNo.size() == 0) {
			COUTTIME << "ϵͳ�ţ������Ų���Ϊ��" << endl;
			return;
		}

		auto find = m_mapAccounts.find("HKD");
		if (find == m_mapAccounts.end())
			return;

		CStockReqOrderCancelField req = {};

		string localID = BuildLocalID(1);

		safe_cpy(req.UserId, m_appConfig.userId.c_str());
		safe_cpy(req.LocalNo, localID.c_str());
		safe_cpy(req.AccountNo, find->second.AccountNo);
		//safe_cpy(req.TradePwd, find->second.TradePwd);
		safe_cpy(req.SystemNo, m_systemNo.c_str());
		safe_cpy(req.OrderNo, m_orderNo.c_str());
		safe_cpy(req.ExchangeCode, "HKEX");//KRX
		safe_cpy(req.ContractCode, "00004.HK");//020560.KR
		safe_cpy(req.BidAskFlag, STOCK_BID);
		safe_cpy(req.OrderQty, "1000");
		//safe_cpy(req.FilledNumber, "0");

		if (!m_pStockApi->ReqOrderCancel(&req, 0)) {
			COUTTIME << req.ErrorDescription << endl;
		}
	}
	void ReqQryInstrument()
	{
		m_iQryPage = 0;
		QryInstrument(m_iQryPage);
	}
	void ReqChangePassword()
	{
		CStockReqPasswordUpdateField req = {};

		safe_cpy(req.UserId, m_appConfig.userId.c_str());
		safe_cpy(req.OldPassword, "888888");
		safe_cpy(req.NewPassword, "888888");

		if (!m_pStockApi->ReqPasswordUpdate(&req, 0)) {
			COUTTIME << req.ErrorDescription << endl;
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
	virtual void OnRtnTrade(CStockRtnTradeField *pRtnTrade, CStockRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		COUTTIME << "OnRtnTrade():UserId= " << pRtnTrade->UserId <<
			", OrderNo= " << pRtnTrade->OrderNo <<
			", FilledPrice= " << pRtnTrade->FilledPrice << endl;
		if (bIsLast) { COUTTIME << "-----------Over------------" << endl; }
	}
	virtual void OnRtnOrder(CStockRtnOrderField *pRtnOrder, CStockRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		COUTTIME << "OnRtnOrder(): ExchangeNo= " << pRtnOrder->ExchangeNo <<
			", OrderNo= " << pRtnOrder->OrderNo <<
			", FilledNumber= " << pRtnOrder->FilledNumber <<
			", FilledAdvPrice= " << pRtnOrder->FilledAdvPrice << endl;
		if (bIsLast) { COUTTIME << "-----------Over------------" << endl; }
	}
	virtual void OnRtnCapital(CStockRtnCapitalField *pRtnCapital, CStockRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		COUTTIME << "OnRtnCapital(): AccountNo= " << pRtnCapital->AccountNo <<
			", OrderNo= " << pRtnCapital->OrderNo << endl;
		if (bIsLast) { COUTTIME << "-----------Over------------" << endl; }
	}
	virtual void OnRtnPosition(CStockRtnPositionField *pRtnPosition, CStockRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		COUTTIME << "OnRtnPosition(): ClientNo= " << pRtnPosition->ClientNo <<
			", ExchangeCode= " << pRtnPosition->ExchangeCode << endl;
		if (bIsLast) { COUTTIME << "-----------Over------------" << endl; }
	}

	// ��ͨ����
public:
	virtual void OnRspNeedVerify(bool bFirstLogin, bool bHasSetQA)
	{
		m_bIsLogin = true;

		if (bFirstLogin) {
			COUTTIME << "���ǵ�һ�ε�¼����Ҫ���ڽ�����֤" << endl;
			ReqSetVerifyQA();
		}

		if (bHasSetQA) {
			COUTTIME << "�Ѿ����ù�����" << endl;
		}
	}
	virtual void OnRspUserLogin(CStockRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		if (pRspInfo->ErrorID) {
			COUTTIME << "��¼������ʧ��." << endl;
			COUTTIME << "ErrorID = " << pRspInfo->ErrorID << endl;
			COUTTIME << "ErrorMsg = " << pRspInfo->ErrorMsg << endl;
			m_bIsLogin = false;
		}
		else {
			COUTTIME << "��¼�������ɹ�." << endl;
			COUTTIME << "�ʽ��˺�: ";
			m_bIsLogin = true;
		}
	}
	virtual void OnRspUserLogout(CStockRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		COUTTIME << "ErrorID = " << pRspInfo->ErrorID << endl;
		COUTTIME << "ErrorMsg = " << pRspInfo->ErrorMsg << endl;
		m_bIsLogin = false;
	}
	virtual void OnRspVerifyCode(CStockRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		COUTTIME << "ErrorID = " << pRspInfo->ErrorID << endl;
		COUTTIME << "ErrorMsg = " << pRspInfo->ErrorMsg << endl;
	}
	virtual void OnRspSafeVerify(CStockRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		COUTTIME << "ErrorID = " << pRspInfo->ErrorID << endl;
		COUTTIME << "ErrorMsg = " << pRspInfo->ErrorMsg << endl;
	}
	virtual void OnRspSetVerifyQA(CStockRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		ReqSafeVerify();
		COUTTIME << "ErrorID = " << pRspInfo->ErrorID << endl;
		COUTTIME << "ErrorMsg = " << pRspInfo->ErrorMsg << endl;
	}
	virtual void OnRspAccount(CStockRspAccountField *pRspAccount, CStockRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		if (pRspInfo->ErrorID) {
			COUTTIME << "OnRspAccount (): ErrorID = " << pRspInfo->ErrorID <<
			 ",ErrorMsg = " << pRspInfo->ErrorMsg << endl;
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
	virtual void OnRspQuestion(CStockRspQuestionField *pRspQuestion, CStockRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		COUTTIME << "QuestionId=" << pRspQuestion->QuestionId <<
			", QuestionCN= " << pRspQuestion->QuestionCN <<
			", QuestionEN= " << pRspQuestion->QuestionEN << endl;
	}
	virtual void OnRspOrderInsert(CStockRspOrderInsertField *pRspOrderInsert, CStockRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		COUTTIME << "OnRspOrderInsert(): ErrorID = " << pRspInfo->ErrorID << 
		",ErrorMsg = " << pRspInfo->ErrorMsg << endl;

		if (pRspInfo->ErrorID) {
			m_systemNo = "";
			m_orderNo = "";
		}
		else {
			m_systemNo = pRspOrderInsert->SystemNo;
			m_orderNo = pRspOrderInsert->OrderNo;
		}
	}
	virtual void OnRspOrderModify(CStockRspOrderModifyField *pRspOrderModify, CStockRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		COUTTIME << "OnRspOrderModify(): ErrorID = " << pRspInfo->ErrorID <<
		 ",ErrorMsg = " << pRspInfo->ErrorMsg << 
		 ",UserId = " << pRspOrderModify->UserId << endl;
	}
	virtual void OnRspOrderCancel(CStockRspOrderCancelField *pRspOrderCancel, CStockRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		COUTTIME << "OnRspOrderCancel(): ErrorID = " << pRspInfo->ErrorID << 
		",ErrorMsg = " << pRspInfo->ErrorMsg <<
		",SystemNo = " << pRspOrderCancel->SystemNo << endl;
	}
	virtual void OnRspPasswordUpdate(CStockRspPasswordUpdateField *pRspPasswordUpdate, CStockRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		COUTTIME << "ErrorID = " << pRspInfo->ErrorID << endl;
		COUTTIME << "ErrorMsg = " << pRspInfo->ErrorMsg << endl;
		COUTTIME << "UserId = " << pRspPasswordUpdate->UserId << endl;
	}

	// ��ѯ����
public:
	virtual void OnRspQryTick(CStockRspTickField *pRspTick, CStockRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		COUTTIME << "UpperTickCode= " << pRspTick->UpperTickCode <<
			", DotNum= " << pRspTick->DotNum << endl;
		if (bIsLast) { COUTTIME << "-----------Over------------" << endl; }
	}
	virtual void OnRspQryOrder(CStockRspOrderField *pRspOrder, CStockRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		COUTTIME << "UserId= " << pRspOrder->UserId <<
			", OrderNo= " << pRspOrder->OrderNo <<
			", OrderPrice=" << pRspOrder->OrderPrice << endl;
		if (bIsLast) { COUTTIME << "-----------Over------------" << endl; }
	}
	virtual void OnRspQryTrade(CStockRspTradeField *pRspTrade, CStockRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		COUTTIME << "FilledNo= " << pRspTrade->FilledNo <<
			", FilledPrice= " << pRspTrade->FilledPrice << endl;
		
		if (bIsLast) { COUTTIME << "-----------Over------------" << endl; }
	}
	virtual void OnRspQryVersion(CStockRspVersionField *pRspVersion, CStockRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		COUTTIME << "Version= " << pRspVersion->Version <<
			", MustUpdate= " << pRspVersion->MustUpdate << endl;
	}
	virtual void OnRspQryCapital(CStockRspCapitalField *pRspCapital, CStockRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		COUTTIME << "UserId= " << pRspCapital->UserId <<
			", TodayInitialBalance= " << pRspCapital->TodayInitialBalance <<
			", CanCashOutMoneyAmount= " << pRspCapital->CanCashOutMoneyAmount <<",TodayTradableFund="<< pRspCapital->TodayTradableFund <<
			",Currency = " <<pRspCapital->CurrencyNo <<endl;
		if (bIsLast) { COUTTIME << "-----------Over------------" << endl; }
	}
	virtual void OnRspQryPosition(CStockRspPositionField *pRspPosition, CStockRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		COUTTIME << "ClientNo= " << pRspPosition->ClientNo <<
			", ExchangeCode= " << pRspPosition->ExchangeCode <<
			", PosCostPrice= " << pRspPosition->PosCostPrice <<
			", FrosenShares= " << pRspPosition->FrosenShares <<
			", CanSellShares= " << pRspPosition->CanSellShares << endl;
		if (bIsLast) { COUTTIME << "-----------Over------------" << endl; }
	}
	virtual void OnRspQryExchange(CStockRspExchangeField *pRspExchange, CStockRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		COUTTIME << "ExchangeNo= " << pRspExchange->ExchangeNo <<
			", ExchangeName= " << pRspExchange->ExchangeName << endl;
		if (bIsLast) { COUTTIME << "-----------Over------------" << endl; }
	}
	virtual void OnRspQryCurrency(CStockRspCurrencyField *pRspCurrency, CStockRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		COUTTIME << "CurrencyNo= " << pRspCurrency->CurrencyNo << ", "
			"CurrencyName= " << pRspCurrency->CurrencyName << endl;
		if (bIsLast) { COUTTIME << "-----------Over------------" << endl; }
	}
	virtual void OnRspQryInstrument(CStockRspInstrumentField *pRspInstrument, CStockRspInfoField *pRspInfo, int iRequestID, bool bIsLast)
	{
		if (pRspInfo->ErrorID) {
			COUTTIME << "ErrorID = " << pRspInfo->ErrorID << endl;
			COUTTIME << "-----------Over------------" << endl;
		}
		else {
			int static count=1;
			COUTTIME <<count++<<": "<< "ExchangeName= " << pRspInstrument->ExchangeNo
				<< ", CommodityNo= " << pRspInstrument->CommodityNo << endl;

			if (bIsLast) {
				m_iQryPage++;
				QryInstrument(m_iQryPage);
			}
		}
	}
};

