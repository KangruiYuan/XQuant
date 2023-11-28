/////////////////////////////////////////////////////////////////////////
/// DriectAccess Trade Engine
/// Copyright (C) Shanghai DirectAccess Technology Co., Ltd.
/// Last Modify 2019/3/18
/// Define Future Struct
/// Author (c) Wang Jian Quan (Franklin)
/////////////////////////////////////////////////////////////////////////

#pragma once

#include "DADataType.h"

namespace Directaccess {


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
// new order request struct
struct CFutureReqOrderInsertField
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

	TDAStringType		BidAskFlag;							// ������: DERIVATIVE_BID=��,DERIVATIVE_ASK=��	
															// Bid or ask: DERIVATIVE_BID=bid,DERIVATIVE_ASK=ask

	TDAStringType		OpenCloseFlag;						// ���ֻ���ƽ��: DERIVATIVE_OPEN_POS_FLAG=����,DERIVATIVE_CLOSE_POS_FLAG=ƽ��
															// Open/close position flag: DERIVATIVE_OPEN_POS_FLAG=open position	,DERIVATIVE_CLOSE_POS_FLAG=close position

	TDAStringType		OrderQty;							// ��������
															// Order quantity

	TDAStringType		OrderPrice;							// �µ��۸�	
															// Order price

	// �������ͣ�
	//		DERIVATIVE_LIMIT_ORDER=�޼۵�, DERIVATIVE_MARKET_ORDER=�м۵�
	//		DERIVATIVE_LIMIT_STOP_ORDER=�޼�ֹ��DERIVATIVE_STOP_LOSS_ORDER=ֹ��	
	// order type:
	//		DERIVATIVE_LIMIT_ORDER=limit order, DERIVATIVE_MARKET_ORDER=market order 
	//		DERIVATIVE_LIMIT_STOP_ORDER=limit stop order ,DERIVATIVE_STOP_LOSS_ORDER=stop loss order
	TDAStringType		OrderType;

	TDAStringType		TriggerPrice;						// �����۸�
															// Trigger price
	// ��Ч����:
	//		DERIVATIVE_TDY_TIF=������Ч, DERIVATIVE_GTC_TIF=������Ч��GTC����DERIVATIVE_OPG_TIF=OPG,DERIVATIVE_IOC_TIF4=IOC
	//		DERIVATIVE_FOK_TIF=FOK��DERIVATIVE_GTD_TIF=GTD��DERIVATIVE_ATC_TIF=ATC��DERIVATIVE_FAK_TIF=FAK
	// order time in force:
	//		DERIVATIVE_TDY_TIF=the day only,DERIVATIVE_GTC_TIF=GTC,DERIVATIVE_OPG_TIF=OPG,DERIVATIVE_IOC_TIF=IOC
	//		DERIVATIVE_FOK_TIF=FOK,DERIVATIVE_GTD_TIF=GTD,DERIVATIVE_ATC_TIF=ATC,DERIVATIVE_FAK_TIF=FAK	
	TDAStringType		TIF;							
	
	TDAStringType		StrategyId;							// ����ID 20130726 add
															// Strategy id

	TDAStringType		MaxShow;							// ��ɽ����ʾ���������
															// Max show quantity for ICE order													

	TDAStringType		MinQty;								// FAK/FOK��������С�ɽ���
															// Min filled quantity expected by FAK/FOK order

	TDAStringType		Tag50;								// �µ���ID(CME�������ض�)
															//  Order placer's id (CME exchange specific)

	TDAStringType		ErrorDescription;					// ������Ϣ
															// Error message description
	TDAIntType		    IsProgram;							// ���򻯵�(0)���˹���(1)	

	TDAStringType	    OrgOrderLocationID;					// ISO(3166-1)��׼�ж���Ĺ��Ҵ���
															// ISO(3166-1)identifier of the physical location

};
// ������������
struct CFutureRspOrderInsertField
{
	TDAStringType		UserId;								// �û���ʶ
															// User id
		
	TDAStringType		AccountNo;							// �ʽ��˺�
															// Account No														

	TDAStringType		SystemNo;							// ϵͳ���
															// System no	
		
	TDAStringType		LocalNo;							// ���ر�� API�û��ĳ���ָ���ı��ض������
															// Order ID assigned by API user program

	TDAStringType		OrderNo;							// ������ ������ϵͳ�����Ķ����ţ�LocalNo:SystemNo:OrderNo��һ��һ��һ�Ĺ�ϵ
															// The order number given by the exchange system ,LocalNo:SystemNo:OrderNo,these three are one-to-one relationships
																	
	TDAStringType		ExchangeCode;						// ����������
															// Exchange code														

	TDAStringType		ContractCode;						// ��Լ����
															// Contract code

	TDAStringType		BidAskFlag;							// ������: DERIVATIVE_BID=��,DERIVATIVE_ASK=��
															// Bid or ask: DERIVATIVE_BID=bid,DERIVATIVE_ASK=ask

	TDAStringType		OrderQty;							// ��������
															// Order quantity

	TDAStringType		OrderPrice;							// �µ��۸�
															// Order price
		
	// �������ͣ�
	//		DERIVATIVE_LIMIT_ORDER=�޼۵�, DERIVATIVE_MARKET_ORDER=�м۵�
	//		DERIVATIVE_LIMIT_STOP_ORDER=�޼�ֹ��DERIVATIVE_STOP_LOSS_ORDER=ֹ��	
	// Order type:
	//		DERIVATIVE_LIMIT_ORDER=limit order, DERIVATIVE_MARKET_ORDER=market order 
	//		DERIVATIVE_LIMIT_STOP_ORDER=limit stop order ,DERIVATIVE_STOP_LOSS_ORDER=stop loss order
	TDAStringType		OrderType;							
	
	TDAStringType		OrderDate;							// �µ�����
															// Order date

	TDAStringType		OrderTime;							// �µ�ʱ��
															// Order time

	TDAStringType		ErrorCode;							// �������
															// Error code

	// ����״̬:
	//		DERIVATIVE_ORDER_STATE1=������  DERIVATIVE_ORDER_STATE2=���Ŷӣ�  DERIVATIVE_ORDER_STATE3=���ֳɽ�
	//		DERIVATIVE_ORDER_STATE4=��ȫ�ɽ���DERIVATIVE_ORDER_STATE5=�ѳ��൥��DERIVATIVE_ORDER_STATE6=�ѳ���
	//		DERIVATIVE_ORDER_STATE7=ָ��ʧ�ܣ�DERIVATIVE_ORDER_STATE8=���ͳ���  DERIVATIVE_ORDER_STATE9=�����ģ�
	//		DERIVATIVE_ORDER_STATEA=������
	// Order state:
	//		DERIVATIVE_ORDER_STATE1=requested 
	//		DERIVATIVE_ORDER_STATE2=be queuing  
	//		DERIVATIVE_ORDER_STATE3=some orders were closed  
	//		DERIVATIVE_ORDER_STATE4=full order  
	//		DERIVATIVE_ORDER_STATE5=the remaining order has been cancelled
	//		DERIVATIVE_ORDER_STATE6=order has been cancelled  
	//		DERIVATIVE_ORDER_STATE7=command failure 
	//		DERIVATIVE_ORDER_STATE8=the command is waiting to be sent 
	//		DERIVATIVE_ORDER_STATE9=the command is waiting to be changed 
	//		DERIVATIVE_ORDER_STATEA=the command is waiting to be cancelled
	TDAStringType		OrderState;							
															
	
	TDAStringType		TriggerPrice;						// �����۸�
															// Trigger price
	// ��Ч����:
	//		DERIVATIVE_TDY_TIF=������Ч, DERIVATIVE_GTC_TIF=������Ч��GTC����DERIVATIVE_OPG_TIF=OPG,DERIVATIVE_IOC_TIF4=IOC
	//		DERIVATIVE_FOK_TIF=FOK��DERIVATIVE_GTD_TIF=GTD��DERIVATIVE_ATC_TIF=ATC��DERIVATIVE_FAK_TIF=FAK
	// Order time in force:
	//		DERIVATIVE_TDY_TIF=the day only,DERIVATIVE_GTC_TIF=GTC,DERIVATIVE_OPG_TIF=OPG,DERIVATIVE_IOC_TIF=IOC
	//		DERIVATIVE_FOK_TIF=FOK,DERIVATIVE_GTD_TIF=GTD,DERIVATIVE_ATC_TIF=ATC,DERIVATIVE_FAK_TIF=FAK
	TDAStringType		TIF;

	TDAStringType		OpenCloseFlag;						// ���ֻ���ƽ��: DERIVATIVE_OPEN_POS_FLAG=����,DERIVATIVE_CLOSE_POS_FLAG=ƽ��
															// Open/close position flag: DERIVATIVE_OPEN_POS_FLAG=open position	,DERIVATIVE_CLOSE_POS_FLAG=close position

	TDAStringType		StrategyId;							// ����ID		
															// Strategy id													
		
	TDAStringType		MaxShow;							// ��ɽ����ʾ���������
															// Max show quantity for ICE order

	TDAStringType		MinQty;								// FAK/FOK��������С�ɽ��� 
															// Min filled quantity expected by FAK/FOK order

	TDAStringType		ExchangeTime;						// ����������ʱ��
															// Exchange time
	
	TDAStringType		OrdSourceType;						// �ն�����(CME�������ض�)
															// Identify the type of terminal(CME exchange specific)

	TDAStringType		Tag50;								// �µ���ID(CME�������ض�)
															// Order placer's id (CME exchange specific)
};
// �޸Ķ�������
struct CFutureReqOrderModifyField
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

	TDAStringType		BidAskFlag;							// ������: DERIVATIVE_BID=��,DERIVATIVE_ASK=��
															// Bid or ask: DERIVATIVE_BID=bid,DERIVATIVE_ASK=ask

	TDAStringType		OrderQty;							// ��������
															// Order quantity

	TDAStringType		OrderPrice;							// �µ��۸�
															// Order price
	
	TDAStringType		ModifyQty;							// �ĵ��� 
															// Modify quantity

	TDAStringType		ModifyPrice;						// �ĵ��۸�
															// Modify price
	
	// �������ͣ�
	//		DERIVATIVE_LIMIT_ORDER=�޼۵�, DERIVATIVE_MARKET_ORDER=�м۵�
	//		DERIVATIVE_LIMIT_STOP_ORDER=�޼�ֹ��DERIVATIVE_STOP_LOSS_ORDER=ֹ��	
	// order type:
	//		DERIVATIVE_LIMIT_ORDER=limit order, DERIVATIVE_MARKET_ORDER=market order 
	//		DERIVATIVE_LIMIT_STOP_ORDER=limit stop order ,DERIVATIVE_STOP_LOSS_ORDER=stop loss order
	TDAStringType		OrderType;							
	
	TDAStringType		TriggerPrice;						// �����۸�
															// Trigger price

	TDAStringType		ModifyTriggerPrice;					// �ĵ������۸�
															// Modify trigger price
	// ��Ч����:
	//		DERIVATIVE_TDY_TIF=������Ч, DERIVATIVE_GTC_TIF=������Ч��GTC��	
	// order time in force:
	//		DERIVATIVE_TDY_TIF=the day only,DERIVATIVE_GTC_TIF=GTC
	TDAStringType		TIF;

	TDAStringType		Tag50;								// �µ���ID(CME�������ض�)
															// Order placer's id (CME exchange specific)

	TDAStringType		ErrorDescription;					// ������Ϣ
															// Error description
	TDAStringType	    OrgOrderLocationID;					// ISO(3166-1)��׼�ж���Ĺ��Ҵ���
															// ISO(3166-1)identifier of the physical location

};
// �޸Ķ�������
typedef CFutureRspOrderInsertField CFutureRspOrderModifyField;
// ��������
struct CFutureReqOrderCancelField
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

	TDAStringType		BidAskFlag;							// ������: DERIVATIVE_BID=��,DERIVATIVE_ASK=��
															// Bid or ask: DERIVATIVE_BID=bid,DERIVATIVE_ASK=ask

	TDAStringType		OrderQty;							// �µ���
															// Order quantity

	TDAStringType		OrderPrice;							// �µ��۸�
															// Order price
	
		// �������ͣ�
	//		DERIVATIVE_LIMIT_ORDER=�޼۵�, DERIVATIVE_MARKET_ORDER=�м۵�
	// Order type:
	//		DERIVATIVE_LIMIT_ORDER=limit order, DERIVATIVE_MARKET_ORDER=market order 
	TDAStringType		OrderType;							
		
	TDAStringType		Tag50;								// �µ���ID(CME�������ض�)
															//  Order placer's id (CME exchange specific)

	TDAStringType		ErrorDescription;					// ������Ϣ
															// Error message description

	TDAStringType	    OrgOrderLocationID;					// ISO(3166-1)��׼�ж���Ĺ��Ҵ���
															// ISO(3166-1)identifier of the physical location

};
// ��������
struct CFutureRspOrderCancelField
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

	TDAStringType		BidAskFlag;							// ������: DERIVATIVE_BID=��,DERIVATIVE_ASK=��
															// Bid or ask: DERIVATIVE_BID=bid,DERIVATIVE_ASK=ask

	TDAStringType		OrderQty;							// �µ���
															// Order quantity

	TDAStringType		OrderPrice;							// �µ��۸�
															// Order price

	TDAStringType		FilledQty;							// �ѳɽ���
															// Filled quantity (The number of orders has been completed)

	TDAStringType		CancelledQty;						// �ѳ�����
															// Cancelled quantity
	// �������ͣ�
	//		DERIVATIVE_LIMIT_ORDER=�޼۵�, DERIVATIVE_MARKET_ORDER=�м۵�
	// Order type:
	//		DERIVATIVE_LIMIT_ORDER=limit order, DERIVATIVE_MARKET_ORDER=market order 
	TDAStringType		OrderType;							
	
	TDAStringType		CancelledDate;						// ��������
															// Cancelled date

	TDAStringType		CancelledTime;						// ����ʱ��
															// Cancelled time

	TDAStringType		ErrorCode;							// �������
															// Error code
	
	TDAStringType		OrdSourceType;						// �ն�����(CME�������ض�)
															// Identify the type of terminal(CME exchange specific)
															
	TDAStringType		Tag50;								// �µ���ID(CME�������ض�)
															// Order placer's id (CME exchange specific)
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
															// User id

	TDAStringType		AccountNo;							// �ʽ��˺�
															// Account No
// �Ƿ�ģ���û���DERIVATIVE_IS_SIMULATED_USER=�ǣ�DERIVATIVE_IS_NOT_SIMULATED_USER or other������
// Is it a simulated user:
// DERIVATIVE_IS_SIMULATED_USER=is a simulated user
// DERIVATIVE_IS_NOT_SIMULATED_USER or other = is not a simulated user
	TDAStringType		IsSimulation;						
															
	TDAStringType		OrderNo;							// ȡ��ָ���������Ժ�Ķ���
															// Obtain a subsequent order with the specified order number

	TDAStringType		OrderDateTime;						// ȡ��ָ������ʱ���Ժ�Ķ�������ʽ��yyyy-MM-dd hh:mm:ss��
															// Obtain orders after the specified order time��format��yyyy-MM-dd hh:mm:ss��

	TDAStringType		ErrorDescription;					// ������Ϣ
															// Error description
};
// ��ѯ��������
struct CFutureRspOrderField
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

	TDAStringType		BidAskFlag;							// ������: DERIVATIVE_BID=��,DERIVATIVE_ASK=��
															// Bid or ask: DERIVATIVE_BID=bid,DERIVATIVE_ASK=ask

	TDAStringType		OrderQty;							// ��������
															// Order quantity

	TDAStringType		OrderPrice;							// �µ��۸�
															// Order price

	TDAStringType		FilledQty;							// �ѳɽ���
															// Filled quantity (The number of orders has been completed)

	TDAStringType		FilledPrice;						// �ɽ�����
															// Filled price(Average transaction price)

	// �������ͣ�
	//		DERIVATIVE_LIMIT_ORDER=�޼۵�, DERIVATIVE_MARKET_ORDER=�м۵�
	//		DERIVATIVE_LIMIT_STOP_ORDER=�޼�ֹ��DERIVATIVE_STOP_LOSS_ORDER=ֹ��	
	// Order type:
	//		DERIVATIVE_LIMIT_ORDER=limit order, DERIVATIVE_MARKET_ORDER=market order 
	//		DERIVATIVE_LIMIT_STOP_ORDER=limit stop order ,DERIVATIVE_STOP_LOSS_ORDER=stop loss order
	TDAStringType		OrderType;							
	
	TDAStringType		OrderDate;							// �µ�����
															// Order date

	TDAStringType		OrderTime;							// �µ�ʱ��
															// Order time

	TDAStringType		ErrorCode;							// �������
															// Error code

	// ����״̬:
	//		DERIVATIVE_ORDER_STATE1=������  DERIVATIVE_ORDER_STATE2=���Ŷӣ�  DERIVATIVE_ORDER_STATE3=���ֳɽ�
	//		DERIVATIVE_ORDER_STATE4=��ȫ�ɽ���DERIVATIVE_ORDER_STATE5=�ѳ��൥��DERIVATIVE_ORDER_STATE6=�ѳ���
	//		DERIVATIVE_ORDER_STATE7=ָ��ʧ�ܣ�DERIVATIVE_ORDER_STATE8=���ͳ���  DERIVATIVE_ORDER_STATE9=�����ģ�
	//		DERIVATIVE_ORDER_STATEA=������
	// Order state:
	//		DERIVATIVE_ORDER_STATE1=requested 
	//		DERIVATIVE_ORDER_STATE2=be queuing  
	//		DERIVATIVE_ORDER_STATE3=some orders were closed  
	//		DERIVATIVE_ORDER_STATE4=full order  
	//		DERIVATIVE_ORDER_STATE5=the remaining order has been cancelled
	//		DERIVATIVE_ORDER_STATE6=order has been cancelled  
	//		DERIVATIVE_ORDER_STATE7=command failure 
	//		DERIVATIVE_ORDER_STATE8=the command is waiting to be sent 
	//		DERIVATIVE_ORDER_STATE9=the command is waiting to be changed 
	//		DERIVATIVE_ORDER_STATEA=the command is waiting to be cancelled
	TDAStringType		OrderState;							
	
	TDAStringType		CancelUserId;						// �������û���ʶ
															// User id of cancel order

	TDAStringType		TriggerPrice;						// �����۸�
															// Trigger price

	// ��Ч����:
	//		DERIVATIVE_TDY_TIF=������Ч, DERIVATIVE_GTC_TIF=������Ч��GTC����DERIVATIVE_OPG_TIF=OPG,DERIVATIVE_IOC_TIF4=IOC
	//		DERIVATIVE_FOK_TIF=FOK��DERIVATIVE_GTD_TIF=GTD��DERIVATIVE_ATC_TIF=ATC��DERIVATIVE_FAK_TIF=FAK
	// order time in force:
	//		DERIVATIVE_TDY_TIF=the day only,DERIVATIVE_GTC_TIF=GTC,DERIVATIVE_OPG_TIF=OPG,DERIVATIVE_IOC_TIF=IOC
	//		DERIVATIVE_FOK_TIF=FOK,DERIVATIVE_GTD_TIF=GTD,DERIVATIVE_ATC_TIF=ATC,DERIVATIVE_FAK_TIF=FAK
	TDAStringType		TIF;								

	TDAStringType		OpenCloseFlag;						// ���ֻ���ƽ��: DERIVATIVE_OPEN_POS_FLAG=����,DERIVATIVE_CLOSE_POS_FLAG=ƽ��
															// Open/close position flag: DERIVATIVE_OPEN_POS_FLAG=open position	,DERIVATIVE_CLOSE_POS_FLAG=close position

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
struct CFutureQryTradeField
{

	TDAStringType		UserId;								// �û�		
	TDAStringType		ErrorDescription;					// ������Ϣ
	TDAStringType		lastFilledNo;						//��ѯ�����һ���û��ɽ��� //update 2020.04.29 ywh
	TDAStringType		maxItemNumOnePage;					//��ѯ�ɽ�ÿҳ�������		
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
// Query fund
struct CFutureQryCapitalField
{
	TDACharType			Unused;								// ��ʹ��
															// No use

	TDAStringType		ErrorDescription;					// ������Ϣ
															// Error description
};
// ��ѯ�ʽ𷵻�
// Query fund return struct
struct CFutureRspCapitalField
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
															// Today inital balance

	TDAStringType		TodayRealtimeBalance;				// �ɣ���Ȩ�棻�£�����ʵʱ����Ȩ��
															// Today realtime floating balance with Profit&Loss

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
															// Currency rate

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
							
	TDAMoneyType		TradeLimit;							// �����޶�
															// Trade limit

	TDAMoneyType		CanCashOutMoneyAmount;				// ��ȡ�ʽ�
															// Can cash out money amount

	TDAMoneyType		DepositInterest;					// �´����Ϣ
															// Monthly deposit interest

	TDAMoneyType		LoanInterest;						// ��Ƿ����Ϣ
															// Monthly loan interest

	TDAStringType		ErrorDescription;					// ������Ϣ
															// Error description
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
// Push order change struct
struct CFutureRtnOrderField
{
	TDAStringType		LocalNo;							// ���ر�� API�û��ĳ���ָ���ı��ض������
															// Order ID assigned by API user program

	TDAStringType		ExchangeCode;						// ����������
															// Exchange code

	TDAStringType		ContractCode;						// ��Լ����
															// Contract code

	TDAStringType		OrderNo;							// ������ ������ϵͳ�����Ķ����ţ�LocalNo:SystemNo:OrderNo��һ��һ��һ�Ĺ�ϵ
															// the order number given by the exchange system ,LocalNo:SystemNo:OrderNo,these three are one-to-one relationships

	TDAIntType			OrderQty;							// ί������
															// Quantity of entrusted order

	TDAIntType			FilledQty;							// �ѳɽ�����
															// Filled quantity

	TDAPriceType		FilledAvgPrice;						// �ɽ�����
															// Filled average price	

	TDAIntType			LongPositionQty;					// ��������
															// Long position quantity

	TDAPriceType		LongPosAveragePrx;					// �ɣ����򿪲־��ۣ��£���ֳɽ�����
															// Long - position average price

	TDAPriceType		CNLongPosAveragePrx;				// �й�Ʒ��(����INE/sc)�����õ�ƽ����
															// Long - position average price for Chinese varieties (e.g., INE/sc)

	TDAIntType			ShortPositionQty;					// ��������
															// Short position quantity

	TDAPriceType		ShortPosAveragePrx;					// �ɣ��������־��ۣ��£��ղֳɽ�����
															// Short position transaction average price

	TDAPriceType		CNShortPosAveragePrx;				// �й�Ʒ��(����INE/sc)�����õ�ƽ����
															// Short - position average price for Chinese varieties (e.g., INE/sc)
	// �Ƿ��Ѿ�������
	//	    DERIVATIVE_ORDER_IS_NOT_CANCELLED��û�У�DERIVATIVE_ORDER_IS_CANCELLED���ѳ���														// Short  position average price for Chinese varieties (e.g., INE/sc)
	// Order is cancelled ��
	//		DERIVATIVE_ORDER_IS_NOT_CANCELLED=order is not cancelled
	//		DERIVATIVE_ORDER_IS_CANCELLED=order is cancelled
	TDAStringType		IsCanceled;							
					
	TDAPriceType		FilledTotalFee;						// �ɽ��ܵ�������
															// Total transaction fee

	TDAIntType			SequenceNo;							// ˳���
															// Sequence No

	TDAStringType		AccountNo;							// �ʽ��ʺ�
															// Account No
	//�ֲ�����:
	//		DERIVATIVE_POSITION_TYPE_Y=���,DERIVATIVE_POSITION_TYPE_T=���
	//Position type:
	//		DERIVATIVE_POSITION_TYPE_Y=yesterday position, DERIVATIVE_POSITION_TYPE_T=today position
	TDAStringType		PositionType;						
															

	TDAPriceType		LongPosMargin;						// ����֤��
															// Long position margin

	TDAPriceType		ShortPosMargin;						// ������֤��
															// Short position margin

	TDAPriceType		CurrPrice;							// ���¼�
															// Current price

	TDAPriceType		ProfitLoss;							// ����ӯ��
															// Profit loss
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
// Query position total return
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
	TDAStringType		CommodityCode;					// ��Ʒ��ź�ԼNO 
	TDAStringType		ExchangeNo;						// ���������
	TDAStringType		ContractNo;						// ��ԼNO
	TDAStringType		ContractFName;					// ��Լ��
	TDAStringType		CommodityNo;					// ��Ʒ���
	TDAStringType		CommodityFName;					// ��Ʒ�� 
	TDAStringType		CommodityType;					// ��Ʒ��� 
	TDAStringType		CommodityFCurrencyNo;			// ���ұ�� 
	TDAStringType		CurrencyFName;					// �������� 
	TDAPriceType		ProductDot;						// ��ֵ��һ����С����ļ�ֵ��
	TDAPriceType		UpperTick;						// ��С�䶯��λ 
	TDAStringType		ExchangeName;					// ���������� 
	TDAPriceType		LastSettlePrice;				// ���ս���� 
	TDAStringType		TradeMonth;						// ������ (yyyyMM)/������ (yyyyMMdd)
	TDAIntType			DotNum;							// ����С����λ��
	TDAIntType			LowerTick;						// ���׵�λ
	TDAIntType			DotNumCarry;					// ����С����λ��
	TDAPriceType		UpperTickCarry;					// ������С�䶯��λ
	TDAStringType		FirstNoticeDay;					// �״�֪ͨ�� (yyyyMMdd)
	TDAPriceType		FreezenPercent;					// ���ᱣ֤��ٷֱ� ���Ϻ���Դ���뱣֤��ٷֱȣ�
	TDAPriceType		FreezenMoney;					// ���ᱣ֤��̶�ֵ 
	TDAPriceType		FeeMoney;						// �̶������� 
	TDAPriceType		FeePercent;						// �ٷֱ������� 
	TDAPriceType		PriceStrike;					// �ֻ���Ʒ������ 
	TDAPriceType		ProductDotStrike;				// �ֻ���Ʒ��ֵ  
	TDAPriceType		UpperTickStrike;				// �ֻ���Ʒ��С�䶯��λ 
	TDAStringType		LastTradeDay;					// ������� (yyyyMMdd)
	TDAStringType		LastUpdateDay;					// �������� (yyyyMMdd)
	TDAPriceType		CriticalPrice;					// ��Ȩ�ٽ�۸� 
	TDAPriceType		CriticalMinChangedPrice;		// ��Ȩ�ٽ�۸����µ���С���� 
	TDAStringType		ExchangeSub;					// ʵ�ʽ�����(CMEϸ�ֳ�3��������:CME,CME_COMEX,CME_NYMEX)
	TDAStringType		OptionType;						// ��Ȩ����(R�����ǣ�F������)
	TDAStringType		OptionMonth;					// ��Ȩ����(yyyyMM)
	TDAStringType		OptionStrikePrice;				// ��Ȩִ�м۸�
	TDAStringType		OptionCommodityNo;				// ��Ȩ��Ӧ�ڻ���Ʒ��ţ��Ϻ���Դ������֤��ٷֱȣ�
	TDAStringType		OptionContractNo;				// ��Ȩ��Ӧ�ڻ���Լ���
	TDAStringType		ContractFNameEN;				// ��Լ����Ӣ�ģ�
	TDAStringType		CommodityFNameEN;				// ��Ʒ����Ӣ�ģ�
	TDAStringType		OptionStyle;					// ��Ȩ���(E��ŷʽ��A����ʽ)
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



}//end of namespace Directaccess