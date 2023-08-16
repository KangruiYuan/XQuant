# XQuant

## 项目说明

项目主体在`XQuant`下；`Demo`为完整的功能演示；`ModuleTests`为项目测试的脚本，会时常改动。

`XQuant`下，`FactorManager`用于处理因子类的数据（计算、检验及回测）；`Scripts`为功能性的部分函数，尚未整合到项目中；`StreamWeb`为基于`Streamlit`的可视化Web服务；`TABLES`存放了已有的数据表名；`Temp`为项目计算默认的中间表缓存位置；`Tokens`存放连接服务器数据库及其他数据提供商的API的Token。

## 使用示例

| 模块名称	         |    模块说明    | 子类                                          |                                         模块示例	 |
|---------------|:----------:|:--------------------------------------------|----------------------------------------------:|
| Utils         | 通用变量，常用函数	 | Config, TradeDate, Formatter, Tools         |             [Utils.ipynb](https://github.com/KangruiYuan/XQuant/blob/master/Demo/Utils.ipynb) |
| Collector     |    取数框架    | DataAPI                                     |     [Collector.ipynb](https://github.com/KangruiYuan/XQuant/blob/master/Demo/Collector.ipynb) |
| FileManager   |   文件管理器    | BufferManager                               | [FileManager.ipynb](https://github.com/KangruiYuan/XQuant/blob/master/Demo/FileManager.ipynb) |
| FactorManager | 因子计算、检验及回测 | Analyzer, DataReady, FactorReady, Processer |                                            暂无 |
| SQLAgent      |   SQL交互    |                                             |                                            暂无 |
| Consts        |  初始化加载信息   |                                             |                                            暂无 |
| Schema        | 数据范式    	  |                                             |                                            暂无 |
| Scripts       | 项目相关的实用脚本  |                                             |                                            暂无 |
| StreamWeb     |   可视化网页    |                                             |    请运行[RunWeb.py](https://github.com/KangruiYuan/XQuant/blob/master/XQuant/Scripts/RunWeb.py) |


## 项目结构
```text
|   .gitignore
|   .gitmodules
|   README.md
|   __init__.py
|   
+---.github
|   \---ISSUE_TEMPLATE
|           ISSUE_FOR_BUG.md
|           ISSUE_FOR_DEMAND.md
|           
+---.idea
|   |   .gitignore
|   |   encodings.xml
|   |   misc.xml
|   |   modules.xml
|   |   vcs.xml
|   |   workspace.xml
|   |   XQuant.iml
|   |   
|   \---inspectionProfiles
|           profiles_settings.xml
|           Project_Default.xml
|           
+---Demo
|       Collector.ipynb
|       FileManager.ipynb
|       Utils.ipynb
|       
+---Docs
|       DirTree.txt
|       
+---ModuleTests
|   |   BaseTest.ipynb
|   |   Collector_Test.py
|   |   SingleFuncTest.py
|   |   Utils_Test.py
|   |   
|           Collector_Test.cpython-310.pyc
|           Utils_Test.cpython-310.pyc
|           
+---XQuant
|   |   Collector.py
|   |   Consts.py
|   |   FileManager.py
|   |   Schema.py
|   |   SQLAgent.py
|   |   Utils.py
|   |   __init__.py
|   |   
|   +---FactorManager
|   |   |   Analyzer.py
|   |   |   DataReady.py
|   |   |   FactorReady.py
|   |   |   Processer.py
|   |   |   __init__.py
|   |   |   
|   |           Analyzer.cpython-310.pyc
|   |           DataReady.cpython-310.pyc
|   |           FactorReady.cpython-310.pyc
|   |           Processer.cpython-310.pyc
|   |           __init__.cpython-310.pyc
|   |           
|   +---Scripts
|   |       AutoStart_windows.bat
|   |       DetectWeb.py
|   |       RunWeb.py
|   |       
|   +---StreamWeb
|   |   |   Home.py
|   |   |   
|   |   +---pages
|   |   |       1_Barra_Factor.py
|   |   |       2_Factor_Analysis.py
|   |   |       
|   |   +---pics
|   |   |       ws_logo.png
|   |   |       
|   +---TABLES
|   |       dataYes.json
|   |       em.json
|   |       gm_factor.json
|   |       gm_future.json
|   |       gm_stock.json
|   |       info.json
|   |       jq_factor.json
|   |       jq_prepare.json
|   |       sql.json
|   |       
|   +---Temp
|   |   |   attrs.json
|   |   |   
|   |   \---web_functions
|   |       |   function.py
|   |       |   
|   |               function.cpython-310.pyc
|   |               
|   +---Tokens
|   |       quant.const.ini
|   |       
|           Collector.cpython-310.pyc
|           Consts.cpython-310.pyc
|           FileManager.cpython-310.pyc
|           Schema.cpython-310.pyc
|           SQLAgent.cpython-310.pyc
|           Utils.cpython-310.pyc
|           __init__.cpython-310.pyc
|           
\---XQuant.wiki

```
