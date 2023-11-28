/////////////////////////////////////////////////////////////////////////
/// DriectAccess Trade Engine
/// Copyright (C) Shanghai DirectAccess Technology Co., Ltd.
/// Last Modify 2019/3/18
/// Define DataType For API
/// Author (c) Wang Jian Quan (Franklin)
/////////////////////////////////////////////////////////////////////////

#pragma once

#define DA_STR_SIZE					256

#define MAX_BROKER					4096

#define DAAPI_VERSION				"1.12"

#ifdef _WIN32 
#define OS_NAME						"Windows"
#else
#define OS_NAME						"Linux"
#endif

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

