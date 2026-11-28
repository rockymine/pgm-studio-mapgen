import zipfile,sys,re,glob,os
for z in sorted(glob.glob(sys.argv[1]+'/*.zip')):
    zf=zipfile.ZipFile(z); names=zf.namelist()
    xmls=[n for n in names if re.search(r'(^|/)map\.xml$',n)]
    print('=====',os.path.basename(z),len(names),'files,',len(xmls),'map.xml')
    for n in sorted(xmls):
        x=zf.read(n).decode('utf-8','replace')
        g=lambda t:(re.search(r'<%s>([^<]*)</%s>'%(t,t),x) or [None,''])[1]
        obj=[k for k in ['wools','destroyables','cores','control-points','hills','flags','score'] if '<'+k in x]
        auth=re.findall(r'<author[^>]*>[^<]*</author>|<author[^/]*/>',x)
        auth=[re.sub(r'\s+',' ',a)[:90] for a in auth]
        com=re.findall(r'<!--\s*(.{1,50}?)\s*-->',x)[:3]
        print(' ',n.rsplit('/map.xml',1)[0] or '.','|',g('name'),'|',g('version'),'|',','.join(obj),'|',g('created'),'|',' / '.join(auth)[:200],'|',';'.join(com))
