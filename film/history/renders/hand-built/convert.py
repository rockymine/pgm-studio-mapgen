import json
d=json.load(open('map.json'))
pal=d['palette']
M={'#858585':(1,5),'#6e6e6e':(4,0),'#8c8c8c':(1,6),'#3a1d22':(112,0),'#96604c':(45,0),'#9a6c58':(1,1),'#a77562':(1,2),'#7a7a7a':(98,0),'#5d6d72':(159,9),'#8d8d8d':(1,0),'#8a8a8a':(44,0),'#3b3b3e':(7,0),'#4a5053':(35,7),'#4aaed6':(35,3),'#707070':(4,0),'#7f7f7f':(1,0),'#5fe0d5':(57,0),'#a3a8b4':(82,0),'#9a9a92':(35,8),'#efc12f':(35,4),'#f2d03a':(41,0),'#d8d8d8':(42,0),'#b9d6e2':(20,0),'#e4e8e8':(35,0),'#e8761c':(35,1),'#e892ad':(35,6),'#a8302b':(35,14),'#58702a':(35,13),'#76b52a':(35,5),'#2fd36a':(133,0),'#bdbdbd':(1,3),'#c3c3c3':(1,4),'#b84db0':(35,2),'#9e9e9e':(43,0),'#25272b':(35,15),'#7b35ab':(35,10),'#221c30':(49,0)}
for i,(l,c) in enumerate(pal): assert c in M,c
b=d['blocks']; half={}
for i in range(0,len(b),4):
    half[(b[i],b[i+1],b[i+2])]=M[pal[b[i+3]>>1][1]]
full=dict(half); coll=0
for (x,y,z),v in half.items():
    k=(119-x,y,173-z)
    if k in full: coll+=1
    full[k]=v
print(len(half),len(full),coll)
def dump(m,fn):
    json.dump([[x,y,z,v[0],v[1]] for (x,y,z),v in m.items()],open(fn,'w'),separators=(',',':'))
dump(half,'half.json'); dump(full,'full.json')
xs=[k[0] for k in full];zs=[k[2] for k in full];ys=[k[1] for k in full]
print(min(xs),max(xs),min(ys),max(ys),min(zs),max(zs))
