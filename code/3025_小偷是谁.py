import sys
names = [b"\xBC\xD7", b"\xD2\xD2", b"\xB1\xFB", b"\xB6\xA1"]

found = False
for thief in range(4):
    a1 = (thief != 1) 
    a2 = (thief == 3) 
    jia_ok = (a1 and a2) or ((not a1) and (not a2))

    b1 = (thief != 1)  
    b2 = (thief == 2)  
    yi_ok = (b1 and b2) or ((not b1) and (not b2))

    
    c1 = (thief != 0)  
    c2 = (thief == 1)  
    bing_ok = (c1 and c2) or ((not c1) and (not c2))

    
    d1 = (thief != 3)  
    d2 = True        
    ding_ok = (d1 and d2) or ((not d1) and (not d2))

    if jia_ok and yi_ok and bing_ok and ding_ok:
        sys.stdout.buffer.write(names[thief])
        found = True
        break

if not found:
    sys.stdout.buffer.write(b"\n")