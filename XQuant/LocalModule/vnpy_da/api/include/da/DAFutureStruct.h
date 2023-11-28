/////////////////////////////////////////////////////////////////////////
/// DriectAccess Trade Engine
/// Copyright (C) Shanghai DirectAccess Technology Co., Ltd.
/// Last Modify 2019/3/18
/// Define Future Struct
/// Author (c) Wang Jian Quan (Franklin)
/////////////////////////////////////////////////////////////////////////

#pragma once

#include "DADataType.h"

// ��������
struct CFutureRspInfoField 
{
	TDAIntType			ErrorID;							// ������
	TDAStringType		ErrorMsg;							// ��������
};
// �û���¼����
struct CFutureReqUserLoginField
{
	TDAStringType		UserId;								// �û���ʶ
	TDAStringType		UserPwd;							// �û�����
	TDAStringType		UserType;							// �û�����
	TDAStringType		MacAddress;							// MAC��ַ
	TDAStringType		ComputerName;						// �������
	TDAStringType		SoftwareName;						// �������
	TDAStringType		SoftwareVersion;					// ����汾��
	TDAStringType		AuthorCode;							// ��Ȩ��
	TDAStringType		ErrorDescription;					// ������Ϣ
};
// �û���¼����
struct CFutureRspAccountField
{
	TDAStringType		UserId;								// �û���ʶ
	TDAStringType		UserName;							// �û���    
	TDAStringType		UserType;							// �û�����             
	TDAStringType		LoginPwd;							// ��¼����             
	TDAStringType		AccountNo;							// �ʽ��˺�              
	TDAStringType		TradePwd;							// ��������             
	TDAStringType		IsSimulation;						// �Ƿ�ģ���û�              
	TDAStringType		FrontendIp;							// ǰ�û�IP��ַ              
	TDAStringType		FrontendPort;						// ǰ�û��˿ں�            
	TDAStringType		CurrencyNo;							// �ʻ�����           
	TDAStringType		UserState;							// �û�״̬ C���� U���� D����         
	TDAStringType		SelAll;								// �Ƿ����������Ȩ             
	TDAStringType		Strategy;							// �Ƿ�������Զ�����Ե�              
	TDAStringType		Inner;								// �Ƿ�����¹��ڵ�             
	TDAStringType		YingSun;							// �Ƿ����ʹ��ֹ��ֹӯ������������          
	TDAStringType		ChaoDan;							// �Ƿ����ʹ�ó����ֹ���             
	TDAStringType		Option;								// �Ƿ���Խ�����Ȩ��0             
	TDAStringType		CmeMarket;							// �Ƿ���Ի�ȡCME���飺0              
	TDAStringType		CmeCOMEXMarket;						// �Ƿ���Ի�ȡCME_COMEX����               
	TDAStringType		CmeNYMEXMarket;						// �Ƿ���Ի�ȡCME_NYMEX����               
	TDAStringType		CmeCBTMarket;						// �Ƿ���Ի�ȡCME_CBT����               
	TDAStringType		IceUSMarket;						// �Ƿ���Ի�ȡICE US����              
	TDAStringType		IceECMarket;						// �Ƿ���Ի�ȡICE EC����             
	TDAStringType		IceEFMarket;						// �Ƿ���Ի�ȡICE EF����             
	TDAStringType		CanTradeStockHK;					// �Ƿ���Խ��׸۹�             
	TDAStringType		CanTradeStockAM;					// �Ƿ���Խ�������            
	TDAStringType		MultiLogin;							// �Ƿ���Զദ��¼          
	TDAStringType		SellStockHK;						// �Ƿ�������ո۹�              
	TDAStringType		SellStockAM;						// �Ƿ������������                
	TDAStringType		CanTradeStockKRX;					// �Ƿ���Խ��׺���               
	TDAStringType		HkexMarket;							// �Ƿ���Ի�ȡ�ڻ��۽���HKEX���飺0�������ԣ�1�����ԣ���ʹ���Ż����飩��2������ʹ���Ż����飻3������ʹ���Ż����� mantis1080 mantis393           
	TDAStringType		IdNumber;							// �û����֤����Ʊ�����֤���ͣ�ֻ������Ϊ1ʱ����ѡ88���Ż����飻�ڻ������֤���룬15λ��18λ�ǹ��ڿͻ���    
	TDAStringType		HkexMarketFee;						// �۽��������շѽ�Ϊ0ʱ��ʾ�ڻ����ڣ�����0��ʾ��ʼ�շѣ�       
	TDAStringType		IsProfessional;						// CME����Ȩ���Ƿ���רҵ�棨1���ǣ�0����  
	TDAStringType		IsOverSea;							// �Ƿ����¼       
	TDAStringType		IsFirstLogin;						// �Ƿ����豸���ε�¼ 
	TDAStringType		UserMobile;							// �û��ֻ��� 
	TDAStringType		HasSetQA;							// �Ƿ��Ѿ��������ܱ������ 
	TDAStringType		CanTradeStockSGXQ;					// �Ƿ���Խ����¼��¹�      
	TDAStringType		ExistMac;							// �Ƿ��Ѿ��󶨹��豸mac��ַ��1���ǣ�0 or other������   
	TDAStringType		RatioINE;							// �Ϻ���Դ��ȡ�ʽ�ϵ��          
	TDAStringType		EurexMarket;						// �Ƿ���Ի�ȡEurex���飺0�������ԣ�1�����ԣ���̫���Żݣ���2�����ԣ���רҵ����3�����ԣ�רҵͶ���ߣ���4�������ԣ�����ʾ����̫������ʹ����̫���Ż����飩   
	TDAStringType		HkexIsOverMaxTerminal;				// �Ƿ񳬹�����ն���:0:δ����,��0����      
	TDAStringType		HkexOverMoney;						// �۽��������ն����շ�      
	TDAStringType		CanTradeStockAU;					// �Ƿ�ɽ��װĹ�      
	TDAStringType		NyFlag;								// ��Դ��ʾ
};
// �û��ǳ�����
struct CFutureReqUserLogoutField
{
	TDAStringType		UserId;								// �û���ʶ
	TDAStringType		AccountNo;							// �ʽ��˺�
	TDAStringType		ErrorDescription;					// ������Ϣ
};
// ������������
struct CFutureReqOrderInsertField
{
	TDAStringType		UserId;								// �û���ʶ
	TDAStringType		UserType;							// �û����ͣ�1��һ���û���2������ͨ�û���
	TDAStringType		AccountNo;							// �ʽ��˺�
	TDAStringType		LocalNo;							// ���ر��
	TDAStringType		TradePwd;							// ��������
	TDAStringType		IsRiskOrder;						// �û��µ����ͣ�C���ǿտͻ��µ���D����del�µ� R��ǿƽ�µ�����أ���Y��ӯ�𵥣�T��������
	TDAStringType		ExchangeCode;						// ����������
	TDAStringType		TreatyCode;							// ��Լ����
	TDAStringType		BuySale;							// ��������1=buy 2=sell
	TDAStringType		AddReduce;							// ���ֻ���ƽ�֣�1=���� 2=ƽ�֣�3=ƽ��
	TDAStringType		OrderNumber;						// �µ���
	TDAStringType		OrderPrice;							// �µ��۸�
	TDAStringType		TradeType;							// ���׷�ʽ��1=regular 2=FOK 3=IOC
	TDAStringType		PriceType;							// �������ͣ�1=�޼۵�, 2=�м۵���3=�޼�ֹ��stop to limit����4=ֹ��stop to market��
	TDAStringType		HtsType;							// ���ں�Լ�µ��� "STARTEGY";�Զ�������µ���"SELFDEFINE"
	TDAStringType		ForceID;							// ǿƽ���
	TDAStringType		TriggerPrice;						// �����۸�
	TDAStringType		ValidDate;							// ��Ч���ڣ�1=������Ч, 2=������Ч��GTC����3=OPG��4=IOC��5=FOK��6=GTD��7=ATC��8=FAK��
	TDAStringType		StrategyId;							// ����ID 20130726 add
	TDAStringType		MaxShow;							// ��ʾί���� 20150803 add ����С��ί����
	TDAStringType		MinQty;								// ��С�ɽ��� 20150901 add ����С�ڵ���ί���� ��Ч����=4IOCʱ MaxShow>=1С��ί����ʱ��FOK������ί����ʱ��FAK
	TDAStringType		ErrorDescription;					// ������Ϣ
};
// ������������
struct CFutureRspOrderInsertField
{
	TDAStringType		UserId;								// �û���ʶ
	TDAStringType		AccountNo;							// �ʽ��˺�
	TDAStringType		SystemNo;							// ϵͳ���
	TDAStringType		LocalNo;							// ���ر��
	TDAStringType		OrderNo;							// ������
	TDAStringType		OrigOrderNo;						// ԭ������
	TDAStringType		OrderMethod;						// �µ���ʽ��1��������2���ĵ���3������
	TDAStringType		AcceptType;							// ��������
	TDAStringType		ExchangeCode;						// ����������
	TDAStringType		TreatyCode;							// ��Լ����
	TDAStringType		BuySale;							// ��������1=buy 2=sell
	TDAStringType		OrderNumber;						// �µ���
	TDAStringType		OrderPrice;							// �µ��۸�
	TDAStringType		FilledNumber;						// �ѳɽ���
	TDAStringType		FilledPrice;						// �ɽ�����
	TDAStringType		TradeType;							// ���׷�ʽ��1=regular 2=FOK 3=IOC
	TDAStringType		PriceType;							// �������ͣ�1=�޼۵�, 2=�м۵���3=�޼�ֹ��stop to limit����4=ֹ��stop to market��
	TDAStringType		HtsType;							// 0=regular 1=HTS
	TDAStringType		OrderDate;							// �µ�����
	TDAStringType		OrderTime;							// �µ�ʱ��
	TDAStringType		ErrorCode;							// �������
	TDAStringType		OrderState;							// ����״̬��1��������2�����Ŷӣ�3�����ֳɽ���4����ȫ�ɽ���5���ѳ��൥��6���ѳ�����7��ָ��ʧ�ܣ�8�����ͳ���9�������ģ�A����������
	TDAStringType		IsRiskOrder;						// �û��µ����ͣ�C���ǿտͻ��µ���D����del�µ� R��ǿƽ�µ�����أ���Y��ӯ�𵥣�T��������
	TDAStringType		CancelUserId;						// �������û���ʶ
	TDAStringType		TriggerPrice;						// �����۸�
	TDAStringType		ValidDate;							// ��Ч���ڣ�1=������Ч, 2=������Ч��GTC����3=OPG��4=IOC��5=FOK��6=GTD��7=ATC��8=FAK��
	TDAStringType		AddReduce;							// ���ֻ���ƽ�֣�1=���� 2=ƽ�֣�3=ƽ��4=ƽ��
	TDAStringType		StrategyId;							// ����ID 20130726 add
	TDAStringType		MaxShow;							// ��ʾί���� 20150803 add ����С��ί����
	TDAStringType		MinQty;								// ��С�ɽ��� 
	TDAStringType		ExchangeTime;						// ����������ʱ��
	TDAStringType		CancelTime;							// ����ʱ��
};
// �޸Ķ�������
struct CFutureReqOrderModifyField
{
	TDAStringType		SystemNo;							// ϵͳ���
	TDAStringType		UserId;								// �û���ʶ
	TDAStringType		UserType;							// �û����ͣ�1��һ���û���2������ͨ�û���
	TDAStringType		LocalNo;							// ���ر��
	TDAStringType		AccountNo;							// �ʽ��˺�
	TDAStringType		TradePwd;							// ��������
	TDAStringType		OrderNo;							// ������
	TDAStringType		ExchangeCode;						// ����������
	TDAStringType		TreatyCode;							// ��Լ����
	TDAStringType		BuySale;							// ��������1=buy 2=sell
	TDAStringType		OrderNumber;						// �µ���
	TDAStringType		OrderPrice;							// �µ��۸�
	TDAStringType		FilledNumber;						// �ѳɽ��� 
	TDAStringType		ModifyNumber;						// �ĵ��� 
	TDAStringType		ModifyPrice;						// �ĵ��۸�
	TDAStringType		TradeType;							// ���׷�ʽ��1=regular 2=FOK 3=IOC
	TDAStringType		PriceType;							// �۸����ͣ�1=�޼۵�, 2=�м۵���3=�޼�ֹ��stop to limit����4=ֹ��stop to market��
	TDAStringType		IsRiskOrder;						// �û��µ����ͣ�C���ǿտͻ��µ���D����del�µ� R��ǿƽ�µ�����أ�
	TDAStringType		TriggerPrice;						// �����۸�
	TDAStringType		ModifyTriggerPrice;					// �ĵ������۸�
	TDAStringType		ValidDate;							// ��Ч���ڣ�1��������Ч��2��������Ч��
	TDAStringType		ErrorDescription;					// ������Ϣ
};
// �޸Ķ�������
typedef CFutureRspOrderInsertField CFutureRspOrderModifyField;
// ��������
struct CFutureReqOrderCancelField
{
	TDAStringType		UserId;								// �û���ʶ
	TDAStringType		UserType;							// �û����ͣ�1��һ���û���2������ͨ�û���
	TDAStringType		LocalNo;							// ���ر��
	TDAStringType		AccountNo;							// �ʽ��˺�
	TDAStringType		TradePwd;							// ��������
	TDAStringType		IsSimulation;						// �Ƿ�ģ���û���1���ǣ�0 or other������
	TDAStringType		SystemNo;							// ϵͳ���
	TDAStringType		OrderNo;							// ������
	TDAStringType		ExchangeCode;						// ����������
	TDAStringType		TreatyCode;							// ��Լ����
	TDAStringType		BuySale;							// ��������1=buy 2=sell
	TDAStringType		OrderNumber;						// �µ���
	TDAStringType		OrderPrice;							// �µ��۸�
	TDAStringType		FilledNumber;						// �ѳɽ��� 
	TDAStringType		TradeType;							// ���׷�ʽ��1=regular 2=FOK 3=IOC
	TDAStringType		PriceType;							// �۸����ͣ�1=limit order, 2=market order
	TDAStringType		HtsType;							// 0=regular 1=HTS
	TDAStringType		IsRiskOrder;						// �û��µ����ͣ�C���ǿտͻ��µ���D����del�µ� R��ǿƽ�µ�����أ�
	TDAStringType		ErrorDescription;					// ������Ϣ
};
// ��������
struct CFutureRspOrderCancelField
{
	TDAStringType		UserId;								// �û���ʶ
	TDAStringType		AccountNo;							// �ʽ��˺�
	TDAStringType		SystemNo;							// ϵͳ���
	TDAStringType		LocalNo;							// ���غ�
	TDAStringType		OrderNo;							// ������
	TDAStringType		CancelNo;							// ������
	TDAStringType		ExchangeCode;						// ����������
	TDAStringType		TreatyCode;							// ��Լ����
	TDAStringType		BuySale;							// ��������1=buy 2=sell
	TDAStringType		OrderNumber;						// �µ���
	TDAStringType		OrderPrice;							// �µ��۸�
	TDAStringType		FilledNumber;						// �ѳɽ���
	TDAStringType		CancelNumber;						// �ѳ�����
	TDAStringType		TradeType;							// ���׷�ʽ��1=regular 2=FOK 3=IOC
	TDAStringType		PriceType;							// �۸����ͣ�1=limit order, 2=market order
	TDAStringType		HtsType;							// 0=regular 1=HTS
	TDAStringType		CancelDate;							// ��������
	TDAStringType		CancelTime;							// ����ʱ��
	TDAStringType		ErrorCode;							// �������
	TDAStringType		IsRiskOrder;						// �û��µ����ͣ�C���ǿտͻ��µ���D����del�µ� R��ǿƽ�µ�����أ�
};
// �޸���������
struct CFutureReqPasswordUpdateField
{
	TDAStringType		UserId;								// �û�����
	TDAStringType		OldPassword;						// �û�ԭ����
	TDAStringType		NewPassword;						// �û�������
	TDAStringType		ErrorDescription;					// ������Ϣ
};
// �޸����뷵��
struct CFutureRspPasswordUpdateField
{
	TDAStringType		UserId;								// �û�����
	TDAStringType		OldPassword;						// �û�ԭ����
	TDAStringType		NewPassword;						// �û�������
};
// ��ѯ��������
struct CFutureQryOrderField
{
	TDAStringType		UserId;								// �û���ʶ
	TDAStringType		UserType;							// �û����ͣ�1��һ���û���2������ͨ�û���
	TDAStringType		AccountNo;							// �ʽ��˺�
	TDAStringType		TradePwd;							// ��������
	TDAStringType		IsSimulation;						// �Ƿ�ģ���û���1���ǣ�0 or other������
	TDAStringType		OrderNo;							// ȡ��ָ���������Ժ�Ķ���
	TDAStringType		OrderDateTime;						// ȡ��ָ������ʱ���Ժ�Ķ�������ʽ��yyyy-MM-dd hh:mm:ss��
	TDAStringType		ErrorDescription;					// ������Ϣ
};
// ��ѯ��������
struct CFutureRspOrderField
{
	TDAStringType		UserId;								// �û���ʶ
	TDAStringType		AccountNo;							// �ʽ��˺�
	TDAStringType		SystemNo;							// ϵͳ���
	TDAStringType		LocalNo;							// ���ر��
	TDAStringType		OrderNo;							// ������
	TDAStringType		OrigOrderNo;						// ԭ������
	TDAStringType		OrderMethod;						// �µ���ʽ��1��������2���ĵ���3������
	TDAStringType		AcceptType;							// ��������
	TDAStringType		ExchangeCode;						// ����������
	TDAStringType		TreatyCode;							// ��Լ����
	TDAStringType		BuySale;							// ��������1=buy 2=sell
	TDAStringType		OrderNumber;						// �µ���
	TDAStringType		OrderPrice;							// �µ��۸�
	TDAStringType		FilledNumber;						// �ѳɽ���
	TDAStringType		FilledPrice;						// �ɽ�����
	TDAStringType		TradeType;							// ���׷�ʽ��1=regular 2=FOK 3=IOC
	TDAStringType		PriceType;							// �������ͣ�1=�޼۵�, 2=�м۵���3=�޼�ֹ��stop to limit����4=ֹ��stop to market��
	TDAStringType		HtsType;							// 0=regular 1=HTS
	TDAStringType		OrderDate;							// �µ�����
	TDAStringType		OrderTime;							// �µ�ʱ��
	TDAStringType		ErrorCode;							// �������
	TDAStringType		OrderState;							// ����״̬��1��������2�����Ŷӣ�3�����ֳɽ���4����ȫ�ɽ���5���ѳ��൥��6���ѳ�����7��ָ��ʧ�ܣ�8�����ͳ���9�������ģ�A����������
	TDAStringType		IsRiskOrder;						// �û��µ����ͣ�C���ǿտͻ��µ���D����del�µ� R��ǿƽ�µ�����أ���Y��ӯ�𵥣�T��������
	TDAStringType		CancelUserId;						// �������û���ʶ
	TDAStringType		TriggerPrice;						// �����۸�
	TDAStringType		ValidDate;							// ��Ч���ڣ�1=������Ч, 2=������Ч��GTC����3=OPG��4=IOC��5=FOK��6=GTD��7=ATC��8=FAK��
	TDAStringType		AddReduce;							// ���ֻ���ƽ�֣�1=���� 2=ƽ�֣�3=ƽ��4=ƽ��
	TDAStringType		StrategyId;							// ����ID 20130726 add
	TDAStringType		MaxShow;							// ��ʾί���� 20150803 add ����С��ί����
	TDAStringType		MinQty;								// ��С�ɽ��� 
	TDAStringType		ExchangeTime;						// ����������ʱ��
	TDAStringType		CancelTime;							// ����ʱ��
};
// ��ѯ�ɽ�����
struct CFutureQryTradeField
{
	TDAStringType		UserId;								// �û�		
	TDAStringType		ErrorDescription;					// ������Ϣ
};
// ��ѯ�ɽ�����
struct CFutureRspTradeField
{
	TDAStringType		UserId;								// �û���ʶ
	TDAStringType		AccountNo;							// �ʽ��˺�
	TDAStringType		FilledNo;							// �ɽ���ţ�Ҫ����7λ�Ķ�����ţ�һ��11λ��
	TDAStringType		OrderNo;							// ������
	TDAStringType		SystemNo;							// ϵͳ���
	TDAStringType		LocalNo;							// ���ر��
	TDAStringType		ExchangeCode;						// ����������
	TDAStringType		TreatyCode;							// ��Լ����
	TDAStringType		BuySale;							// ��������1=buy 2=sell
	TDAStringType		FilledNumber;						// �ɽ���
	TDAStringType		FilledPrice;						// �ɽ��۸�
	TDAStringType		FilledDate;							// �ɽ�����(yyyy-MM-dd)
	TDAStringType		FilledTime;							// �ɽ�ʱ��(hh:mm:ss)
	TDAStringType		Commsion;							// �ɽ�������
	TDAStringType		OrderNumber;						// ί������
	TDAStringType		OrderPrice;							// ί�м۸�
	TDAStringType		DeliveryDate;						// ��Լ��������(yyyyMMdd)
	TDAStringType		FilledType;							// �ɽ����(N����ͨ�µ��ɽ���C��T������ģ��ɽ�)
	TDAStringType		OrderType;							// �������ͣ�1=�޼۵�, 2=�м۵���3=�޼�ֹ��stop to limit����4=ֹ��stop to market��
	TDAStringType		ValidDate;							// ��Ч���ڣ�1=������Ч, 2=������Ч��
	TDAStringType		AddReduce;							// ���ֻ���ƽ�֣�1=���� 2=ƽ�֣�3=ƽ��4=ƽ��
	TDAStringType		ErrorDescription;					// ������Ϣ
};
// ��ѯ��Լ����
struct CFutureQryInstrumentField
{
	TDAIntType			PageIndex;							// ��ѯ������,ÿ�η��ص�����
	TDAStringType		ExchangeNo;							// ���������룬�����дֵ����ѯһ���������ĺ�Լ
	TDAStringType		CommodityNo;						// ��Լ���롣��ѯ������Լ	
	TDAStringType		CommodityType;						// ��Ʒ��� 
	TDAStringType		ContractNo;							// ��ԼNO
	TDAStringType		ErrorDescription;					// ������Ϣ
};
// ��ѯ��Լ����
struct CFutureRspInstrumentField
{
	TDAStringType		CommodityCode;						// ��Ʒ��ź�ԼNO 
	TDAStringType		ExchangeNo;							// ���������
	TDAStringType		ContractNo;							// ��ԼNO
	TDAStringType		ContractFName;						// ��Լ��
	TDAStringType		CommodityNo;						// ��Ʒ���
	TDAStringType		CommodityFName;						// ��Ʒ�� 
	TDAStringType		CommodityType;						// ��Ʒ��� 
	TDAStringType		CommodityFCurrencyNo;				// ���ұ�� 
	TDAStringType		CurrencyFName;						// �������� 
	TDADoubleType		ProductDot;							// ��ֵ��һ����С����ļ�ֵ��
	TDADoubleType		UpperTick;							// ��С�䶯��λ 
	TDAStringType		ExchangeName;						// ���������� 
	TDADoubleType		LastSettlePrice;					// ���ս���� 
	TDAStringType		TradeMonth;							// ������ (yyyyMM)/������ (yyyyMMdd)
	TDAIntType			DotNum;								// ����С����λ��
	TDAIntType			LowerTick;							// ���׵�λ
	TDAIntType			DotNumCarry;						// ����С����λ��
	TDADoubleType		UpperTickCarry;						// ������С�䶯��λ
	TDAStringType		FirstNoticeDay;						// �״�֪ͨ�� (yyyyMMdd)
	TDADoubleType		FreezenPercent;						// ���ᱣ֤��ٷֱ� ���Ϻ���Դ���뱣֤��ٷֱȣ�
	TDADoubleType		FreezenMoney;						// ���ᱣ֤��̶�ֵ 
	TDADoubleType		FeeMoney;							// �̶������� 
	TDADoubleType		FeePercent;							// �ٷֱ������� 
	TDADoubleType		PriceStrike;						// �ֻ���Ʒ������ 
	TDADoubleType		ProductDotStrike;					// �ֻ���Ʒ��ֵ  
	TDADoubleType		UpperTickStrike;					// �ֻ���Ʒ��С�䶯��λ 
	TDAStringType		LastTradeDay;						// ������� (yyyyMMdd)
	TDAStringType		LastUpdateDay;						// �������� (yyyyMMdd)
	TDADoubleType		CriticalPrice;						// ��Ȩ�ٽ�۸� 
	TDADoubleType		CriticalMinChangedPrice;			// ��Ȩ�ٽ�۸����µ���С���� 
	TDAStringType		ExchangeSub;						// ʵ�ʽ�����(CMEϸ�ֳ�3��������:CME,CME_COMEX,CME_NYMEX)
	TDAStringType		OptionType;							// ��Ȩ����(R�����ǣ�F������)
	TDAStringType		OptionMonth;						// ��Ȩ����(yyyyMM)
	TDAStringType		OptionStrikePrice;					// ��Ȩִ�м۸�
	TDAStringType		OptionCommodityNo;					// ��Ȩ��Ӧ�ڻ���Ʒ��ţ��Ϻ���Դ������֤��ٷֱȣ�
	TDAStringType		OptionContractNo;					// ��Ȩ��Ӧ�ڻ���Լ���
	TDAStringType		ContractFNameEN;					// ��Լ����Ӣ�ģ�
	TDAStringType		CommodityFNameEN;					// ��Ʒ����Ӣ�ģ�
	TDAStringType		OptionStyle;						// ��Ȩ���(E��ŷʽ��A����ʽ)
};
// ��ѯ����������
struct CFutureQryExchangeField
{
	TDAStringType		ProductGroupID;
	TDAStringType		ErrorDescription;					// ������Ϣ
};
// ��ѯ����������
struct CFutureRspExchangeField
{
	TDAStringType		ExchangeNo;							// ���������
	TDAStringType		ExchangeName;						// ����������
	TDAStringType		SettleType;							// ���������ͣ�HK���۹ɣ�US�����ɣ�
	TDAStringType 		NameEN;								// ���������ƣ�Ӣ�ģ�
};
// ��ѯ�ʽ�����
struct CFutureQryCapitalField
{
	TDACharType			Unused;								// ��ʹ��	
	TDAStringType		ErrorDescription;					// ������Ϣ
};
// ��ѯ�ʽ𷵻�
struct CFutureRspCapitalField
{
	TDAStringType		UserId;								// �û���ʶ
	TDAStringType		InMoney;							// ���
	TDAStringType		OutMoney;							// ����
	TDAStringType		TodayCanUse;						// �����
	TDAStringType		TodayAmount;						// ����
	TDAStringType		TodayBalance;						// ��Ȩ��
	TDAStringType		FreezenMoney;						// �����ʽ�
	TDAStringType		Commission;							// Ӷ��
	TDAStringType		Margin;								// ��֤��
	TDAStringType		OldCanUse;							// �����
	TDAStringType		OldAmount;							// ����
	TDAStringType		OldBalance;							// ��Ȩ��
	TDAStringType		FloatingProfit;						// ����ӯ��
	TDAStringType		CurrencyNo;							// ���ֱ�� 
	TDAMoneyType		CurrencyRate;						// ����������Ļ���
	TDAMoneyType		UnexpiredProfit;					// δ����ƽӯ
	TDAMoneyType		UnaccountProfit;					// δ��ƽӯ
	TDAMoneyType		KeepDeposit;						// ά�ֱ�֤��
	TDAMoneyType		Royalty;							// ��ȨȨ����
	TDAMoneyType		Credit;								// ���ζ��
	TDAMoneyType		AddCapital;							// �����ʽ�
	TDAMoneyType		IniEquity;							// ��ʼ�ʽ�
	TDAStringType		AccountNo;							// �ʽ��ʺ� 1
	TDAMoneyType		MortgageMoney;						// ���Ҽ�ֵ 20150610 added for �۹�
	TDAMoneyType		MarginLimit;						// �Iչ���޶�� 20150727 added for �۹�
	TDAMoneyType		BorrowValue;						// �����ֵ 20150727 added for �۹�
	TDAMoneyType		T1;									// T1 20160219 added for �۹�
	TDAMoneyType		T2;									// T2 20160219 added for �۹�
	TDAMoneyType		T3;									// T3 20160219 added for �۹�
	TDAMoneyType		TN;									// Tn 20160219 added for �۹�
	TDAMoneyType		TradeLimit;							// �����޶�
	TDAMoneyType		CanCashOut;							// ��ȡ�ʽ�
	TDAMoneyType		AccruedCrInt;						// �´����Ϣ
	TDAMoneyType		AccruedDrInt;						// ��Ƿ����Ϣ
	TDAMoneyType		CrossMax;							// ���г��ʽ��޶�
	TDAMoneyType		SellFreezenMoney;					// ���ն����ʽ�
	TDAMoneyType		SellInterest;						// ������Ϣ
	TDAMoneyType		SellNeedAddMargin;					// �貹����
	TDAStringType		NetProfit;							// ��ӯ�� 1
	TDAStringType		ProfitRate;							// ӯ���� 1
	TDAStringType		RiskRate;							// ������ 1
	TDAStringType		ErrorDescription;					// ������Ϣ
};
// ��ѯ�ֲ�����
struct CFutureQryPositionField
{
	TDAStringType		ErrorDescription;					// ������Ϣ
};
// ��ѯ�ֲַ���
struct CFutureRspPositionField
{
	TDAStringType		MatchDate;							// �ɽ����ڣ�yyyyMMdd��
	TDAStringType		MatchNo;							// �ɽ����
	TDAStringType		ClientNo;							// �ͻ����
	TDAStringType		ExchangeNo;							// ���������
	TDAStringType		CommodityNo;						// ��Ʒ���
	TDAStringType		ContractNo;							// ��Լ���
	TDAStringType		Direct;								// ��������1����2������
	TDAVolumeType		HoldVol;							// �ֲ���
	TDAPriceType		HoldPrice;							// ���־��ۣ�ԭʼ���ּۣ�
	TDAStringType		CurrencyNo;							// ���ұ��
	TDAPriceType		ForciblyPrice;						// �����ĳֲ־���
	TDAStringType		Account;							// �ʽ��˺�
	TDAStringType		HoldType;							// �ֲ����ͣ�0����֣�1����֣�
	TDAStringType		DeliveryDate;						// ��Լ��������(yyyyMMdd)
	TDAStringType		ExchangeName;						// ����������(�ͻ����Լ�ȡ��)
	TDAStringType		CurrencyName;						// ��������(�ͻ����Լ�ȡ��)
	TDAStringType		ContCode;							// ��Լ���루��Ʒ���+��Լ��ţ�(�ͻ����Լ�ȡ��)
	TDAPriceType		HoldMargin;							// �ֱֲ�֤�� add 20141222
};
// ��ѯ��������
struct CFutureQryTickField
{
	TDACharType			Unused;								// ��ʹ��
	TDAStringType		ErrorDescription;					// ������Ϣ
};
// ��ѯ���㷵��
struct CFutureRspTickField
{
	TDAStringType		UpperTickCode;						// ��С�䶯��λ����
	TDAStringType		PriceFrom;							// ��С�䶯��λ��ʼ����۸�
	TDAStringType		UpperTick;							// ������С�䶯��λ
	TDAStringType		ProductDot;							// ��С�䶯��λ��Ӧ�ĵ�ֵ
	TDAStringType		DotNum;								// ����С��λ��
	TDAStringType		LowerTick;							// ���۵�λ
};
// ��ѯ��������
struct CFutureQryCurrencyField
{
	TDACharType			Unused;								// ��ʹ��
	TDAStringType		ErrorDescription;					// ������Ϣ
};
// ��ѯ���ҷ���
struct CFutureRspCurrencyField
{
	TDAStringType		CurrencyNo;							// ���ұ��
	TDAIntType			IsBase;								// ���һ��ұ��
	TDADoubleType		ChangeRate;							// ����ҵĻ������
	TDAStringType		CurrencyName;						// ��������
	TDAStringType		CurrencyNameEN;						// �������ƣ�Ӣ�ģ�
};
// ��ѯ������ʱ������
struct CFutureQryCommodityField
{
	TDAStringType		UpdateDate;							// ��������
	TDAStringType		ExchangeNo;							// ���������
	TDAStringType		ErrorDescription;					// ������Ϣ
};
// ��ѯ��Ʒ�б�
struct CFutureRspCommodityField
{
	TDAStringType		CommodityNo;						// ��Ʒ���
	TDAStringType		ExchangeNo;							// ���������
	TDAStringType		CommodityType;						// ��Ʒ����	
	TDAStringType		Name;								// ��Ʒ����
	TDAStringType		Enabled;							// ����״̬
	TDAStringType		RegDate;							// ������	
	TDAStringType		CurrencyNo;							// ���ֱ��	
	TDADoubleType		ProductDot;							// ��������ֵ
	TDADoubleType		LowerTick;							// ���׵�λ
	TDADoubleType		UpperTick;							// ��С�䶯��λ	
	TDAIntType			DotNum;								// ����С����λ��
	TDAIntType			StrikeCommodityId;					// ���Ժ�ԼID
	TDAStringType		OptionStyle;						// ��Ȩ����
	TDAStringType		ExchangeNo2;						// ��������� (��ExchangeNo�µĽ���������COMEX NYMEX)
	TDAStringType		IsSFuture;							// �Ƿ��Ǹ����ڻ�
};
// ��ѯ������������ʱ������
struct CFutureQryExchangeTimeField
{
	TDACharType			Unused;								// ��ʹ��
	TDAStringType		ErrorDescription;					// ������Ϣ
};
// ��ѯ��Ʒ������ʱ������
struct CFutureQryCommodityTimeField
{
	TDAStringType		ExchangeNo;							// ����������
	TDAStringType		CommodityNo;						// ��Ʒ����
	TDAStringType		ErrorDescription;					// ������Ϣ
};
// ��ѯ������������ʱ�䷵��
struct CFutureRspExchangeTimeField
{
	TDAStringType		Year;								//  ��ǰ���
	TDAStringType		SummerBegin;						//  ����ʱ��ʼʱ��
	TDAStringType		WinterBegin;						//  ����ʱ��ʼʱ��
	TDAStringType		ExchangeNo;							//  ����������
	TDAStringType		Name;								//  ����������
};
// ��ѯ��Ʒ������ʱ�䷵��
struct CFutureRspCommodityTimeField
{
	TDAStringType		CrossTrade;							// �Ƿ����
	TDAStringType		Stage;								// ״̬
	TDAStringType		Summer;								// 2���� 1����	
	TDAStringType		Opendate;							// ��Ʒ����ʱ��
	TDAStringType		Closingdate;						// ��Ʒ����ʱ��
	TDAStringType		CommodityNo;						// ��Ʒ����
	TDAStringType		ComName;							// ��Ʒ����
	TDAStringType		ExchangeNo;							// ����������
	TDAStringType		ExName;								// ����������
};
// ��ѯ�汾����
struct CFutureQryVersionField
{
	TDAStringType		UserId;								// �û���ʶ
	TDAStringType		UserPwd;							// �û�����
	TDAStringType		ErrorDescription;					// ������Ϣ
};
// ��ѯ�汾����
struct CFutureRspVersionField
{
	TDAStringType		Version;							// �汾��
	TDAStringType		MustUpdate;							// �Ƿ������µ��°汾��������ʹ�ã�0�����Բ����£�1��������£�
	TDAStringType		MustVersion;						// ����Ҫ�����İ汾��
	TDAStringType		VersionContent_CN;					// �汾��������
	TDAStringType		VersionContent_US;					// �汾����Ӣ��
};
//-------------------------------------------------------------------------
// ���Ͷ����仯
struct CFutureRtnOrderField
{
	TDAStringType		LocalOrderNo;						// ���ض�����
	TDAStringType		ExchangeNo;							// ����������
	TDAStringType		TreatyCode;							// ��Լ����
	TDAStringType		OrderNo;							// ������
	TDAIntType			OrderNumber;						// ί������
	TDAIntType			FilledNumber;						// �ѳɽ�����
	TDAPriceType		FilledAdvPrice;						// �ɽ�����
	TDAIntType			BuyHoldNumber;						// ��������
	TDAPriceType		BuyHoldOpenPrice;					// ���򿪲־���
	TDAPriceType		BuyHoldPrice;						// �������
	TDAIntType			SaleHoldNumber;						// ��������
	TDAPriceType		SaleHoldOpenPrice;					// �������־���
	TDAPriceType		SaleHoldPrice;						// ��������
	TDAStringType		IsCanceled;							// �Ƿ��Ѿ�������0��û�У�1���ѳ�����
	TDAPriceType		FilledTotalFee;						// �ɽ��ܵ�������
	TDAIntType			Status;								// ˳���
	TDAStringType		AccountNo;							// �ʽ��ʺ�
	TDAStringType		HoldType;							// �ֲ����ͣ�0����֣�1����֣�
	TDAPriceType		HoldMarginBuy;						// ����֤��
	TDAPriceType		HoldMarginSale;						// ������֤��
	TDAPriceType		CurrPrice;							// ���¼�
	TDAPriceType		FloatProfit;						// ����ӯ��
};
// �����ʽ�仯
struct CFutureRtnCapitalField
{
	TDAStringType		ClientNo;							// �ͻ���
	TDAStringType		AccountNo;							// �ʽ��ʺ�
	TDAStringType		CurrencyNo;							// ����
	TDAPriceType		Available;							// �����
	TDAPriceType		YAvailable;							// �����
	TDAPriceType		CanCashOut;							// ��ɳ�
	TDAPriceType		Money;								// ����
	TDAPriceType		ExpiredProfit;						// ƽ��ӯ��
	TDAPriceType		FrozenDeposit;						// �����ʽ�
	TDAPriceType		Fee;								// ������
	TDAPriceType		Deposit;							// ��֤��
	TDAPriceType		KeepDeposit;						// ά�ֱ�֤��
	TDAIntType			Status;								// ״̬
	TDAPriceType		InMoney;							// ���
	TDAPriceType		OutMoney;							// ����
	TDAPriceType		UnexpiredProfit;					// δ����ƽӯ
	TDAPriceType		TodayTotal;							// ��Ȩ��
	TDAPriceType		UnaccountProfit;					// δ��ƽӯ
	TDAPriceType		Royalty;							// ��ȨȨ����
	TDAStringType		ExchangeNo;							// ����������
	TDAStringType		TreatyCode;							// ��Լ����
	TDAStringType		OrderNo;							// ������
	TDAIntType			OrderNumber;						// ί������
	TDAIntType			FilledNumber;						// �ѳɽ�����
	TDAPriceType		FilledAdvPrice;						// �ɽ�����
	TDAIntType			BuyHoldNumber;						// ��������
	TDAPriceType		BuyHoldOpenPrice;					// ���򿪲־���
	TDAPriceType		BuyHoldPrice;						// �������
	TDAIntType			SaleHoldNumber;						// ��������
	TDAPriceType		SaleHoldOpenPrice;					// �������־���
	TDAPriceType		SaleHoldPrice;						// ��������
	TDAStringType		IsCanceled;							// �Ƿ��Ѿ�������0��û�У�1���ѳ�����
	TDAPriceType		FilledTotalFee;						// �ɽ��ܵ�������
	TDAPriceType		Credit;								// ���ζ��
	TDAPriceType		MarginLimit;						// �Iչ���޶�� 20150727 added for �۹�
	TDAPriceType		BorrowValue;						// �����ֵ 20150727 added for �۹�
	TDAPriceType		MortgageMoney;						// ���Ҽ�ֵ 20150727 added for �۹�
	TDAPriceType		T1;									// T1 20160219 added for �۹�
	TDAPriceType		T2;									// T2 20160219 added for �۹�
	TDAPriceType		T3;									// T3 20160219 added for �۹�
	TDAPriceType		TN;									// Tn 20160219 added for �۹�
	TDAPriceType		TradeLimit;							// �����޶�
	TDAPriceType		FCrossMax;							// ���г��ʽ��޶�
	TDAPriceType		SellFreezenMoney;					// ���ն����ʽ�
	TDAPriceType		SellInterest;						// ������Ϣ
	TDAPriceType		SellNeedAddMargin;					// �貹����
};
// ���ͳֱֲ仯
typedef CFutureRtnOrderField CFutureRtnPositionField;
// ���ͳɽ�����
typedef CFutureRspTradeField CFutureRtnTradeField;
//-------------------------------------------------------------------------
// ��ȡ����
struct CFutureReqGetQuestionField
{
	TDAIntType			Unused;								// �û��ʺ�
	TDAStringType		ErrorDescription;					// ������Ϣ
};
// ��ȡ���ⷵ��
struct CFutureRspQuestionField
{
	TDAStringType		QuestionType;						// ��������	0�������ڻ���1�����ʹ�Ʊ
	TDAStringType		QuestionId;							// ������
	TDAStringType		QuestionCN;							// ���⣨���ģ�
	TDAStringType		QuestionEN;							// ���⣨Ӣ�ģ�
};
// ��ȫ��֤����
struct CFutureReqSafeVerifyField
{
	TDAStringType		UserId;								// �û��ʺ�
	TDAStringType		UserPwd;							// ��������
	TDAStringType		Type;								// ���
	TDAStringType		Question;							// �ܱ�������
	TDAStringType		Answer;								// �ܱ������
	TDAStringType		MobileNumber;						// �ֻ���
	TDAStringType		VerifyCode;							// �ֻ���֤��
	TDAStringType		SaveMac;							// �Ƿ���Ҫ��ס���豸
	TDAStringType		MacAddress;							// MAC��ַ
	TDAStringType		ErrorDescription;					// ������Ϣ
};
// ������֤�����
struct CFutureReqSetVerifyQAField
{
	TDAStringType		UserId;								// �û��ʺ�
	TDAStringType		UserPwd;							// ��������
	TDAStringType		Type;								// ���
	TDAStringType		Question;							// �ܱ�������
	TDAStringType		Answer;								// �ܱ������
	TDAStringType		MobileNumber;						// �ֻ���
	TDAStringType		VerifyCode;							// �ֻ���֤��
	TDAStringType		SaveMac;							// �Ƿ���Ҫ��ס���豸
	TDAStringType		ErrorDescription;					// ������Ϣ
};
// ������֤��
struct CFutureReqVerifyCodeField
{
	TDAStringType		UserId;								// �û��ʺ�
	TDAStringType		UserPwd;							// ��������
	TDAStringType		Type;								// ���
	TDAStringType		Question;							// �ܱ�������
	TDAStringType		Answer;								// �ܱ������
	TDAStringType		MobileNumber;						// �ֻ���
	TDAStringType		VerifyCode;							// �ֻ���֤��
	TDAStringType		ErrorDescription;					// ������Ϣ
};
//-------------------------------------------------------------------------
// ��ѯ�ֲֺϼ�����
struct CFutureQryTotalPositionField
{
	TDAStringType		AccountNo;							// �ʽ��˺�
	TDAStringType		ErrorDescription;					// ������Ϣ
};
// ��ѯ�ֲֺϼƷ���
typedef CFutureRtnOrderField CFutureRspTotalPositionField;
// ��ѯ��������
struct CFutureQryStrategyField
{
	TDAStringType		ExchangeNo;							// ���������룬�����дֵ����ѯһ���������Ĳ���
	TDAStringType		ErrorDescription;					// ������Ϣ
};
// ��ѯ���Է���
struct CFutureRspStrategyField
{
	TDAStringType		UserId;								// ���������û�����
	TDAStringType		KeyId;								// ����Id
	TDAStringType		Name;								// ��������
	TDAStringType		Code;								// ���Դ���
	TDAIntType			PriceType;							// ���Լ۸�����
	TDAIntType			PriceTypeDetailType;				// ���Լ۸���ϸ����
	TDAStringType		PriceFormula;						// ���Լ۸�ʽ
	TDAIntType			TriggerMethod;						// ����ģʽ
	TDAIntType			InnerProtect;						// �Ƿ��������̱���
	TDAIntType			PassiveFailCloseMainLeg;			// �Ƿ񱻶����µ�ʧ������ƽ��Ӧ������
	TDAIntType			SlipPoint;							// ����ģʽΪ2���ɽ�����ʱ���õĻ�����
	TDAIntType			RecoverPriceMethod;					// ׷�ӱ�������
	TDAIntType			RecoverPriceSeconds;				// �����ȹҵ�����������м�׷��
	TDAStringType		SetType;							// ������������
	TDAPriceType		MinChangePrice;						// ��������۸���С�䶯��λ
	TDAIntType			MaxNum;								// �����ȵ�������µ���
	TDAIntType			SuportQuantity;						// �����Ⱥ�Լ��С���̹ҵ���
	TDAIntType			SafeDeep;							// ��ȫ���
	TDAIntType			MainRange;							// ��������
	TDAStringType		ManualZhuiDanBeyondNum;				// �����ֶ�׷��������
	TDAStringType		ManualPingZhuDongBeyondNum;			// �����ֶ�ƽ��������
	TDAIntType			AutoGuaDanSeconds;					// �����Զ���ʱ���ã��ҵ�����
	TDAIntType			AutoZhuiBeiDongDots;				// �����Զ���ʱ׷��������
	TDAIntType			AutoPingZhuDongDots;				// �����Զ���ʱƽ��������
	TDAIntType			AutoZhiSunDot;						// �����Զ�ֹ������
	TDAIntType			AutoZhiSunZhuiBeiDongDots;			// �����Զ�ֹ��׷�������ã�׷�ۻ�������
	TDAIntType			AutoZhiSunPingZhuDongDots;			// �����Զ�ֹ��ƽ�������ã�׷�ۻ�������
	TDAIntType			DotLen;								// ��������۸�С��λ��
	TDAStringType		TradeTime;							// ���ý��׵�ʱ���
};
// ��ѯ������ϸ����
struct CFutureQryStrategyDetailField
{
	TDAStringType		StartegyCommodityNo;				// ��Լ����
	TDAStringType		ErrorDescription;					// ������Ϣ
};
// ��ѯ������ϸ����
struct CFutureRspStrategyDetailField
{
	TDAStringType		StartegyCommodityNo;				// ������Ʒ���
	TDAStringType		StartegyContractNo;					// ���Ժ�Լ��ϱ��
	TDAStringType		Price;								// �۸�
	TDAIntType			LegNum;								// ������2����Լ����Ϊ2�ȣ�
	TDAStringType		LastTradeDate;						// ������գ�yyyy-MM-dd��
	TDAIntType			SeqId;								// �����к�Լ˳���
	TDAStringType		CommodityNo;						// �����к�Լ����Ʒ���
	TDAStringType		ContractNo;							// �����к�Լ�ĺ�Լ���
	TDAStringType		Direct;								// ��������1��ʾ��2��ʾ����
	TDAIntType			Quantity;							// ��Լ�µ�����
	TDAStringType		Model;								// ��Լ�µ�����
	TDAStringType		ModifyDate;							// ���������ڣ�yyyy-MM-dd��
	TDAStringType		OrderMethod;						// �µ����ͣ��޼ۣ��мۣ�
	TDAPriceType		PriceTolerance;						// �۸����̶�
	TDAPriceType		PriceParam;							// �۸��������
	TDAIntType			SuportQuantity;						// ��Լ��С���̹ҵ���
	TDAIntType			MinMove;							// ��Լ��С�ƶ�
	TDAIntType			TimerOrder;							// ��Լ��ʱ׷��
	TDAStringType		TimerOrderBeyondNum;				// ��ʱ׷��������
	TDAIntType			TimerOrderPrice;					// ��Լ��ʱ׷��
	TDAStringType		TimerOrderPriceBeyondNum;			// ��ʱ׷�ۻ�����
	TDAStringType		TimerOrderPriceTriggerNum;			// ��ʱ׷�۴�������
	TDAIntType			ZhiSunOrder;						// ֹ��׷��
	TDAStringType		ZhiSunOrderBeyondNum;				// ֹ��׷��������
	TDAIntType			TimerPingCang;						// ��Լ��ʱƽ��
	TDAStringType		TimerPingCangBeyondNum;				// ��ʱƽ�ֻ�����
	TDAIntType			SafeDeep;							// ��ȫ���
	TDAIntType			MainRange;							// ��������
};

