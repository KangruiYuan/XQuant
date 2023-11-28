#pragma once
#include "DAFutureApi.h"

class ITrade
{
    public:
	virtual void OnFrontConnected() {};
	virtual void OnFrontDisconnected(int iReason) {};
	virtual void OnRspQryCapital(CFutureRspCapitalField *pRspCapital, CFutureRspInfoField *pRspInfo, int iRequestID, bool bIsLast) {};
};

