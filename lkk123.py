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
    output = e.__repr__()
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
            if "ForwardAccelForce" in _any:
                return "ForwardAccelForce"
            return None
    
    def __setoutput(index:str,content:float|int):
        global output
        try:
            if content.is_integer():
                content = int(content)
        except AttributeError:
            output += 'Kart.' + index + ' = ' + str(content) + ';\n'
            outputxmlroot.set(index,str(content))
            return
        if isinstance(content,float):
            output += 'Kart.' + index + ' = ' + float_to_str(content) + 'f;\n'
            outputxmlroot.set(index,float_to_str(content))
        elif isinstance(content,int):
            output += 'Kart.' + index + ' = ' + str(content) + ';\n'
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
        paramroot=parse.getroot()
        for i in data.keys():
            try:
                paramdataname=i
                kartdataname=i
                if i == 'StartForwardAccelForceSpeed':
                    paramdataname='StartForwardAccelFactorSpeed'
                elif i == 'StartForwardAccelForceItem':
                    paramdataname='StartForwardAccelFactorItem'
                value=paramroot.attrib[paramdataname]
                if data[kartdataname].useable:
                    value = data[kartdataname].formula.evaluate(value)
                elif kartdataname == 'instAccelGaugeMinUsable':
                    value = float(outputxmlroot.attrib['instAccelGaugeLength']) * float(value)
                elif "StartForwardAccelForce" in kartdataname:
                     tempformula=data[kartdataname].formula.OutputInfixformula().replace("ForwardAccelForce",outputxmlroot.attrib["ForwardAccelForce"])
                     tempformula=Formula(tempformula,True)
                     value = tempformula.evaluate(value)
                elif 'x ? 1 : 0' in data[kartdataname].formula.OutputInfixformula():
                    if __readbool(value):
                        value=1
                    else:
                        value=0
                else:
                    value = data[kartdataname].default
                __setoutput(kartdataname,value)
            except KeyError:
                default=data[kartdataname].default
                if "StartForwardAccelForce" in kartdataname:
                    default=float(outputxmlroot.attrib["ForwardAccelForce"])
                __setoutput(kartdataname,default)
    except Exception as e:
        xml=None
        _type=1
        output = e.__repr__()

finally:
    
    if _type==1:
        with open("param_.xml",'w',encoding='utf-8') as f:
            f.write(output)
    elif _type == 0:
            outputxml.write("param_.xml")

    