# Miksikese-hack
Automaatne bot, mis suudab teha Miksikese pranglimist.

Hetkel töötab veatult lahutamisega.   
Liitmisel satub vahepeal pytesseract segadusse ja loeb pildi pealt näiteks välja "34+5", kuigi tegelt oli pildil "3+4". "+" märk tingib vahepeal lisa "4" lugemist. Võiks parandada fondi muutmisega või muul viisil pildi tuunimisega.    
Korrutamine ja jagamine hetkel ei tööta, sest pythoni eval() ei saa hakkama märkidega ":" ja "x". Tuleks lihtsalt pildilt loetavat sõne töödelda ja need sümbolid vahetada tehtemärkidega, mis vastavad Pyhtoni süntaksile.   
