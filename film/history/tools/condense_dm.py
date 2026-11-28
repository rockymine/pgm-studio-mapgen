import sys,re
lines=open(sys.argv[1],encoding='utf-8').read().split('\n')
out=[];cur=None;author='?';buf=[]
def flush():
    if cur: 
        t=' / '.join(x for x in buf if x)
        out.append(f"{cur[:16]} {author[:2]}: {t[:600]}")
skip=re.compile(r'^(\[|\]| — |\d{1,2}:\d\d [AP]M|\d+/\d+/\d+, .*[AP]M|Modify Attachment|Delete|Add Reaction|\d+|Expand \(.*|.*\(\d+ KB\)|\d+ KB|Image|Edit)$')
i=0
while i<len(lines):
    l=lines[i]
    m=re.match(r'^=== (\S+) ',l)
    if m:
        flush();cur=m.group(1);buf=[]
        # author line next if followed by ' — '
        if i+2<len(lines) and lines[i+2].strip()=='—' or (i+2<len(lines) and lines[i+2]==' — '):
            author=lines[i+1].strip(); i+=2
        i+=1;continue
    s=l.strip()
    if skip.match(s) or not s: i+=1;continue
    if s.startswith('[attachments]'): s='[att]'
    s=re.sub(r'https://cdn\.discordapp\S+','',s)
    buf.append(s); i+=1
flush()
open(sys.argv[2],'w',encoding='utf-8').write('\n'.join(out))
