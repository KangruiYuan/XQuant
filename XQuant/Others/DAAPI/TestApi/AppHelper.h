#pragma once

#ifndef _WIN32

#define MAX_PATH					260

typedef long						LONG;
typedef long long					LONGLONG;
typedef unsigned long long			ULONGLONG;
typedef unsigned char				BYTE;
typedef unsigned char*				LPBYTE;
typedef char*					    LPCSTR;
typedef const char*					LPCTSTR;
typedef char						TCHAR;

typedef uint32_t					DWORD;
typedef uint16_t					WORD;
typedef int 						BOOL;

#define SOCKET_ERROR				-1
#define INVALID_SOCKET				-1

#define FALSE						0
#define TRUE						1

typedef int 						SOCKET;

#define ATLASSERT

#define MoveMemory					memmove

#define __max(a,b) (((a) > (b)) ? (a) : (b))
#define __min(a,b) (((a) < (b)) ? (a) : (b))

typedef struct _SYSTEMTIME {
	WORD wYear;
	WORD wMonth;
	WORD wDayOfWeek;
	WORD wDay;
	WORD wHour;
	WORD wMinute;
	WORD wSecond;
	WORD wMilliseconds;
} SYSTEMTIME, *PSYSTEMTIME, *LPSYSTEMTIME;

inline void
GetLocalTime(LPSYSTEMTIME st)
{
	time_t now;
	time(&now);
	tm *tm_now = localtime(&now);

	timeval tv;
	gettimeofday(&tv, NULL);

	st->wYear = tm_now->tm_year + 1900;
	st->wMonth = tm_now->tm_mon + 1;
	st->wDay = tm_now->tm_mday;
	st->wHour = tm_now->tm_hour;
	st->wMinute = tm_now->tm_min;
	st->wSecond = tm_now->tm_sec;
	st->wMilliseconds = tv.tv_usec / 1000;
}

#endif

#ifdef _WIN32
#define LOCALID_FILE	".\\Config\\Live.ini"
#else
#define LOCALID_FILE	"./Config/Live.ini"
#endif

#define APP_NAME		"Generel"
#define COUTTIME		cout << GetDateTime()

void CrossSleep(int millisecond)
{
#ifdef _WIN32
	::Sleep(millisecond);
#else
	usleep(millisecond * 1000);
#endif
}

enum ColorValue
{
	Black = 0,
	Blue = 1,
	Green = 2,
	Cyan = 3,
	Red = 4,
	Pink = 5,
	Yellow = 6,
	White = 7,
	Gray = 8,
	LightBlue = 9,
	LightGreen = 10,
	LightCyan = 11,
	LightRed = 12,
	LightPink = 13,
	LightYellow = 14,
	LightWhite = 15,
};

void cprintf(ColorValue color, const char* format, ...)
{
#ifdef _WIN32
	HANDLE handle = ::GetStdHandle(STD_OUTPUT_HANDLE);

	CONSOLE_SCREEN_BUFFER_INFO csbi;
	GetConsoleScreenBufferInfo(handle, &csbi);
	SetConsoleTextAttribute(handle, color);

	va_list args;
	va_start(args, format);
	vprintf(format, args);
	va_end(args);

	SetConsoleTextAttribute(handle, csbi.wAttributes);
#else

	static const char* colorTable[16] = {
		"\033[0m\033[30m",      /* Black */
		"\033[0m\033[34m",      /* Blue */
		"\033[0m\033[32m",      /* Green */
		"\033[0m\033[36m",      /* Cyan */
		"\033[0m\033[31m",      /* Red */
		"\033[0m\033[35m",      /* Magenta */
		"\033[0m\033[33m",      /* Yellow */
		"\033[0m\033[37m",      /* White */
		"\033[1m\033[30m",      /* Bold Black */
		"\033[1m\033[34m",      /* Bold Blue */
		"\033[1m\033[32m",      /* Bold Green */
		"\033[1m\033[36m",      /* Bold Cyan */
		"\033[1m\033[31m",      /* Bold Red */
		"\033[1m\033[35m",      /* Bold Magenta */
		"\033[1m\033[33m",      /* Bold Yellow */
		"\033[1m\033[37m"      /* Bold White */
	};

	const int count = sizeof(colorTable) / sizeof(colorTable[0]);
	if (color < count) {
		printf(colorTable[color]);

		va_list args;
		va_start(args, format);
		vprintf(format, args);
		va_end(args);

		printf("\033[0m");
	}
#endif
}

#define safe_cpy(tar, src)	SafeStrcpy(tar, sizeof(tar), src);

inline void SafeStrcpy(char* tar, size_t tar_size, const char* src)
{
	size_t n = __min(strlen(src), tar_size - 1);
	memcpy(tar, src, n);
	tar[n] = 0;
}

