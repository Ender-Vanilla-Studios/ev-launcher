import zipfile
import os
import shutil
import requests

# with zipfile.ZipFile('мод пак на Ender_vanilla 1.19.4-20240505T073428Z-001.zip', 'r') as zip_ref:
#  zip_ref.extractall('ev-test')

url19_4 = 'https://www.dropbox.com/scl/fi/hybfe4qlrnyn9gfeaag3k/modpack-EV-1.19.4.zip?rlkey=jzh6lltilkus2by45wbqekvo5&st=oxvgz9lv&dl=1'
url20_1 = 'https://www.dropbox.com/scl/fi/4fm8uwicf4wvz13inmmh6/modpack-EV-1.20.1.zip?rlkey=qr88pkwqkgw2dvtpoo9vzmc6v&st=3duyy9eb&dl=1'
url20_4 = 'https://www.dropbox.com/scl/fi/h3k65ptezyc2fq0vdsgtg/modpack-EV-1.20.4.zip?rlkey=0qzcg34jnf1t73kulv06go5mx&st=13yqx3xz&dl=1'

# response = requests.get(url19_4)
# with open("modpack EV 1.19.4.zip", 'wb') as f:
#  f.write(response.content)

url = url19_4

r = requests.get(url)
with open('modpack EV 1.19.4.zip', 'wb') as f:
 f.write(r.content)


os.chdir('.ev-game')
shutil.unpack_archive('modpack EV 1.19.4', '.', format= "zip")
os.remove('modpack EV 1.19.4.zip')