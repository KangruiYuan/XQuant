
from pathlib import Path
import os

jupyter_folder = Path(__file__).parent
html_folder = Path(__file__).parents[1] / "Docs" / "DemoHtml"

jupyter_files = list(jupyter_folder.glob('*.ipynb'))

for file in jupyter_files:
    os.system(f"jupyter nbconvert --to html {file}")

orginal_files = list(jupyter_folder.glob('*.html'))

for file in orginal_files:
    destination = html_folder / file.name
    with destination.open(mode='wb') as fid:
        fid.write(file.read_bytes())
    file.unlink()
