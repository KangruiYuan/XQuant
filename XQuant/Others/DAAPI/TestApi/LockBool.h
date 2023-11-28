
#pragma once

class CLockBool
{
private:
	std::mutex		m_mutex;		// ��ֵ��
	bool			m_value;		// ����ֵ

public:
	CLockBool() :m_value(false) {}
	virtual ~CLockBool() {}

public:
	inline void operator = (bool value)
	{
		m_mutex.lock();
		m_value = value;
		m_mutex.unlock();
	}
	inline operator bool()
	{
		m_mutex.lock();
		bool temp = m_value;
		m_mutex.unlock();
		return temp;
	}
};

