/////////////////////////////////////////////////////////////////////////
/// DriectAccess Trade Engine
/// Copyright (C) Shanghai DirectAccess Technology Co., Ltd.
/// Last Modify 2019/3/18
/// Define Stock Struct
/// Author (c) Wang Jian Quan (Franklin)
/////////////////////////////////////////////////////////////////////////

#pragma once

#include "DADataType.h"

namespace Directaccess {

	// ��������
	struct CStockRspInfoField
	{
		TDAIntType			ErrorID;							// ������
		TDAStringType		ErrorMsg;							// ��������
	};
	// �û���¼����
	struct CStockReqUserLoginField
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
	struct CStockRspAccountField
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
	struct CStockReqUserLogoutField
	{
		TDAStringType		UserId;								// �û���ʶ
		TDAStringType		AccountNo;							// �ʽ��˺�
		TDAStringType		ErrorDescription;					// ������Ϣ
	};
	// ������������
	struct CStockReqOrderInsertField
	{
		TDAStringType		UserId;								// �û���ʶ
																// User id

		TDAStringType		AccountNo;							// �ʽ��˺�
																// Account No

		TDAStringType		LocalNo;							// API�û��ĳ���ָ���ı��ض������
																// Order ID assigned by API user program

		TDAStringType		ExchangeCode;						// ����������
																// Exchange code

		TDAStringType		ContractCode;						// ��Լ����
																// Contract code 

		// ������:		STOCK_BID=��,  STOCK_ASK=��
		// Bid or ask:		STOCK_BID=bid, STOCK_ASK=ask
		TDAStringType		BidAskFlag;

		// ���ֻ���ƽ��:
				// STOCK_OPEN_POS_FLAG=����,STOCK_OPEN_POS_FLAG=ƽ��
		// open/close position flag:
				// STOCK_OPEN_POS_FLAG=open position,STOCK_CLOSE_POS_FLAG=close position
		TDAStringType		OpenCloseFlag;

		TDAStringType		OrderQty;							// �µ���
																// Order quantity

		TDAStringType		OrderPrice;							// �µ��۸�
																// Order price

		// �������ͣ�
		//		STOCK_LIMIT_ORDER=�޼۵�, STOCK_MARKET_ORDER=�м۵�
		//		STOCK_LIMIT_STOP_ORDER=�޼�ֹ��STOCK_STOP_LOSS_ORDER=ֹ��	
		// Order type:
		//		STOCK_LIMIT_ORDER=limit order, STOCK_MARKET_ORDER=market order 
		//		STOCK_LIMIT_STOP_ORDER=limit stop order ,STOCK_STOP_LOSS_ORDER=stop loss order
		TDAStringType		OrderType;

		TDAStringType		TriggerPrice;						// �����۸�
																// Trigger price

		// ��Ч����:
		//		STOCKE_TDY_TIF=������Ч, STOCK_GTC_TIF=������Ч��GTC����STOCK_OPG_TIF=OPG,STOCK_IOC_TIF4=IOC
		//		STOCK_FOK_TIF=FOK��STOCK_GTD_TIF=GTD��STOCK_ATC_TIF=ATC��STOCK_FAK_TIF=FAK
		// Order time in force:
		//		STOCK_TDY_TIF=the day only,STOCK_GTC_TIF=GTC,STOCK_OPG_TIF=OPG,STOCK_IOC_TIF=IOC
		//		STOCK_FOK_TIF=FOK,STOCK_GTD_TIF=GTD,STOCK_ATC_TIF=ATC,STOCK_FAK_TIF=FAK						
		TDAStringType		TIF;

		TDAStringType		StrategyId;							// ����ID 20130726 add
																// Strategy id

		TDAStringType		MaxShow;							// ��ɽ����ʾ���������
																// Max show quantity for ICE order		

		TDAStringType		MinQty;								// FAK/FOK��������С�ɽ���
																// Min filled quantity expected by FAK/FOK order

		TDAStringType		ErrorDescription;					// ������Ϣ
																// Error message description
	};
	// ������������
	struct CStockRspOrderInsertField
	{
		TDAStringType		UserId;								// �û���ʶ
																// User id

		TDAStringType		AccountNo;							// �ʽ��˺�
																// Account No

		TDAStringType		SystemNo;							// ϵͳ���
																// System No	

		TDAStringType		LocalNo;							// ���ر�� API�û��ĳ���ָ���ı��ض������
																// Order ID assigned by API user program

		TDAStringType		OrderNo;							// ������ ������ϵͳ�����Ķ����ţ�LocalNo:SystemNo:OrderNo��һ��һ��һ�Ĺ�ϵ
																// The order number given by the exchange system ,LocalNo:SystemNo:OrderNo,these three are one-to-one relationships

		TDAStringType		ExchangeCode;						// ����������
																// Exchange code	

		TDAStringType		ContractCode;						// ��Լ����
																// Contract code
		// ������:		STOCK_BID=��,  STOCK_ASK=��
		// Bid or ask:		STOCK_BID=bid, STOCK_ASK=ask
		TDAStringType		BidAskFlag;

		TDAStringType		OrderQty;							// �µ���
																// Order quantity

		TDAStringType		OrderPrice;							// �µ��۸�
																// Order price	

		// �������ͣ�
		//		STOCK_LIMIT_ORDER=�޼۵�, STOCK_MARKET_ORDER=�м۵�
		//		STOCK_LIMIT_STOP_ORDER=�޼�ֹ��STOCK_STOP_LOSS_ORDER=ֹ��	
		// Order type:
		//		STOCK_LIMIT_ORDER=limit order, STOCK_MARKET_ORDER=market order 
		//		STOCK_LIMIT_STOP_ORDER=limit stop order ,STOCK_STOP_LOSS_ORDER=stop loss order
		TDAStringType		OrderType;

		TDAStringType		OrderDate;							// �µ�����
																// Order date

		TDAStringType		OrderTime;							// �µ�ʱ��
																// Order time

		TDAStringType		ErrorCode;							// �������
																// Error code
		// ����״̬:
		//		STOCK_ORDER_STATE1=������  STOCK_ORDER_STATE2=���Ŷӣ�  STOCK_ORDER_STATE3=���ֳɽ�
		//		STOCK_ORDER_STATE4=��ȫ�ɽ���STOCK_ORDER_STATE5=�ѳ��൥��STOCK_ORDER_STATE6=�ѳ���
		//		STOCK_ORDER_STATE7=ָ��ʧ�ܣ�STOCK_ORDER_STATE8=���ͳ���  STOCK_ORDER_STATE9=�����ģ�
		//		STOCK_ORDER_STATEA=������
		// Order state:
		//		STOCK_ORDER_STATE1=requested 
		//		STOCK_ORDER_STATE2=be queuing  
		//		STOCK_ORDER_STATE3=some orders were closed  
		//		STOCK_ORDER_STATE4=full order  
		//		STOCK_ORDER_STATE5=the remaining order has been cancelled
		//		STOCK_ORDER_STATE6=order has been cancelled  
		//		STOCK_ORDER_STATE7=command failure 
		//		STOCK_ORDER_STATE8=the command is waiting to be sent 
		//		STOCK_ORDER_STATE9=the command is waiting to be changed 
		//		STOCK_ORDER_STATEA=the command is waiting to be cancelled
		TDAStringType		OrderState;

		TDAStringType		TriggerPrice;						// �����۸�
																// Trigger price
		// ��Ч����:
		//		STOCKE_TDY_TIF=������Ч, STOCK_GTC_TIF=������Ч��GTC����STOCK_OPG_TIF=OPG,STOCK_IOC_TIF4=IOC
		//		STOCK_FOK_TIF=FOK��STOCK_GTD_TIF=GTD��STOCK_ATC_TIF=ATC��STOCK_FAK_TIF=FAK
		// Order time in force:
		//		STOCK_TDY_TIF=the day only,STOCK_GTC_TIF=GTC,STOCK_OPG_TIF=OPG,STOCK_IOC_TIF=IOC
		//		STOCK_FOK_TIF=FOK,STOCK_GTD_TIF=GTD,STOCK_ATC_TIF=ATC,STOCK_FAK_TIF=FAK	
		TDAStringType		TIF;

		// ���ֻ���ƽ��:
			// STOCK_OPEN_POS_FLAG=����,STOCK_OPEN_POS_FLAG=ƽ��
		// open/close position flag:
			// STOCK_OPEN_POS_FLAG=open position,STOCK_CLOSE_POS_FLAG=close position
		TDAStringType		OpenCloseFlag;

		TDAStringType		StrategyId;							// ����ID 20130726 add
																// Strategy id	

		TDAStringType		MaxShow;							// ��ɽ����ʾ���������
																// Max show quantity for ICE order

		TDAStringType		MinQty;								// FAK/FOK��������С�ɽ��� 
																// Min filled quantity expected by FAK/FOK order

		TDAStringType		ExchangeTime;						// ����������ʱ��
																// Exchange time

	};
	// �޸Ķ�������
	struct CStockReqOrderModifyField
	{
		TDAStringType		SystemNo;							// ϵͳ���
																// System No

		TDAStringType		UserId;								// �û���ʶ
																// User id

		TDAStringType		LocalNo;							// API�û��ĳ���ָ���ı��ض������
																// Order ID assigned by API user program

		TDAStringType		AccountNo;							// �ʽ��˺�
																// Account No

		TDAStringType		OrderNo;							// ������
																// The order number given by the exchange system ,LocalNo:SystemNo:OrderNo,these three are one-to-one relationships

		TDAStringType		ExchangeCode;						// ����������
																// Exchange code

		TDAStringType		ContractCode;						// ��Լ����
																// Contract code

		// ������:		STOCK_BID=��,  STOCK_ASK=��
		// Bid or ask:		STOCK_BID=bid, STOCK_ASK=ask
		TDAStringType		BidAskFlag;

		TDAStringType		OrderQty;							// �������� 
																// Order quantity

		TDAStringType		OrderPrice;							// �µ��۸�
																// Order price

		TDAStringType		ModifyQty;							// �ĵ��� 
																// Modify quantity

		TDAStringType		ModifyPrice;						// �ĵ��۸�
																// Modify price

		// �������ͣ�
		//		STOCK_LIMIT_ORDER=�޼۵�, STOCK_MARKET_ORDER=�м۵�
		//		STOCK_LIMIT_STOP_ORDER=�޼�ֹ��STOCK_STOP_LOSS_ORDER=ֹ��	
		// Order type:
		//		STOCK_LIMIT_ORDER=limit order, STOCK_MARKET_ORDER=market order 
		//		STOCK_LIMIT_STOP_ORDER=limit stop order ,STOCK_STOP_LOSS_ORDER=stop loss order
		TDAStringType		OrderType;

		TDAStringType		TriggerPrice;						// �����۸�
																// Trigger price

		TDAStringType		ModifyTriggerPrice;					// �ĵ������۸�
																// Modify trigger price

		// ��Ч����:
		//		STOCKE_TDY_TIF=������Ч, STOCK_GTC_TIF=������Ч��GTC����STOCK_OPG_TIF=OPG,STOCK_IOC_TIF4=IOC
		//		STOCK_FOK_TIF=FOK��STOCK_GTD_TIF=GTD��STOCK_ATC_TIF=ATC��STOCK_FAK_TIF=FAK
		// Order time in force:
		//		STOCK_TDY_TIF=the day only,STOCK_GTC_TIF=GTC,STOCK_OPG_TIF=OPG,STOCK_IOC_TIF=IOC
		//		STOCK_FOK_TIF=FOK,STOCK_GTD_TIF=GTD,STOCK_ATC_TIF=ATC,STOCK_FAK_TIF=FAK	
		TDAStringType		TIF;

		TDAStringType		ErrorDescription;					// ������Ϣ
																// Error description
	};
	// �޸Ķ�������
	typedef CStockRspOrderInsertField CStockRspOrderModifyField;
	// ��������
	struct CStockReqOrderCancelField
	{
		TDAStringType		UserId;								// �û���ʶ
																// User id

		TDAStringType		LocalNo;							// API�û��ĳ���ָ���ı��ض������
																// Order ID assigned by API user program

		TDAStringType		AccountNo;							// �ʽ��˺�
																// Account No

		TDAStringType		SystemNo;							// ϵͳ���
																// System No

		TDAStringType		OrderNo;							// ������
																// The order number given by the exchange system ,LocalNo:SystemNo:OrderNo,these three are one-to-one relationships

		TDAStringType		ExchangeCode;						// ����������
																// Exchange code

		TDAStringType		ContractCode;						// ��Լ����
																// Contract code

		// ������:		STOCK_BID=��,  STOCK_ASK=��
		// Bid or ask:		STOCK_BID=bid, STOCK_ASK=ask
		TDAStringType		BidAskFlag;

		TDAStringType		OrderQty;							// �µ���
																// Order quantity

		TDAStringType		OrderPrice;							// �µ��۸�
																// Order price

		// �������ͣ�
		//		STOCK_LIMIT_ORDER=�޼۵�, STOCK_MARKET_ORDER=�м۵�
		//		STOCK_LIMIT_STOP_ORDER=�޼�ֹ��STOCK_STOP_LOSS_ORDER=ֹ��	
		// Order type:
		//		STOCK_LIMIT_ORDER=limit order, STOCK_MARKET_ORDER=market order 
		//		STOCK_LIMIT_STOP_ORDER=limit stop order ,STOCK_STOP_LOSS_ORDER=stop loss order
		TDAStringType		OrderType;

		TDAStringType		ErrorDescription;					// ������Ϣ
																// Error message description
	};
	// ��������
	struct CStockRspOrderCancelField
	{
		TDAStringType		UserId;								// �û���ʶ
																// User id

		TDAStringType		AccountNo;							// �ʽ��˺�
																// Account No

		TDAStringType		SystemNo;							// ϵͳ���
																// System No

		TDAStringType		LocalNo;							// ���ر�� API�û��ĳ���ָ���ı��ض������
																// Order ID assigned by API user program

		TDAStringType		OrderNo;							// ������ ������ϵͳ�����Ķ����ţ�LocalNo:SystemNo:OrderNo��һ��һ��һ�Ĺ�ϵ
																// The order number given by the exchange system ,LocalNo:SystemNo:OrderNo,these three are one-to-one relationships

		TDAStringType		CancelNo;							// ������
																// Cancel order No

		TDAStringType		ExchangeCode;						// ����������
																// Exchange code

		TDAStringType		ContractCode;						// ��Լ����
																// Contract code

		// ������:		STOCK_BID=��,  STOCK_ASK=��
		// Bid or ask:		STOCK_BID=bid, STOCK_ASK=ask
		TDAStringType		BidAskFlag;

		TDAStringType		OrderQty;							// �µ���
																// Order quantity

		TDAStringType		OrderPrice;							// �µ��۸�
																// Order price

		TDAStringType		FilledQty;							// �ѳɽ���
																// Filled quantity (The number of orders has been completed)

		TDAStringType		CancelledQty;						// �ѳ�����
																// Cancelled quantity

		// �������ͣ�
		//		STOCK_LIMIT_ORDER=�޼۵�, STOCK_MARKET_ORDER=�м۵�
		//		STOCK_LIMIT_STOP_ORDER=�޼�ֹ��STOCK_STOP_LOSS_ORDER=ֹ��	
		// Order type:
		//		STOCK_LIMIT_ORDER=limit order, STOCK_MARKET_ORDER=market order 
		//		STOCK_LIMIT_STOP_ORDER=limit stop order ,STOCK_STOP_LOSS_ORDER=stop loss order
		TDAStringType		OrderType;

		TDAStringType		CancelledDate;						// ��������
																// Cancelled date

		TDAStringType		CancelledTime;						// ����ʱ��
																// Cancelled time

		TDAStringType		ErrorCode;							// ������� -----��Ϊ��Ŷ���״̬��1��������2�����Ŷӣ�3�����ֳɽ���4����ȫ�ɽ���5���ѳ��൥��6���ѳ�����7��ָ��ʧ�ܣ�8�����ͳ���9�������ģ�10����������
																// Error code
	};
	// �޸���������
	struct CStockReqPasswordUpdateField
	{
		TDAStringType		UserId;								// �û�����
		TDAStringType		OldPassword;						// �û�ԭ����
		TDAStringType		NewPassword;						// �û�������
		TDAStringType		ErrorDescription;					// ������Ϣ
	};
	// �޸����뷵��
	struct CStockRspPasswordUpdateField
	{
		TDAStringType		UserId;								// �û�����
		TDAStringType		OldPassword;						// �û�ԭ����
		TDAStringType		NewPassword;						// �û�������
	};
	// ��ѯ��������
	struct CStockQryOrderField
	{
		TDAStringType		UserId;								// �û���ʶ
																// User id

		TDAStringType		AccountNo;							// �ʽ��˺�
																// Account No

		// �Ƿ�ģ���û���STOCK_IS_SIMULATED_USER=�ǣ�STOCK_IS_NOT_SIMULATED_USER or other������
		//Simulated user:
		//		STOCK_IS_SIMULATED_USER=is a simulated user
		//		STOCK_IS_NOT_SIMULATED_USER or other = is not a simulated user
		TDAStringType		IsSimulation;

		TDAStringType		OrderNo;							// ȡ��ָ���������Ժ�Ķ���
																// Obtain a subsequent order with the specified order number

		TDAStringType		OrderDateTime;						// ȡ��ָ������ʱ���Ժ�Ķ�������ʽ��yyyy-MM-dd hh:mm:ss��
																// Obtain orders after the specified order time��format��yyyy-MM-dd hh:mm:ss��

		TDAStringType		ErrorDescription;					// ������Ϣ
																// Error description
	};
	// ��ѯ��������
	struct CStockRspOrderField
	{
		TDAStringType		UserId;								// �û���ʶ
																// User id

		TDAStringType		AccountNo;							// �ʽ��˺�
																// Account No

		TDAStringType		SystemNo;							// ϵͳ���
																// System No

		TDAStringType		LocalNo;							// API�û��ĳ���ָ���ı��ض������
																// Order ID assigned by API user program

		TDAStringType		OrderNo;							// ������ ������ϵͳ�����Ķ����ţ�LocalNo:SystemNo:OrderNo��һ��һ��һ�Ĺ�ϵ
																// The order number given by the exchange system ,LocalNo:SystemNo:OrderNo,these three are one-to-one relationships

		TDAStringType		ExchangeCode;						// ����������
																// Exchange code

		TDAStringType		ContractCode;						// ��Լ����
																// Contract code

		// ������:		STOCK_BID=��,  STOCK_ASK=��
		// Bid or ask:		STOCK_BID=bid, STOCK_ASK=ask
		TDAStringType		BidAskFlag;

		TDAStringType		OrderQty;							// �µ���
																// Order quantity

		TDAStringType		OrderPrice;							// �µ��۸�
																// Order price

		TDAStringType		FilledQty;							// �ѳɽ���
																// Filled quantity (The number of orders has been completed)

		TDAStringType		FilledPrice;						// �ɽ�����
																// Filled price(Average transaction price)

		// �������ͣ�
		//		STOCK_LIMIT_ORDER=�޼۵�, STOCK_MARKET_ORDER=�м۵�
		//		STOCK_LIMIT_STOP_ORDER=�޼�ֹ��STOCK_STOP_LOSS_ORDER=ֹ��	
		// Order type:
		//		STOCK_LIMIT_ORDER=limit order, STOCK_MARKET_ORDER=market order 
		//		STOCK_LIMIT_STOP_ORDER=limit stop order ,STOCK_STOP_LOSS_ORDER=stop loss order
		TDAStringType		OrderType;

		TDAStringType		OrderDate;							// �µ�����
																// Order date

		TDAStringType		OrderTime;							// �µ�ʱ��
																// Order time

		TDAStringType		ErrorCode;							// �������
																// Error code

		// ����״̬:
		//		STOCK_ORDER_STATE1=������  STOCK_ORDER_STATE2=���Ŷӣ�  STOCK_ORDER_STATE3=���ֳɽ�
		//		STOCK_ORDER_STATE4=��ȫ�ɽ���STOCK_ORDER_STATE5=�ѳ��൥��STOCK_ORDER_STATE6=�ѳ���
		//		STOCK_ORDER_STATE7=ָ��ʧ�ܣ�STOCK_ORDER_STATE8=���ͳ���  STOCK_ORDER_STATE9=�����ģ�
		//		STOCK_ORDER_STATEA=������
		// Order state:
		//		STOCK_ORDER_STATE1=requested 
		//		STOCK_ORDER_STATE2=be queuing  
		//		STOCK_ORDER_STATE3=some orders were closed  
		//		STOCK_ORDER_STATE4=full order  
		//		STOCK_ORDER_STATE5=the remaining order has been cancelled
		//		STOCK_ORDER_STATE6=order has been cancelled  
		//		STOCK_ORDER_STATE7=command failure 
		//		STOCK_ORDER_STATE8=the command is waiting to be sent 
		//		STOCK_ORDER_STATE9=the command is waiting to be changed 
		//		STOCK_ORDER_STATEA=the command is waiting to be cancelled
		TDAStringType		OrderState;

		TDAStringType		CancelUserId;						// �������û���ʶ
																// User id of cancel order

		TDAStringType		TriggerPrice;						// �����۸�
																// Trigger price

		// ��Ч����:
		//		STOCK_TDY_TIF=������Ч, STOCK_GTC_TIF=������Ч��GTC����STOCK_OPG_TIF=OPG,STOCK_IOC_TIF4=IOC
		//		STOCK_FOK_TIF=FOK��STOCK_GTD_TIF=GTD��STOCK_ATC_TIF=ATC��STOCK_FAK_TIF=FAK
		// Order time in force:
		//		STOCK_TDY_TIF=the day only,STOCK_GTC_TIF=GTC,STOCK_OPG_TIF=OPG,STOCK_IOC_TIF=IOC
		//		STOCK_FOK_TIF=FOK,STOCK_GTD_TIF=GTD,STOCK_ATC_TIF=ATC,STOCK_FAK_TIF=FAK		
		TDAStringType		TIF;

		// ���ֻ���ƽ��:
		//		STOCK_OPEN_POS_FLAG=����,STOCK_OPEN_POS_FLAG=ƽ��
		// open/close position flag:
		//		STOCK_OPEN_POS_FLAG=open position,STOCK_CLOSE_POS_FLAG=close position
		TDAStringType		OpenCloseFlag;

		TDAStringType		StrategyId;							// ����ID 20130726 add
																// Strategy id

		TDAStringType		MaxShow;							// ��ɽ����ʾ���������
																// Max show quantity for ICE order

		TDAStringType		MinQty;								// FAK/FOK��������С�ɽ��� 
																// Min filled quantity expected by FAK/FOK order

		TDAStringType		ExchangeTime;						// ����������ʱ��
																// Exchange time

		TDAStringType		CancelTime;							// ����ʱ��
																// Cancel time
	};
	// ��ѯ�ɽ�����
	struct CStockQryTradeField
	{
		TDAStringType		UserId;								// �û�		
		TDAStringType		ErrorDescription;					// ������Ϣ
		TDAStringType		lastFilledNo;						//��ѯ�����һ���û��ɽ��� update 2020.04.30 ywh
	};
	// ��ѯ�ɽ�����
	struct CStockRspTradeField
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
		TDAStringType		ExchangeTime;						// ����������ʱ��(yyyy-MM-dd hh24:mm:ss) 20151214 add
		TDAStringType		SubClientNo;						// ���˻���
		TDAStringType		FillBrokerList;						// �۹��У��ɽ���ʱ����Եõ��ɽ����������ľ����̴���
		TDAStringType		ErrorDescription;					// ������Ϣ
	};
	// ��ѯ��Լ����
	struct CStockQryInstrumentField
	{
		TDAIntType			PageIndex;							// ��ѯ������,ÿ�η��ص�����
		TDAStringType       ExchangeNo;							// ���������룬�����дֵ����ѯһ���������ĺ�Լ
		TDAStringType		ModifyDay;							// ��Լ��������,������ѯ ��ʽ("20200101")
		TDAStringType		ErrorDescription;					// ������Ϣ
		
	};
	// ��ѯ��Լ����
	struct CStockRspInstrumentField
	{
		TDAStringType		ExchangeNo;							// ��������� 
		TDAStringType		ExchangeName;						// ���������� 
		TDAStringType		CommodityNo;						// ��ԼNO
		TDAStringType		CommodityName;						// ��Ʒ�� 
		TDAStringType		CommodityType;						// ��Ʒ��� 
		TDAStringType		CurrencyNo;							// ���ұ�� 
		TDAStringType		CurrencyName;						// �������� 
		TDADoubleType		ProductDot;							// ��ֵ��һ����С����ļ�ֵ��   
		TDADoubleType		UpperTick;							// ��С�䶯��λ 
		TDADoubleType		SettlePrice;						// ���ս���� 
		TDAStringType		TradeMonth;							// ������ (yyyyMM)/������ (yyyyMMdd)
		TDAIntType			DotNum;								// ����С����λ��
		TDAIntType			LowerTick;							// ���׵�λ
		TDAIntType			DotNumCarry;						// ����С����λ��
		TDADoubleType		UpperTickCarry;						// ������С�䶯��λ
		TDAStringType		FirstNoticeDay;						// �״�֪ͨ�� (yyyyMMdd)
		TDADoubleType		FreezenPercent;						// ���ᱣ֤��ٷֱ� 
		TDADoubleType		FreezenMoney;						// ���ᱣ֤��̶�ֵ 
		TDADoubleType		FeeMoney;							// �̶������� 
		TDADoubleType		FeePercent;							// �ٷֱ������� 
		TDADoubleType		PriceStrike;						// �ֻ���Ʒ������ 
		TDADoubleType		ProductDotStrike;					// �ֻ���Ʒ��ֵ  
		TDADoubleType		UpperTickStrike;					// �ֻ���Ʒ��С�䶯��λ 
		TDAStringType		LastTradeDay;						// ������� (yyyyMMdd)(�ڻ�ר��)
		TDAStringType		LastUpdateDay;						// �������� (yyyyMMdd)(�ڻ�ר��)
		TDADoubleType		CriticalPrice;						// ��Ȩ�ٽ�۸� (�ڻ�ר��)
		TDADoubleType		CriticalMinChangedPrice;			// ��Ȩ�ٽ�۸����µ���С���� (�ڻ�ר��)
		TDAStringType		ExchangeSub;						// ʵ�ʽ�����(CMEϸ�ֳ�3��������:CME,CME_COMEX,CME_NYMEX)(�ڻ�ר��)
		TDAStringType		OptionType;							// ��Ȩ����(R�����ǣ�F������)(�ڻ�ר��)
		TDAStringType		OptionMonth;						// ��Ȩ����(yyyyMM)(�ڻ�ר��)
		TDAStringType		OptionStrikePrice;					// ��Ȩִ�м۸�(�ڻ�ר��)
		TDAStringType		OptionCommodityNo;					// ��Ȩ��Ӧ�ڻ���Ʒ���(�ڻ�ר��)
		TDAStringType		OptionContractNo;					// ��Ȩ��Ӧ�ڻ���Լ���(�ڻ�ר��)
		TDAStringType		MortgagePercent;					// ���Ҽ�ֵ�ٷֱ�
		TDAStringType		UpperTickCode;						// ��С�䶯��λ����
		TDAStringType		LotSize;							// ��С����
		TDAStringType		FlatTime;							// ƽ��ʱ���־(����T+1��0����T+0�����Ե�������ƽ�֣�1����T+1�������������ƽ�֣�N����T+N)
		TDAStringType		CommodityFNameEN;					// ��Ʒ����Ӣ�ģ�
		TDAStringType		CanSell;							// �Ƿ�֧�����գ�0��գ������ԣ�1�����ԣ�
		TDADoubleType		SellRate;							// ����ʱ�İ������������0.5��
		TDADoubleType		SellMax;							// ���ճֲ����޶�
		TDADoubleType		StrikeRate;							// ���ɱ��ʣ���ʾһ������ţ���^���൱�ڶ�������
		TDADoubleType		StrikePrice;						// ��ʹ��
		TDADoubleType		ReceivePrice;						// �ջؼ�
		TDAStringType		ExpireDate;							// �����գ�yyyy-MM-dd��
		TDADoubleType		SellRateKeep;						// ����ʱ��ά�ְ������������0.5��
		TDAStringType		StrikeCommodityNo;					// ����ţ��֤��Ӧ���ɱ��
		TDAStringType		CallPutFlag;						// ����ţ��֤���ǵ���־(C:�ǣ�P:��)
		TDAStringType		Publisher;							// ����ţ��֤�ķ�����
	};
	// ��ѯ����������
	struct CStockQryExchangeField
	{
		TDAStringType		ProductGroupID;
		TDAStringType		ErrorDescription;					// ������Ϣ
	};
	// ��ѯ����������
	struct CStockRspExchangeField
	{
		TDAStringType		ExchangeNo;							// ���������
		TDAStringType		ExchangeName;						// ����������
		TDAStringType		SettleType;							// ���������ͣ�HK���۹ɣ�US�����ɣ�
		TDAStringType 		NameEN;								// ���������ƣ�Ӣ�ģ�
	};
	// ��ѯ�ʽ�����
	struct CStockQryCapitalField
	{
		TDACharType			Unused;								// ��ʹ��	
		TDAStringType		ErrorDescription;					// ������Ϣ
	};
	// ��ѯ�ʽ𷵻�
	// Query fund return struct
	struct CStockRspCapitalField
	{
		TDAStringType		UserId;								// �û���ʶ
																// User id

		TDAStringType		Deposit;							// ���
																// Deposit

		TDAStringType		Withdraw;							// ����
																// Withdraw

		TDAStringType		TodayTradableFund;					// �ɣ�����ã��£����տ����ڽ��׵��ʽ���
																// Today tradable fund amount

		TDAStringType		TodayInitialBalance;				// �ɣ����棻�£������ڳ�Ȩ��
																// today inital balance

		TDAStringType		TodayRealtimeBalance;				// �ɣ���Ȩ�棻�£�����ʵʱ����Ȩ��
																// today realtime floating balance with Profit&Loss

		TDAStringType		FrozenFund;							// �����ʽ�
																// Frozen fund

		TDAStringType		Commission;							// Ӷ��
																// Commission

		TDAStringType		InitialMargin;						// �ɣ���֤���£���ʼ��֤��
																// Initial margin

		TDAStringType		YdTradableFund;						// �ɣ�����ã��£����տ����ڽ��׵��ʽ���
																// Yesterday tradable fund amount

		TDAStringType		YdInitialBalance;					// �ɣ����棻�£������ڳ�Ȩ��
																// Yesterday inital balance

		TDAStringType		YdFinalBalance;						// �ɣ���Ȩ�棻�£�������ĩȨ��
																// Yesterday final balance with Profit&Loss

		TDAStringType		ProfitLoss;							// ����ӯ��
																// Profit and loss

		TDAStringType		CurrencyNo;							// ���ֱ�� 
																// Currency No

		TDAMoneyType		CurrencyRate;						// ����������Ļ���
																//  Currency rate

		TDAMoneyType		LMEUnexpiredPL;						// LMEδ����ƽӯ
																// LME unexpired profit&losss

		TDAMoneyType		LMEUnaccountPL;						// LMEδ��ƽӯ
																// LME unaccounting profit&losss

		TDAMoneyType		MaintenanceMargin;					// ά�ֱ�֤��
																// Maintenance margin

		TDAMoneyType		Premium;							// ��ȨȨ����
																// Premium for options

		TDAMoneyType		CreditAmount;						// ���ζ��
																// Credit amount

		TDAMoneyType		IntialFund;							// ��ʼ�ʽ�
																// Intial fund

		TDAStringType		FundAccountNo;						// �ʽ��ʺ� 
																// Fund account No

		TDAMoneyType		MortgageInMoney;					// ���Ҽ�ֵ 20150610 added for �۹�
																// Mortgage in money(add for HK stock)

		TDAMoneyType		MarginLimit;						// �Iչ���޶�� 20150727 added for �۹�
																// Margin limit(add for Hk stock)

		TDAMoneyType		BorrowInMoney;						// �����ֵ 20150727 added for �۹�
																// Borrow in money

		TDAMoneyType		T1DeliveryMoney;					// T1�ս�����ʽ����븺��
																// T1 day delivery of funds, positive in negative out

		TDAMoneyType		T2DeliveryMoney;					// T2 �ս�����ʽ����븺��
																// T2 day delivery of funds, positive in negative out

		TDAMoneyType		T3DeliveryMoney;					// T3 �ս�����ʽ����븺��
																// T3 day delivery of funds, positive in negative out

		TDAMoneyType		TNDeliveryMoney;					// TN �ս�����ʽ����븺��
																// TN day delivery of funds, positive in negative out

		TDAMoneyType		TradeLimit;							// �����޶�
																// Trade limit

		TDAMoneyType		CanCashOutMoneyAmount;				// ��ȡ�ʽ�
																// Can cash out money amount

		TDAMoneyType		DepositInterest;					// �´����Ϣ
																// Monthly deposit interest

		TDAMoneyType		LoanInterest;						// ��Ƿ����Ϣ
																// Monthly loan interest

		TDAMoneyType		CrossCurrencyMaxMoneyAmt;			// ���г��ʽ��޶�
																// Cross-market capital limits

		TDAMoneyType		SellShortFrozenMoney;				// ���ն����ʽ�
																// Short sale frozen funds

		TDAMoneyType		SellShortInterest;					// ������Ϣ
																// Short sale interest

		TDAMoneyType		ShortPosAddtionalMargin;			// �貹����
																// Short position addtional margin

		TDAStringType		ErrorDescription;					// ������Ϣ
																// Error description
	};
	// ��ѯ�ֲ�����
	struct CStockQryPositionField
	{
		TDAStringType		ErrorDescription;					// ������Ϣ
	};
	// ��ѯ�ֲַ���
	struct CStockRspPositionField
	{
		TDAStringType		ClientNo;							// �û���ʶ
																// Client No

		TDAStringType		ExchangeCode;						// ����������
																// Exchange code

		TDAStringType		ProductCode;						// ֤ȯ����
																// Product code
		// �ֲַ���:
		// STOCK_POSITION_FLAG_LONG=����STOCK_POSITION_FLAG_SHORT=������
		// The position direction flag:
		// STOCK_POSITION_FLAG_LONG=long position,STOCK_POSITION_FLAG_SHORT=short position
		TDAStringType		LongShortPosFlag;

		TDADoubleType		PosCostPrice;						// �ֲֳɱ���
																// Position at cost

		TDAIntType			CanSellShares;						// ��������
																// Can sell shares

		TDAIntType			TodayBuyShares;						// ��������
																// Today buy shares

		TDAIntType			FrosenShares;						// ��������
																// Frosen shares

		TDADoubleType		TotalBuyMoney;						// ���������������ܺ�
																// Total amount of purchase during the holding period

		TDADoubleType		TotalSellMoney;						// ����������������ܺ�
																// Total amount sold during the holding period

		TDAIntType			TotalBuyShares;						// �������������ܹ���
																// Total number of shares bought during the holding period

		TDAIntType			TotalSellShares;					// �������������ܹ���
																// Total number of shares sold during the holding period

		TDAStringType		FirstPosDate;						// �״ο�������(yyyy-MM-dd)
																// Date of first opening(yyyy-MM-dd)

		TDADoubleType		ClosePosPL;							// ƽ��ӯ��
																// Closing position profit

		TDAIntType			T1DeliveryShares;					// T1�ս�����������븺��
																// T1 day delivery of shares, positive in negative out

		TDAIntType			T2DeliveryShares;					// T2�ս�����������븺��
																// T2 day delivery of shares, positive in negative out

		TDAIntType			T3DeliveryShares;					// T3�ս�����������븺��
																// T3 day delivery of shares, positive in negative out

		TDAIntType			NotDeliveryShares;					// δ�������=T1DeliveryShares+T2DeliveryShares+T3DeliveryShares
																// Number of outstanding shares=T1DeliveryShares+T2DeliveryShares+T3DeliveryShares

		TDAIntType			DeliveredShares;					// �ѽ������
																// Number of shares delivered

		TDAIntType			SellShortShares;					// ���չ���
																// Short the number of shares

		TDADoubleType		SellShortMoney;						// ���ն����ʽ�
																// Short sale frozen funds

		TDADoubleType		SSPosAvgCostPrice;					// ���ղ�λ�Ŀ��־���
																// The average opening price of a short position
	};
	// ��ѯ��������
	struct CStockQryTickField
	{
		TDACharType			Unused;								// ��ʹ��
		TDAStringType		ErrorDescription;					// ������Ϣ
	};
	// ��ѯ���㷵��
	struct CStockRspTickField
	{
		TDAStringType		UpperTickCode;						// ��С�䶯��λ����
		TDAStringType		PriceFrom;							// ��С�䶯��λ��ʼ����۸�
		TDAStringType		UpperTick;							// ������С�䶯��λ
		TDAStringType		ProductDot;							// ��С�䶯��λ��Ӧ�ĵ�ֵ
		TDAStringType		DotNum;								// ����С��λ��
		TDAStringType		LowerTick;							// ���۵�λ
	};
	// ��ѯ��������
	struct CStockQryCurrencyField
	{
		TDACharType			Unused;								// ��ʹ��
		TDAStringType		ErrorDescription;					// ������Ϣ
	};
	// ��ѯ���ҷ���
	struct CStockRspCurrencyField
	{
		TDAStringType		CurrencyNo;							// ���ұ��
		TDAIntType			IsBase;								// ���һ��ұ��
		TDADoubleType		ChangeRate;							// ����ҵĻ������
		TDAStringType		CurrencyName;						// ��������
		TDAStringType		CurrencyNameEN;						// �������ƣ�Ӣ�ģ�
	};
	// ��ѯ�汾����
	struct CStockQryVersionField
	{
		TDAStringType		UserId;								// �û���ʶ
		TDAStringType		UserPwd;							// �û�����
		TDAStringType		ErrorDescription;					// ������Ϣ
	};
	// ��ѯ�汾����
	struct CStockRspVersionField
	{
		TDAStringType		Version;							// �汾��
		TDAStringType		MustUpdate;							// �Ƿ������µ��°汾��������ʹ�ã�0�����Բ����£�1��������£�
		TDAStringType		MustVersion;						// ����Ҫ�����İ汾��
		TDAStringType		VersionContent_CN;					// �汾��������
		TDAStringType		VersionContent_US;					// �汾����Ӣ��
	};
	//-------------------------------------------------------------------------
	// ���Ͷ����仯
	struct CStockRtnOrderField
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
	struct CStockRtnCapitalField
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
	typedef CStockRspPositionField CStockRtnPositionField;
	// ���ͳɽ�����
	typedef CStockRspTradeField	CStockRtnTradeField;
	//-------------------------------------------------------------------------
	// ��ȡ����
	struct CStockReqGetQuestionField
	{
		TDAIntType			Unused;								// �û��ʺ�
		TDAStringType		ErrorDescription;					// ������Ϣ
	};
	// ��ȡ���ⷵ��
	struct CStockRspQuestionField
	{
		TDAStringType		QuestionType;						// ��������	0�������ڻ���1�����ʹ�Ʊ
		TDAStringType		QuestionId;							// ������
		TDAStringType		QuestionCN;							// ���⣨���ģ�
		TDAStringType		QuestionEN;							// ���⣨Ӣ�ģ�
	};
	// ��ȫ��֤����
	struct CStockReqSafeVerifyField
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
	struct CStockReqSetVerifyQAField
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
	struct CStockReqVerifyCodeField
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

}