1：libDAApi.so 静态引用了 openssl库1.1.1和zlib库1.2.11。主程序在使用libDAApi.so的时候，如果自身也使用了openssl和zlib的话，建议也静态引用openssl库和zlib库；防止libDAApi.so引用二义性。

2：so发布以使用度比较高的gcc4.8.5和centos7为编译工具和环境。 建议gcc以此版本为准，并建议linux core版本以centos7为准

3：编译DEMO程序TestApi的命令行是 make -f TestApi.mak -B

