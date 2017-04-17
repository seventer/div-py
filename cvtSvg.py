import xmltodict

with open('icons.ssvg') as fd:
    doc = xmltodict.parse(fd.read())

#ff = doc['svg']['defs']['font']['glyph']
#print (ff)
print ('=============================')


for rec_no in range(len(doc['svg']['defs']['font']['glyph'])):
    print("==-[" + str(rec_no) + "]-==")
    name = doc['svg']['defs']['font']['glyph'][rec_no]
    filename = str(rec_no)
    glyph_name = ""
    unicode = ""
    vert_adv_y = ""
    d = ""
    print ('=============================')    
    for key, value in name.items():
        if (key =='@glyph-name'):
            glyph_name = " glyph-name=\"" + value + "\""
            filename = value 
        if (key =='@unicode'):
            unicode = " unicode=\"" + value + "\""
        if (key =='@vert-adv-y'):
            vert_adv_y = " vert_adv-y=\"" + value + "\""
        if (key =='@d'):
            d = " d=\"" + value + "\""
            
    print(glyph_name)
    print(unicode)
    print(vert_adv_y)
    #print ('=============================')
    #print ("<path transform=\"scale(1, -1) translate(0, -1500)\"" +glyph_name + unicode + vert_adv_y + d + "/>")
    #print ('=============================')
    with open(filename + ".svg", 'w') as w:
        w.write('<?xml version="1.0" standalone="no"?>\n')
        w.write('<svg width="1500px" height="1500px" version="1.1" xmlns="http://www.w3.org/2000/svg">\n')
        w.write("<path " + glyph_name + unicode + vert_adv_y + d + "/>")
        w.write('</svg>')

    


