// stdafx.h : ��׼ϵͳ�����ļ��İ����ļ���
// ���Ǿ���ʹ�õ��������ĵ�
// �ض�����Ŀ�İ����ļ�
//

#pragma once

#ifdef _WIN32

#include <map>
#include <mutex>
#include <string>
#include <fstream>
#include <iostream>
#include <algorithm>

#include <SDKDDKVer.h>
#include <windows.h>

using namespace std;

#else

#include <map>
#include <mutex>
#include <string>
#include <fstream>
#include <iostream>
#include <algorithm>
#include <sys/time.h>

#include <stdlib.h>
#include <stdarg.h>
#include <memory.h>
#include <unistd.h>

using namespace std;

#include "minIni.h"

#endif
