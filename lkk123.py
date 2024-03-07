import sys,os
from pathlib import Path
import xml.etree.ElementTree as ElementTree
from Additional_class import Formula,formula_data,float_to_str

if getattr(sys, 'frozen', False):
		cwd = os.path.dirname(os.path.abspath(sys.executable))
elif __file__:
    cwd = os.path.dirname(os.path.abspath(__file__))
cwd=Path(cwd)
try:
    setting=Path(sys.argv[1])
    if setting.suffix=='.xml':
        file=setting
        _type=1
    else:
        with open(setting,'r',encoding='utf-8') as f:
            try:
                file , _type = f.readline().split(',')
                _type=int(_type)
            except ValueError:
                f.seek(0)
                file = f.readline()
                _type = 1
    xml=Path(file)
except Exception as e:
    xml=None
    _type=1
    output = str(e.with_traceback(None))
else:
    def __readbool(_str:str):
            if 'true' in _str.lower():
                return True
            return False
        
    def __readdefault(_any):
        try:
            result = float(_any)
            if result.is_integer():
                result = int(result)
            return result
        except ValueError:
            return None
    
    def __setoutput(index:str,content:float|int):
        if content.is_integer():
            content = int(content)
        if isinstance(content,float):
            global output
            output += 'Kart.' + index + ' = ' + float_to_str(content) + 'f\n'
            outputxmlroot.set(index,float_to_str(content))
        elif isinstance(content,int):
            output += 'Kart.' + index + ' = ' + str(content) + 'f\n'
            outputxmlroot.set(index,str(content))
        else:
            raise TypeError("'content' type is wrong.")

    try:
        output=''
        outputxml=ElementTree.ElementTree(ElementTree.Element('id'))
        outputxmlroot = outputxml.getroot()
        data={str():formula_data(None,Formula("",False))}
        data.clear()
        with open(cwd/"data.data",'r',encoding='utf-8') as f:
            temp=f.readline()
            while temp:
                elements=temp.split(',')
                dataname=elements[0].removesuffix(" ")
                default=__readdefault(elements[2])
                useable=__readbool(elements[3])
                formula=Formula(elements[1],useable)
                data[dataname]=formula_data(dataname,formula,default,useable)
                temp=f.readline()
        parse=ElementTree.parse(xml)
        root=parse.getroot()
        for i in data.keys():
            try:
                if i == 'StartForwardAccelForceSpeed':
                    i='StartForwardAccelFactorSpeed'
                elif i == 'StartForwardAccelForceItem':
                    i='StartForwardAccelFactorItem'
                value=root.attrib[i]
                if i=='StartForwardAccelFactorSpeed':
                    i='StartForwardAccelForceSpeed'
                elif i=='StartForwardAccelFactorItem':
                    i='StartForwardAccelForceItem'
                if data[i].useable:
                    value = data[i].formula.evaluate(value)
                elif i == 'instAccelGaugeMinUsable':
                    value = float(outputxmlroot.attrib['instAccelGaugeLength']) * float(value)
                elif 'x ? 1 : 0' in data[i].formula.OutputInfixformula():
                    if __readbool(value):
                        value=1
                    else:
                        value=0
                else:
                    value = data[i].default
                __setoutput(i,value)
            except KeyError:
                if i=='StartForwardAccelFactorSpeed':
                    i='StartForwardAccelForceSpeed'
                elif i=='StartForwardAccelFactorItem':
                    i='StartForwardAccelForceItem'
                __setoutput(i,data[i].default)
    except Exception as e:
        xml=None
        _type=1
        output = str(e)

finally:
    
    if _type==1:
        with open("param.xml",'w',encoding='utf-8') as f:
            f.write(output)
    elif _type == 0:
            outputxml.write("param.xml")

    