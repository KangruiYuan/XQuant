/////////////////////////////////////////////////////////////////////////
/// DriectAccess Trade Engine
/// Copyright (C) Shanghai DirectAccess Technology Co., Ltd.
/// Last Modify 2019/3/18
/// Define Market Struct
/// Author (c) Wang Jian Quan (Franklin)
/////////////////////////////////////////////////////////////////////////

#pragma once

#include "DADataType.h"

// ��������
struct CMarketRspInfoField
{
	TDAIntType			ErrorID;						// ������
	TDAStringType		ErrorMsg;						// ��������
};

// �û���¼����
struct CMarketReqUserLoginField
{
	TDAStringType		UserId;							// �û���ʶ
	TDAStringType		UserPwd;						// �û�����
	TDAStringType		UserType;						// �û�����
	TDAStringType		MacAddress;						// MAC��ַ
	TDAStringType		ComputerName;					// �������
	TDAStringType		SoftwareName;					// �������
	TDAStringType		SoftwareVersion;				// ����汾��
	TDAStringType		AuthorCode;						// ��Ȩ��
	TDAStringType		ErrorDescription;				// ������Ϣ
};

// �û���¼����
struct CMarketRspUserLoginField
{
	TDAStringType		UserName;						// �û���    
	TDAStringType		UserPwd;						// ��¼����             
	TDAStringType		UserType;						// �û�����             
};

// �û��ǳ�����
struct CMarketReqUserLogoutField
{
	TDAStringType		BrokerID;						// ���͹�˾����
	TDAStringType		UserId;							// �û�����
	TDAStringType		ErrorDescription;				// ������Ϣ
};

// ������������
struct CMarketReqMarketDataField
{
	TDACharType			MarketType;						// ��������
	TDACharType			SubscMode;						// ��������
	TDAIntType			MarketCount;					// �����������	
	TDAStringType		MarketTrcode[MAX_SUB_COUNT];	// ��������ĺ�Լ
	TDAStringType		ErrorDescription;				// ������Ϣ
};

// ������������
struct CMarketRspMarketDataField
{
	TDAStringType		ExchangeCode;					// ����������
	TDAStringType		TreatyCode;						// ��Լ����
	TDAStringType		BuyPrice;   					// ���
	TDAStringType		BuyNumber;   					// ����
	TDAStringType		SalePrice;   					// ����
	TDAStringType		SaleNumber;   					// ����
	TDAStringType		CurrPrice;   					// ���¼�
	TDAStringType		CurrNumber;   					// ������
	TDAStringType		High;   						// ������߼�
	TDAStringType		Low;   							// ������ͼ�
	TDAStringType		Open;   						// ���̼�
	TDAStringType		IntradaySettlePrice;   			// �������н����(��Ʊ�����̼�)
	TDAStringType		Close;   						// ��������
	TDAStringType		Time;   						// ����ʱ��
	TDAStringType		FilledNum;   					// �ɽ���
	TDAStringType		HoldNum;   						// �ֲ���
	TDAStringType		BuyPrice2; 						// ���2
	TDAStringType		BuyPrice3;  					// ���3
	TDAStringType		BuyPrice4;  					// ���4
	TDAStringType		BuyPrice5;  					// ���5
	TDAStringType		BuyNumber2;  					// ����2
	TDAStringType		BuyNumber3;  					// ����3
	TDAStringType		BuyNumber4;  					// ����4
	TDAStringType		BuyNumber5;  					// ����5
	TDAStringType		SalePrice2;  					// ����2
	TDAStringType		SalePrice3;  					// ����3
	TDAStringType		SalePrice4;  					// ����4
	TDAStringType		SalePrice5;  					// ����5
	TDAStringType		SaleNumber2; 					// ����2
	TDAStringType		SaleNumber3;  					// ����3
	TDAStringType		SaleNumber4;  					// ����4
	TDAStringType		SaleNumber5;  					// ����5
	TDAStringType		HideBuyPrice; 					// �������
	TDAStringType		HideBuyNumber; 					// ��������
	TDAStringType		HideSalePrice; 					// ��������
	TDAStringType		HideSaleNumber;					// ��������
	TDAStringType		LimitDownPrice; 				// ��ͣ��
	TDAStringType		LimitUpPrice;  					// ��ͣ��
	TDAStringType		TradeDay;   					// ������
	TDAStringType		BuyPrice6;						// ���6
	TDAStringType		BuyPrice7;						// ���7
	TDAStringType		BuyPrice8;						// ���8
	TDAStringType		BuyPrice9;						// ���9
	TDAStringType		BuyPrice10;						// ���10
	TDAStringType		BuyNumber6;						// ����6
	TDAStringType		BuyNumber7;						// ����7
	TDAStringType		BuyNumber8;						// ����8
	TDAStringType		BuyNumber9;						// ����9
	TDAStringType		BuyNumber10;					// ����10
	TDAStringType		SalePrice6;						// ����6
	TDAStringType		SalePrice7;						// ����7
	TDAStringType		SalePrice8;						// ����8
	TDAStringType		SalePrice9;						// ����9
	TDAStringType		SalePrice10;					// ����10
	TDAStringType		SaleNumber6;					// ����6
	TDAStringType		SaleNumber7;					// ����7
	TDAStringType		SaleNumber8;					// ����8
	TDAStringType		SaleNumber9;					// ����9
	TDAStringType		SaleNumber10;					// ����10
	TDAStringType		TradeFlag;						// �۽�����Ʊ���飺�ɽ�����
	TDAStringType		DataTimestamp;					// ����������ʱ���
	TDAStringType		DataSourceId;					// ������Դ
	TDAStringType		CanSellVol;						// �����չ��������������ã�
	TDAStringType		QuoteType;  					// ��������
	TDAStringType		AggressorSide;  				// �������������
	TDAStringType		PreSettlementPrice;  			// ����㣨��Ʊ�������̼ۣ�
};

// ���ľ���������
struct CMarketReqBrokerDataField
{
	TDAStringType		ContCode;						// ��Լ����
	TDAStringType		ErrorDescription;				// ������Ϣ
};

// ���ؾ���������
struct CMarketRspBrokerDataField
{
	TDABrokerType		BrokerData;						// ����������
};

// ���ͽ����սṹ��
struct CMarketRspTradeDateField
{
	TDAStringType		TradeDate;						// ��������
	TDAStringType		TradeProduct;					// ���ײ�Ʒ
};
