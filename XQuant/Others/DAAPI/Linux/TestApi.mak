
CC = gcc
CPP = g++
LINK = g++ -Wl,-rpath=. 

CFLAGS   = -m64 -O3 -W -Wno-format -Wno-unused-result -Wno-missing-field-initializers -finput-charset=GBK
CPPFLAGS = -m64 -O3 -W -Wno-format -Wno-unused-result -Wno-missing-field-initializers -finput-charset=GBK -std=c++0x
LDFLAGS  = -ldl -pthread -lrt -Wl,-Bdynamic -L. -lDAApi

CORE_INCS = -I include -I TestApi

ALL_HPP =  TestApi/MyFuture.h \
	TestApi/MyMarket.h \
	TestApi/MyStock.h \
	TestApi/stdafx.h

main: main.o minIni.o
	$(LINK) -o TestApi.elf Main.o minIni.o $(LDFLAGS)

main.o: TestApi/Main.cpp $(ALL_HPP)
	$(CPP) -c TestApi/Main.cpp $(CPPFLAGS) $(CORE_INCS)

minIni.o: TestApi/minIni.c $(ALL_HPP)
	$(CC) -c TestApi/minIni.c $(CFLAGS) $(CORE_INCS)

clean:
	rm -f *.o *.elf *.a






