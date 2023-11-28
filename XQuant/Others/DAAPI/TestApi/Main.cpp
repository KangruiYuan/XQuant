// Main.cpp : �������̨Ӧ�ó������ڵ㡣
//

#include "stdafx.h"
#include "LockBool.h"
#include "AppHelper.h"
#include "AppConfig.h"
#include "MyStock.h"
#include "MyFuture.h"
#include "MyMarket.h"

#define WRONG_COMMAND		"����ʶ�������!"	
#define CONNECTING_TEXT		"�������Ӳ���½������...."
#define CONT_LOGIN_TEXT		"�Ѿ����Ӳ���½���˷�����."

#define IF_LOGIN_CALL(cls,fun,help)						\
if ( cls.IsCreate() ) {									\
	cout << help << endl;								\
	cls.fun();											\
}														\
else {													\
	cout << "������������ 'A' ���Ӳ���½" << endl;		\
}														\

void ShowStockHelp()
{
	cout << "" << endl;
	cout << "------ ���Թ�Ʊ�ӿ� ------" << endl;
	cprintf(ColorValue::LightGreen, "  A");
	cout << " ���Ӳ���¼" << endl;
	cout << "  B ��ѯ��Լ" << endl;
	cout << "  C ��ѯ������" << endl;
	cout << "  D ��ѯ�ʽ�" << endl;
	cout << "  E ��ѯ�ֲ�" << endl;
	cout << "  F ��ѯ�ɽ�" << endl;
	cout << "  G ��ѯ����" << endl;
	cout << "  H ��ѯ����" << endl;
	cout << "  I ��ѯ����" << endl;
	cout << "  J �µ�" << endl;
	cout << "  K �ĵ�" << endl;
	cout << "  L ����" << endl;
	cout << "  ? ����" << endl;
	cout << "  ......" << endl;
	cprintf(ColorValue::LightRed, "  *");
	cout << " ������һ��" << endl;
	cout << "--------------------------" << endl;
	cout << "����������:";
}

LONG TestStock()
{
	ShowStockHelp();

	string cmd;
	CMyStock myStock;
	while (true) {
		cin >> cmd;
		std::transform(cmd.begin(), cmd.end(), cmd.begin(), ::toupper);

		if (cmd == "*") {
			cout << "������һ��...." << endl;
			break;
		}
		else if (cmd == "?") {
			ShowStockHelp();
		}
		else if (cmd == "A") {
			if (myStock.IsCreate()) {
				cout << (myStock.IsLogin() ? CONT_LOGIN_TEXT : CONNECTING_TEXT) << endl;
			}
			else {
				myStock.Create();
			}
		}
		else if (cmd == "B") {
			IF_LOGIN_CALL(myStock, ReqQryInstrument, "��ѯ��Լ");
		}
		else if (cmd == "C") {
			IF_LOGIN_CALL(myStock, ReqQryExchange, "��ѯ������");
		}
		else if (cmd == "D") {
			IF_LOGIN_CALL(myStock, ReqQryCapital, "��ѯ�ʽ�");
		}
		else if (cmd == "E") {
			IF_LOGIN_CALL(myStock, ReqQryPosition, "��ѯ�ֲ�");
		}
		else if (cmd == "F") {
			IF_LOGIN_CALL(myStock, ReqQryTrade, "��ѯ�ɽ�");
		}
		else if (cmd == "G") {
			IF_LOGIN_CALL(myStock, ReqQryTick, "��ѯ����");
		}
		else if (cmd == "H") {
			IF_LOGIN_CALL(myStock, ReqQryCurrency, "��ѯ����");
		}
		else if (cmd == "I") {
			IF_LOGIN_CALL(myStock, ReqQryOrder, "��ѯ����");
		}
		else if (cmd == "J") {
			IF_LOGIN_CALL(myStock, ReqOrderInsert, "�µ�");
		}
		else if (cmd == "K") {
			IF_LOGIN_CALL(myStock, ReqOrderModify, "�ĵ�");
		}
		else if (cmd == "L") {
			IF_LOGIN_CALL(myStock, ReqOrderCancel, "����");
		}
		else if (cmd == "M") {
			IF_LOGIN_CALL(myStock, ReqQryVersion, "��ѯ�汾");
		}
		else if (cmd == "N") {
			IF_LOGIN_CALL(myStock, ReqGetQuestion, "��ѯ����");
		}
		else if (cmd == "O") {
			IF_LOGIN_CALL(myStock, ReqVerifyCode, "У������");
		}
		else if (cmd == "P") {
			IF_LOGIN_CALL(myStock, ReqSafeVerify, "��ȫ��֤");
		}
		else if (cmd == "Q") {
			IF_LOGIN_CALL(myStock, ReqSetVerifyQA, "������֤�����");
		}
		else if (cmd == "R") {
			IF_LOGIN_CALL(myStock, ReqChangePassword, "�޸�����");
		}
		else {
			cout << WRONG_COMMAND << endl;
		}
	}
	myStock.Destroy();
	return 0;
}

void ShowFutureHelp()
{
	cout << "" << endl;
	cout << "------ �����ڻ��ӿ� ------" << endl;
	cprintf(ColorValue::LightGreen, "  A");
	cout << "  ���Ӳ���¼" << endl;
	cout << "  B ��ѯ��Լ" << endl;
	cout << "  C ��ѯ������" << endl;
	cout << "  D ��ѯ�ʽ�" << endl;
	cout << "  E ��ѯ�ֲ�" << endl;
	cout << "  F ��ѯ�ɽ�" << endl;
	cout << "  G �޸�����" << endl;
	cout << "  H ��ѯ����" << endl;
	cout << "  I ��ѯ����" << endl;
	cout << "  J �µ�" << endl;
	cout << "  K �ĵ�" << endl;
	cout << "  L ����" << endl;
	cout << "  ? ����" << endl;
	cout << "  ......" << endl;
	cprintf(ColorValue::LightRed, "  *");
	cout << " ������һ��" << endl;
	cout << "--------------------------" << endl;
	cout << "����������:";
}

LONG TestFuture()
{
	ShowFutureHelp();

	string cmd;
	CMyFuture myFuture;
	while (true) {
		cin >> cmd;
		std::transform(cmd.begin(), cmd.end(), cmd.begin(), ::toupper);

		if (cmd == "*") {
			cout << "������һ��...." << endl;
			break;
		}
		else if (cmd == "?") {
			ShowFutureHelp();
		}
		else if (cmd == "A") {
			if (myFuture.IsCreate()) {
				cout << (myFuture.IsLogin() ? CONT_LOGIN_TEXT : CONNECTING_TEXT) << endl;
			}
			else {
				myFuture.Create();
			}
		}
		else if (cmd == "B") {
			IF_LOGIN_CALL(myFuture, ReqQryInstrument, "��ѯ��Լ");
		}
		else if (cmd == "C") {
			IF_LOGIN_CALL(myFuture, ReqQryExchange, "��ѯ������");
		}
		else if (cmd == "D") {
			IF_LOGIN_CALL(myFuture, ReqQryCapital, "��ѯ�ʽ�");
		}
		else if (cmd == "E") {
			IF_LOGIN_CALL(myFuture, ReqQryPosition, "��ѯ�ֲ�");
		}
		else if (cmd == "F") {
			IF_LOGIN_CALL(myFuture, ReqQryTrade, "��ѯ�ɽ�");
		}
		else if (cmd == "G") {
			IF_LOGIN_CALL(myFuture, ReqChangePassword, "�޸�����");
		}
		else if (cmd == "H") {
			IF_LOGIN_CALL(myFuture, ReqQryCurrency, "��ѯ����");
		}
		else if (cmd == "I") {
			IF_LOGIN_CALL(myFuture, ReqQryOrder, "��ѯ����");
		}
		else if (cmd == "J") {
			IF_LOGIN_CALL(myFuture, ReqOrderInsert, "�µ�");
		}
		else if (cmd == "K") {
			IF_LOGIN_CALL(myFuture, ReqOrderModify, "�ĵ�");
		}
		else if (cmd == "L") {
			IF_LOGIN_CALL(myFuture, ReqOrderCancel, "����");
		}
		else if (cmd == "M") {
			IF_LOGIN_CALL(myFuture, ReqQryExchangeTime, "��ѯ������ʱ��");
		}
		else if (cmd == "N") {
			IF_LOGIN_CALL(myFuture, ReqQryCommodityTime, "��ѯ��Ʒʱ��");
		}
		else if (cmd == "O") {
			IF_LOGIN_CALL(myFuture, ReqQryVersion, "��ѯ�汾");
		}
		else if (cmd == "P") {
			IF_LOGIN_CALL(myFuture, ReqQryStrategy, "��ѯ����");
		}
		else if (cmd == "Q") {
			IF_LOGIN_CALL(myFuture, ReqQryStrategyDetail, "��ѯ����ϸ��");
		}
		else if (cmd == "R") {
			IF_LOGIN_CALL(myFuture, ReqGetQuestion, "��ѯ����");
		}
		else if (cmd == "S") {
			IF_LOGIN_CALL(myFuture, ReqVerifyCode, "У������");
		}
		else if (cmd == "T") {
			IF_LOGIN_CALL(myFuture, ReqSafeVerify, "��ȫ��֤");
		}
		else if (cmd == "U") {
			IF_LOGIN_CALL(myFuture, ReqSetVerifyQA, "������֤�����");
		}
		else if (cmd == "V") {
			IF_LOGIN_CALL(myFuture, ReqQryTotalPosition, "��ѯ�ֲֺϼ�");
		}
		else if (cmd == "W") {
			IF_LOGIN_CALL(myFuture, ReqQryCommodity, "��ѯ��Ʒ");
		}
		else {
			cout << WRONG_COMMAND << endl;
		}
	}
	myFuture.Destroy();
	return 0;
}

void ShowMarketHelp()
{
	cout << "" << endl;
	cout << "------ ��������ӿ� ------" << endl;
	cprintf(ColorValue::LightGreen, "  A");
	cout << "  ���Ӳ���¼" << endl;
	cout << "  B ���Ĺ�Ʊ����" << endl;
	cout << "  C �˶���Ʊ����" << endl;
	cout << "  D �����ڻ�����" << endl;
	cout << "  E �˶��ڻ�����" << endl;
	cout << "  F ���Ĺ�Ʊ������" << endl;
	cout << "  G �˶���������" << endl;
	cout << "  H �������������ڻ�����" << endl;
	cout << "  ? ����" << endl;
	cprintf(ColorValue::LightRed, "  *");
	cout << " �����ϼ�" << endl;
	cout << "--------------------------" << endl;
	cout << "����������:";
}

LONG TestMarket()
{
	ShowMarketHelp();

	string cmd;
	CMyMarket myMarket;
	while (true) {
		std::cin >> cmd;
		std::transform(cmd.begin(), cmd.end(), cmd.begin(), ::toupper);

		if (cmd == "*") {
			cout << "������һ��...." << endl;
			break;
		}
		else if (cmd == "?") {
			ShowMarketHelp();
		}
		else if (cmd == "A") {
			if (myMarket.IsCreate()) {
				cout << (myMarket.IsLogin() ? CONT_LOGIN_TEXT : CONNECTING_TEXT) << endl;
			}
			else {
				myMarket.Create();
			}
		}
		else if (cmd == "B") {
			IF_LOGIN_CALL(myMarket, SubscStockMarket, "���Ĺ�Ʊ����");
		}
		else if (cmd == "C") {
			IF_LOGIN_CALL(myMarket, UnsubscStockMarket, "�˶���Ʊ����");
		}
		else if (cmd == "D") {
			IF_LOGIN_CALL(myMarket, SubscFutureMarket, "�����ڻ�����");
		}
		else if (cmd == "E") {
			IF_LOGIN_CALL(myMarket, UnsubscFutureMarket, "�˶��ڻ�����");
		}
		else if (cmd == "F") {
			IF_LOGIN_CALL(myMarket, SubscStockBroker, "���Ĺ�Ʊ������");
		}
		else if (cmd == "G") {
			IF_LOGIN_CALL(myMarket, UnsubscAllMarket, "�˶���������");
		}
		else {
			cout << WRONG_COMMAND << endl;
		}
	}
	myMarket.Destroy();
	return 0;
}

void ShowRootHelp()
{
	cout << "" << endl;
	cout << "��������������  ֱ��ӿڲ��Գ���  ��������������" << endl;
	cout << "" << endl;
	cout << "  S ���Թ�Ʊ����...." << endl;
	cout << "  F �����ڻ�����...." << endl;
	cout << "  M �������鹦��...." << endl;
	cprintf(ColorValue::LightRed, "  X");
	cout << " �˳����Գ���" << endl;
	cout << "  ? ����" << endl;
	cout << "------------------------------------------" << endl;
	cout << "����������:";
}

int main()
{
#ifdef _WIN32
	SetConsoleTitle(L"ֱ��ӿڲ��Գ���");
	WSADATA wsaData = {};
	if (WSAStartup(MAKEWORD(2, 2), &wsaData) != NO_ERROR)
		return false;
#endif

	ShowRootHelp();

	string cmd;
	while (true) {
		cin >> cmd;
		std::transform(cmd.begin(), cmd.end(), cmd.begin(), ::toupper);
		if (cmd == "X") {
			break;
		}
		else if (cmd == "*") {
			ShowRootHelp();
		}
		else if (cmd == "?") {
			ShowRootHelp();
		}
		else if (cmd == "S") {
			TestStock();
			ShowRootHelp();
		}
		else if (cmd == "F") {
			TestFuture();
			ShowRootHelp();
		}
		else if (cmd == "M") {
			TestMarket();
			ShowRootHelp();
		}
		else {
			cout << WRONG_COMMAND << endl;
		}
	}

#ifdef _WIN32
	WSACleanup();
#endif

	cout << "��ȫ�˳�����." << endl;
}

