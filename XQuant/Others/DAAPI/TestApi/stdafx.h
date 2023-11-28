// stdafx.h : 标准系统包含文件的包含文件，
// 或是经常使用但不常更改的
// 特定于项目的包含文件
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
