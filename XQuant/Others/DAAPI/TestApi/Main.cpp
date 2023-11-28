// Main.cpp : 定义控制台应用程序的入口点。
//

#include "stdafx.h"
#include "LockBool.h"
#include "AppHelper.h"
#include "AppConfig.h"
#include "MyStock.h"
#include "MyFuture.h"
#include "MyMarket.h"

#define WRONG_COMMAND		"不能识别的命令!"	
#define CONNECTING_TEXT		"正在连接并登陆服务器...."
#define CONT_LOGIN_TEXT		"已经连接并登陆上了服务器."

#define IF_LOGIN_CALL(cls,fun,help)						\
if ( cls.IsCreate() ) {									\
	cout << help << endl;								\
	cls.fun();											\
}														\
else {													\
	cout << "请先输入命令 'A' 连接并登陆" << endl;		\
}														\

void ShowStockHelp()
{
	cout << "" << endl;
	cout << "------ 测试股票接口 ------" << endl;
	cprintf(ColorValue::LightGreen, "  A");
	cout << " 连接并登录" << endl;
	cout << "  B 查询合约" << endl;
	cout << "  C 查询交易所" << endl;
	cout << "  D 查询资金" << endl;
	cout << "  E 查询持仓" << endl;
	cout << "  F 查询成交" << endl;
	cout << "  G 查询跳点" << endl;
	cout << "  H 查询币种" << endl;
	cout << "  I 查询订单" << endl;
	cout << "  J 下单" << endl;
	cout << "  K 改单" << endl;
	cout << "  L 撤单" << endl;
	cout << "  ? 帮助" << endl;
	cout << "  ......" << endl;
	cprintf(ColorValue::LightRed, "  *");
	cout << " 返回上一级" << endl;
	cout << "--------------------------" << endl;
	cout << "请输入命令:";
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
			cout << "返回上一级...." << endl;
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
			IF_LOGIN_CALL(myStock, ReqQryInstrument, "查询合约");
		}
		else if (cmd == "C") {
			IF_LOGIN_CALL(myStock, ReqQryExchange, "查询交易所");
		}
		else if (cmd == "D") {
			IF_LOGIN_CALL(myStock, ReqQryCapital, "查询资金");
		}
		else if (cmd == "E") {
			IF_LOGIN_CALL(myStock, ReqQryPosition, "查询持仓");
		}
		else if (cmd == "F") {
			IF_LOGIN_CALL(myStock, ReqQryTrade, "查询成交");
		}
		else if (cmd == "G") {
			IF_LOGIN_CALL(myStock, ReqQryTick, "查询跳点");
		}
		else if (cmd == "H") {
			IF_LOGIN_CALL(myStock, ReqQryCurrency, "查询货币");
		}
		else if (cmd == "I") {
			IF_LOGIN_CALL(myStock, ReqQryOrder, "查询订单");
		}
		else if (cmd == "J") {
			IF_LOGIN_CALL(myStock, ReqOrderInsert, "下单");
		}
		else if (cmd == "K") {
			IF_LOGIN_CALL(myStock, ReqOrderModify, "改单");
		}
		else if (cmd == "L") {
			IF_LOGIN_CALL(myStock, ReqOrderCancel, "撤单");
		}
		else if (cmd == "M") {
			IF_LOGIN_CALL(myStock, ReqQryVersion, "查询版本");
		}
		else if (cmd == "N") {
			IF_LOGIN_CALL(myStock, ReqGetQuestion, "查询问题");
		}
		else if (cmd == "O") {
			IF_LOGIN_CALL(myStock, ReqVerifyCode, "校验密码");
		}
		else if (cmd == "P") {
			IF_LOGIN_CALL(myStock, ReqSafeVerify, "安全验证");
		}
		else if (cmd == "Q") {
			IF_LOGIN_CALL(myStock, ReqSetVerifyQA, "设置验证问题答案");
		}
		else if (cmd == "R") {
			IF_LOGIN_CALL(myStock, ReqChangePassword, "修改密码");
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
	cout << "------ 测试期货接口 ------" << endl;
	cprintf(ColorValue::LightGreen, "  A");
	cout << "  连接并登录" << endl;
	cout << "  B 查询合约" << endl;
	cout << "  C 查询交易所" << endl;
	cout << "  D 查询资金" << endl;
	cout << "  E 查询持仓" << endl;
	cout << "  F 查询成交" << endl;
	cout << "  G 修改密码" << endl;
	cout << "  H 查询币种" << endl;
	cout << "  I 查询订单" << endl;
	cout << "  J 下单" << endl;
	cout << "  K 改单" << endl;
	cout << "  L 撤单" << endl;
	cout << "  ? 帮助" << endl;
	cout << "  ......" << endl;
	cprintf(ColorValue::LightRed, "  *");
	cout << " 返回上一级" << endl;
	cout << "--------------------------" << endl;
	cout << "请输入命令:";
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
			cout << "返回上一级...." << endl;
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
			IF_LOGIN_CALL(myFuture, ReqQryInstrument, "查询合约");
		}
		else if (cmd == "C") {
			IF_LOGIN_CALL(myFuture, ReqQryExchange, "查询交易所");
		}
		else if (cmd == "D") {
			IF_LOGIN_CALL(myFuture, ReqQryCapital, "查询资金");
		}
		else if (cmd == "E") {
			IF_LOGIN_CALL(myFuture, ReqQryPosition, "查询持仓");
		}
		else if (cmd == "F") {
			IF_LOGIN_CALL(myFuture, ReqQryTrade, "查询成交");
		}
		else if (cmd == "G") {
			IF_LOGIN_CALL(myFuture, ReqChangePassword, "修改密码");
		}
		else if (cmd == "H") {
			IF_LOGIN_CALL(myFuture, ReqQryCurrency, "查询货币");
		}
		else if (cmd == "I") {
			IF_LOGIN_CALL(myFuture, ReqQryOrder, "查询订单");
		}
		else if (cmd == "J") {
			IF_LOGIN_CALL(myFuture, ReqOrderInsert, "下单");
		}
		else if (cmd == "K") {
			IF_LOGIN_CALL(myFuture, ReqOrderModify, "改单");
		}
		else if (cmd == "L") {
			IF_LOGIN_CALL(myFuture, ReqOrderCancel, "撤单");
		}
		else if (cmd == "M") {
			IF_LOGIN_CALL(myFuture, ReqQryExchangeTime, "查询交易所时间");
		}
		else if (cmd == "N") {
			IF_LOGIN_CALL(myFuture, ReqQryCommodityTime, "查询商品时间");
		}
		else if (cmd == "O") {
			IF_LOGIN_CALL(myFuture, ReqQryVersion, "查询版本");
		}
		else if (cmd == "P") {
			IF_LOGIN_CALL(myFuture, ReqQryStrategy, "查询策略");
		}
		else if (cmd == "Q") {
			IF_LOGIN_CALL(myFuture, ReqQryStrategyDetail, "查询策略细节");
		}
		else if (cmd == "R") {
			IF_LOGIN_CALL(myFuture, ReqGetQuestion, "查询问题");
		}
		else if (cmd == "S") {
			IF_LOGIN_CALL(myFuture, ReqVerifyCode, "校验密码");
		}
		else if (cmd == "T") {
			IF_LOGIN_CALL(myFuture, ReqSafeVerify, "安全验证");
		}
		else if (cmd == "U") {
			IF_LOGIN_CALL(myFuture, ReqSetVerifyQA, "设置验证问题答案");
		}
		else if (cmd == "V") {
			IF_LOGIN_CALL(myFuture, ReqQryTotalPosition, "查询持仓合计");
		}
		else if (cmd == "W") {
			IF_LOGIN_CALL(myFuture, ReqQryCommodity, "查询商品");
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
	cout << "------ 测试行情接口 ------" << endl;
	cprintf(ColorValue::LightGreen, "  A");
	cout << "  连接并登录" << endl;
	cout << "  B 订阅股票行情" << endl;
	cout << "  C 退订股票行情" << endl;
	cout << "  D 订阅期货行情" << endl;
	cout << "  E 退订期货行情" << endl;
	cout << "  F 订阅股票经济商" << endl;
	cout << "  G 退订所有行情" << endl;
	cout << "  H 按交易所订阅期货行情" << endl;
	cout << "  ? 帮助" << endl;
	cprintf(ColorValue::LightRed, "  *");
	cout << " 返回上级" << endl;
	cout << "--------------------------" << endl;
	cout << "请输入命令:";
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
			cout << "返回上一级...." << endl;
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
			IF_LOGIN_CALL(myMarket, SubscStockMarket, "订阅股票行情");
		}
		else if (cmd == "C") {
			IF_LOGIN_CALL(myMarket, UnsubscStockMarket, "退订股票行情");
		}
		else if (cmd == "D") {
			IF_LOGIN_CALL(myMarket, SubscFutureMarket, "订阅期货行情");
		}
		else if (cmd == "E") {
			IF_LOGIN_CALL(myMarket, UnsubscFutureMarket, "退订期货行情");
		}
		else if (cmd == "F") {
			IF_LOGIN_CALL(myMarket, SubscStockBroker, "订阅股票经济商");
		}
		else if (cmd == "G") {
			IF_LOGIN_CALL(myMarket, UnsubscAllMarket, "退订所有行情");
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
	cout << "※※※※※※※  直达接口测试程序  ※※※※※※※" << endl;
	cout << "" << endl;
	cout << "  S 测试股票功能...." << endl;
	cout << "  F 测试期货功能...." << endl;
	cout << "  M 测试行情功能...." << endl;
	cprintf(ColorValue::LightRed, "  X");
	cout << " 退出测试程序" << endl;
	cout << "  ? 帮助" << endl;
	cout << "------------------------------------------" << endl;
	cout << "请输入命令:";
}

int main()
{
#ifdef _WIN32
	SetConsoleTitle(L"直达接口测试程序");
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

	cout << "安全退出程序." << endl;
}

