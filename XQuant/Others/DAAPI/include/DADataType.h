/////////////////////////////////////////////////////////////////////////
/// DriectAccess Trade Engine
/// Copyright (C) Shanghai DirectAccess Technology Co., Ltd.
/// Last Modify 2019/3/18
/// Define DataType For API
/// Author (c) Wang Jian Quan (Franklin)
/////////////////////////////////////////////////////////////////////////

#pragma once

namespace Directaccess{

#define DA_STR_SIZE					256
#define TRADE_MAX_NUM_ONE_PAGE		(5000)	//update 2020.04.30 ywh 
#define MAX_BROKER					4096

#define DAAPI_VERSION				"1.18.2.0"

#ifdef _WIN32 
#ifdef LIB_DA_API_EXPORT
#define DA_API_EXPORT				__declspec(dllexport)
#else
#define DA_API_EXPORT				__declspec(dllimport)
#endif
#else
#define DA_API_EXPORT
#endif

typedef char						TDACharType;
typedef char						TDAStringType[DA_STR_SIZE];
typedef char						TDABrokerType[MAX_BROKER];

typedef int							TDAIntType;
typedef int							TDAVolumeType;

typedef double						TDADoubleType;
typedef double						TDAPriceType;
typedef double						TDAMoneyType;

/// ����������˶���
#define MAX_SUB_COUNT				20

/////////////////////////////////////////////////////////////////////////
/// ������������
/////////////////////////////////////////////////////////////////////////

/// ��Ʊ
#define DAF_TYPE_Stock				'S'
/// �ڻ�
#define DAF_TYPE_Future				'D'
/// δ֪
#define DAF_TYPE_Unknown			 0

/////////////////////////////////////////////////////////////////////////
/// ��������
/////////////////////////////////////////////////////////////////////////

/// ׷�Ӷ���
#define DAF_SUB_Append				'1'
/// �滻����
#define DAF_SUB_Replace				'2'
/// �˶�
#define DAF_SUB_Unsubcribe			'3'
/// �˶�����
#define DAF_SUB_UnsubcribeAll		'4'

/////////////////////////////////////////////////////////////////////////
/// ������������
/////////////////////////////////////////////////////////////////////////

/// ������������
#define DAF_Market_Full				'Z'
/// �ɽ���������
#define DAF_Market_Fill				'Y'


/// ���ַ��� empty std::string
#define EMPTY_STRING				""


/////////////////////////////////////////////////////////////////////////
//// Derivative define start
/////////////////////////////////////////////////////////////////////////



/// ������:		DERIVATIVE_BID=��,  DERIVATIVE_ASK=��
/// Bid or ask:		DERIVATIVE_BID=bid, DERIVATIVE_ASK=ask
#define DERIVATIVE_BID						"1"
#define DERIVATIVE_ASK						"2"

///���ֻ���ƽ��
///open/close position flag

#define DERIVATIVE_OPEN_POS_FLAG			"1"
#define DERIVATIVE_CLOSE_POS_FLAG			"2"

///��������
///order type
	// �������ͣ�
	//		DERIVATIVE_LIMIT_ORDER=�޼۵�, DERIVATIVE_MARKET_ORDER=�м۵�
	//		DERIVATIVE_LIMIT_STOP_ORDER=�޼�ֹ��DERIVATIVE_STOP_LOSS_ORDER=ֹ��	
	// Order type:
	//		DERIVATIVE_LIMIT_ORDER=limit order, DERIVATIVE_MARKET_ORDER=market order 
	//		DERIVATIVE_LIMIT_STOP_ORDER=limit stop order ,DERIVATIVE_STOP_LOSS_ORDER=stop loss order
#define DERIVATIVE_LIMIT_ORDER				"1"
#define DERIVATIVE_MARKET_ORDER				"2"
#define DERIVATIVE_LIMIT_STOP_ORDER			"3"
#define DERIVATIVE_STOP_LOSS_ORDER			"4"

///��Ч����
///order time in force
	// ��Ч����:
	//		DERIVATIVE_TDY_TIF=������Ч, DERIVATIVE_GTC_TIF=������Ч��GTC����DERIVATIVE_OPG_TIF=OPG,DERIVATIVE_IOC_TIF4=IOC
	//		DERIVATIVE_FOK_TIF=FOK��DERIVATIVE_GTD_TIF=GTD��DERIVATIVE_ATC_TIF=ATC��DERIVATIVE_FAK_TIF=FAK
	// Order time in force:
	//		DERIVATIVE_TDY_TIF=the day only,DERIVATIVE_GTC_TIF=GTC,DERIVATIVE_OPG_TIF=OPG,DERIVATIVE_IOC_TIF=IOC
	//		DERIVATIVE_FOK_TIF=FOK,DERIVATIVE_GTD_TIF=GTD,DERIVATIVE_ATC_TIF=ATC,DERIVATIVE_FAK_TIF=FAK
#define DERIVATIVE_TDY_TIF					"1"
#define DERIVATIVE_GTC_TIF					"2"
#define DERIVATIVE_OPG_TIF					"3"
#define DERIVATIVE_IOC_TIF					"4"
#define DERIVATIVE_FOK_TIF					"5"
#define DERIVATIVE_GTD_TIF					"6"
#define DERIVATIVE_ATC_TIF					"7"
#define DERIVATIVE_FAK_TIF					"8"


///����״̬
///Order state
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
#define DERIVATIVE_ORDER_STATE1				"1"
#define DERIVATIVE_ORDER_STATE2				"2"
#define DERIVATIVE_ORDER_STATE3				"3"
#define DERIVATIVE_ORDER_STATE4				"4"
#define DERIVATIVE_ORDER_STATE5				"5"
#define DERIVATIVE_ORDER_STATE6				"6"
#define DERIVATIVE_ORDER_STATE7				"7"
#define DERIVATIVE_ORDER_STATE8				"8"
#define DERIVATIVE_ORDER_STATE9				"9"
#define DERIVATIVE_ORDER_STATEA				"A"

// �Ƿ�ģ���û���DERIVATIVE_IS_SIMULATED_USER=�ǣ�DERIVATIVE_IS_NOT_SIMULATED_USER or other������
//Simulated user:
//		DERIVATIVE_IS_SIMULATED_USER=is a simulated user
//		DERIVATIVE_IS_NOT_SIMULATED_USER or other = is not a simulated user
#define DERIVATIVE_IS_SIMULATED_USER		"1"
#define DERIVATIVE_IS_NOT_SIMULATED_USER	"0"

// Order is cancelled: 
//		DERIVATIVE_ORDER_IS_NOT_CANCELLED=order is not cancelled
//		DERIVATIVE_ORDER_IS_CANCELLED=order is cancelled
#define DERIVATIVE_ORDER_IS_NOT_CANCELLED   "0"
#define DERIVATIVE_ORDER_IS_CANCELLED		"1"

//�ֲ�����:
//		DERIVATIVE_POSITION_TYPE_Y=���,DERIVATIVE_POSITION_TYPE_T=���
//Position type:
//		DERIVATIVE_POSITION_TYPE_Y=yesterday position, DERIVATIVE_POSITION_TYPE_T=today position
#define DERIVATIVE_POSITION_TYPE_Y			"0"
#define DERIVATIVE_POSITION_TYPE_T			"1"

/////////////////////////////////////////////////////////////////////////
////  End of derivative define
/////////////////////////////////////////////////////////////////////////




/////////////////////////////////////////////////////////////////////////
//// Stock define start
/////////////////////////////////////////////////////////////////////////

// �ֲַ���:
// STOCK_POSITION_FLAG_LONG=����STOCK_POSITION_FLAG_SHORT=������
// The position direction flag:
// STOCK_POSITION_FLAG_LONG=long position,STOCK_POSITION_FLAG_SHORT=short position
#define STOCK_POSITION_FLAG_LONG			"1"
#define STOCK_POSITION_FLAG_SHORT			"2"

// ������:		STOCK_BID=��,  STOCK_ASK=��
// Bid or ask:		STOCK_BID=bid, STOCK_ASK=ask
#define STOCK_BID							"1"
#define STOCK_ASK							"2"

// ���ֻ���ƽ��:
		// STOCK_OPEN_POS_FLAG=����,STOCK_OPEN_POS_FLAG=ƽ��
// open/close position flag:
		// STOCK_OPEN_POS_FLAG=open position,STOCK_CLOSE_POS_FLAG=close position
#define STOCK_OPEN_POS_FLAG					"1"
#define STOCK_CLOSE_POS_FLAG				"2"


///��������
///order type
	// �������ͣ�
	//		STOCK_LIMIT_ORDER=�޼۵�, STOCK_MARKET_ORDER=�м۵�
	//		STOCK_LIMIT_STOP_ORDER=�޼�ֹ��STOCK_STOP_LOSS_ORDER=ֹ��	
	// Order type:
	//		STOCK_LIMIT_ORDER=limit order, STOCK_MARKET_ORDER=market order 
	//		STOCK_LIMIT_STOP_ORDER=limit stop order ,STOCK_STOP_LOSS_ORDER=stop loss order

#define STOCK_LIMIT_ORDER					"1"
#define STOCK_MARKET_ORDER					"2"
#define STOCK_LIMIT_STOP_ORDER				"3"
#define STOCK_STOP_LOSS_ORDER				"4"

///��Ч����
///order time in force
	// ��Ч����:
	//		STOCKE_TDY_TIF=������Ч, STOCK_GTC_TIF=������Ч��GTC����STOCK_OPG_TIF=OPG,STOCK_IOC_TIF4=IOC
	//		STOCK_FOK_TIF=FOK��STOCK_GTD_TIF=GTD��STOCK_ATC_TIF=ATC��STOCK_FAK_TIF=FAK
	// Order time in force:
	//		STOCK_TDY_TIF=the day only,STOCK_GTC_TIF=GTC,STOCK_OPG_TIF=OPG,STOCK_IOC_TIF=IOC
	//		STOCK_FOK_TIF=FOK,STOCK_GTD_TIF=GTD,STOCK_ATC_TIF=ATC,STOCK_FAK_TIF=FAK
#define STOCK_TDY_TIF						"1"
#define STOCK_GTC_TIF						"2"
#define STOCK_OPG_TIF						"3"
#define STOCK_IOC_TIF						"4"
#define STOCK_FOK_TIF						"5"
#define STOCK_GTD_TIF						"6"
#define STOCK_ATC_TIF						"7"
#define STOCK_FAK_TIF						"8"


///����״̬
///Order state
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
#define STOCK_ORDER_STATE1					"1"
#define STOCK_ORDER_STATE2					"2"
#define STOCK_ORDER_STATE3					"3"
#define STOCK_ORDER_STATE4					"4"
#define STOCK_ORDER_STATE5					"5"
#define STOCK_ORDER_STATE6					"6"
#define STOCK_ORDER_STATE7					"7"
#define STOCK_ORDER_STATE8					"8"
#define STOCK_ORDER_STATE9					"9"
#define STOCK_ORDER_STATEA					"A"


// �Ƿ�ģ���û���STOCK_IS_SIMULATED_USER=�ǣ�STOCK_IS_NOT_SIMULATED_USER or other������
//Simulated user:
//		STOCK_IS_SIMULATED_USER=is a simulated user
//		STOCK_IS_NOT_SIMULATED_USER or other = is not a simulated user
#define STOCK_IS_SIMULATED_USER				"1"
#define STOCK_IS_NOT_SIMULATED_USER			"0"

/////////////////////////////////////////////////////////////////////////
////  End of Stock define
/////////////////////////////////////////////////////////////////////////



}