import base64
iconname="Icon2.ico"
with open('icon.py', 'w+') as f:
    f.write(f"img = {base64.b64encode(open(iconname,'rb').read())}")