import json
import time
from classes.page import Page
from classes.adresar_page import AdresarPage

Page.addPage(AdresarPage("https://www.sreality.cz/adresar?strana=1"))
Page.run()
f = open(str(int(time.time()))+".json", "w")
f.write(json.dumps(Page.getCompanies()))
f.close()