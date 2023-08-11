
from XQuant import DataAPI
from XQuant import SQLAgent
from XQuant import Analyzer, Tools
from XQuant import Size
from XQuant import BufferManager

BufferManager.display_file_tree()
BufferManager.delete_files()

# s = Size(begin='20220101')
# IC, IR = Tester.ICIR(s.LNCAP, s.returns)
# Tester.plotter(IC, output=True)

# print(Tools.search_keyword("PE", update=False, verbose=False, limit=5))
