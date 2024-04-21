import xml.etree.ElementTree as et
from pathlib import Path
import sys,os,re

if getattr(sys, 'frozen', False):
	cwd = os.path.dirname(os.path.abspath(sys.executable))
elif __file__:
    cwd = os.path.dirname(os.path.abspath(__file__))
cwd=Path(cwd)
if(__name__=="__main__"):
    try:
        specfile=Path(sys.argv[1])
    except KeyError:
        sys.exit()
    if (specfile.exists()):
        temp=""
        try:
            xml=et.parse(specfile)
        except:
            xml=et.ElementTree(et.Element("debug"))
            xmlroot=xml.getroot()
            with open(specfile,'r',encoding='utf-8') as f:
                content=f.readlines()
            for i in content:
                result=re.match(r"(Kart.)([A-Z|a-z]+)\s?=\s?([\d|.]+)(f?);",i)
                if result:
                    xmlroot.attrib[result.group(2)]=result.group(3)
                xml.write("Kartspec.xml")
        else:
            xmlroot=xml.getroot()
            if xmlroot.tag=="debug":
                for dataname,data in xmlroot.attrib.items():
                    temp+=f"Kart.{dataname} = {data}{'f' if '.' in data else ''};\n"
                with open("Kartspec.txt",'w',encoding='utf-8') as f:
                    f.write(temp)
        
    