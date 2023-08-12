# XQuant

## 项目说明

项目主体在`XQuant`下；`Demo`为完整的功能演示；`ModuleTests`为项目测试的脚本，会时常改动。

`XQuant`下，`FactorManager`用于处理因子类的数据（计算、检验及回测）；`Scripts`为功能性的部分函数，尚未整合到项目中；`StreamWeb`为基于`Streamlit`的可视化Web服务；`TABLES`存放了已有的数据表名；`Temp`为项目计算默认的中间表缓存位置；`Tokens`存放连接服务器数据库及其他数据提供商的API的Token。

## 使用示例

| 模块名称	         |    模块说明    | 子类                             |                             模块示例	 |
|---------------|:----------:|--------------------------------|----------------------------------:|
| Utils         | 通用变量，常用函数	 | Config, TradeDate, Formatter, Tools | [Utils.ipynb](./Demo/Utils.ipynb) |
| Collector     |            |                                |                                暂无 |
| FileManager   |            |                                |                                暂无 |
| SQLAgent      |            |                                |                                暂无 |
| FactorManager |            |                                |                                暂无 |
| Schema        |     	      |                                |                                暂无 |
| Consts        |     	      |                                |                                暂无 |


## 项目结构
```text
|   README.md
|   
+---Demo
+---ModuleTests
|       BaseTest.ipynb
|       Collector_Test.py
|       SingleFuncTest.py
|       Utils_Test.py
|         
\---XQuant
    |   Collector.py
    |   Consts.py
    |   FileManager.py
    |   Schema.py
    |   SQLAgent.py
    |   Utils.py
    |   __init__.py
    |   
    +---FactorManager
    |       Analyzer.py
    |       DataReady.py
    |       FactorReady.py
    |       Processer.py
    |       __init__.py
    |   
    +---Scripts
    |       QuantWeb.py
    |       
    +---StreamWeb
    +---TABLES
    |       dataYes.json
    |       em.json
    |       gm_factor.json
    |       gm_future.json
    |       gm_stock.json
    |       info.json
    |       jq_factor.json
    |       jq_prepare.json
    |       sql.json
    |       
    +---Temp
    +---Tokens
            quant.const.ini
```
