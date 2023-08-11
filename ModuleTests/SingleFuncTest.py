
from XQuant import DataAPI
from XQuant import SQLAgent
from XQuant import Tester, Tools
from XQuant import Size

s = Size(begin='20220101')
IC, IR = Tester.ICIR(s.LNCAP, s.returns)
Tester.plotter(IC, output=True)

# print(Tools.search_keyword("PE", update=False, verbose=False, limit=5))
