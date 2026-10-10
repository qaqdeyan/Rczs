#!/usr/bin/env python3
"""Sync community Wiki Lua pet catalog to compact, image-free JSON."""
import datetime
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

UPSTREAM = "https://raw.githubusercontent.com/JayeGT002/rocom-wiki-data/main/data/wiki_modules/Pets/data/Catalog.lua"
EGGS = {1:"未发现",2:"巨灵组",3:"两栖组",4:"昆虫组",5:"天空组",6:"动物组",7:"妖精组",8:"植物组",9:"拟人组",10:"软体组",11:"大地组",12:"魔力组",13:"海洋组",14:"飞龙组",15:"机械组"}
def table(s,k):
    m = re.search(r"(?:^|[,{}])" + re.escape(k) + r"=\{",s)
    if not m:return ""
    start=m.end()-1
    depth=0; quote=False; escape=False
    for i in range(start,len(s)):
        c=s[i]
        if quote:
            if escape:escape=False
            elif c=="\\":escape=True
            elif c=='"':quote=False
        elif c=='"':quote=True
        elif c=="{":depth+=1
        elif c=="}":
            depth-=1
            if depth==0:return s[start:i+1]
    return ""
def txt(s,k):
    m=re.search(r'(?:^|[,{}])'+re.escape(k)+r'="((?:\\.|[^"\\])*)"',s)
    return json.loads('"'+m.group(1)+'"') if m else ""
def nums(s):
    return {k:int(v) for k,v in re.findall(r"(?:^|[,{}])([a-z_]+)=(-?\d+)",s)}
def terms(s):
    return [json.loads('"'+x+'"') for x in re.findall(r'"((?:\\.|[^"\\])*)"',s)]
def image(name):
    if not re.fullmatch(r"[^/\\?#]{1,180}\.(png|jpe?g|webp)",name,re.I):return ""
    return "https://wiki.biligame.com/nrc/Special:Redirect/file/"+urllib.parse.quote(name,safe="")
def normalize(s):
    identity=re.match(r"pet_\d{6}",s)
    if not identity:return None
    n=txt(s,"number")
    name=txt(s,"title") or txt(s,"name")
    if not n or not name:return None
    im=table(s,"image")
    props=nums(s)
    egg=re.findall(r"\d+",table(s,"egg_group"))
    return dict(
        id=identity.group(),number=str(n).zfill(3),name=name,
        types=[t.removesuffix("系") for t in terms(table(s,"types"))],
        form=("首领形态" if "首领" in name else "地区形态" if "地区" in name else "主形态"),
        stage=(str(props["stage"])+"阶" if props.get("stage") else ""),
        egg_group=" / ".join(EGGS.get(int(x),x) for x in egg),
        season="",description=txt(s,"description"),trait=txt(s,"feature_name"),
        trait_effect="",height=txt(s,"height"),weight=txt(s,"weight"),
        stats=nums(table(s,"stats")),avatar_url=image(txt(im,"head")),
        portrait_url=image(txt(im,"illustration")),
        source_url="https://wiki.biligame.com/nrc/"+urllib.parse.quote(name,safe="")
    )
def main():
    req=urllib.request.Request(UPSTREAM,headers={"User-Agent":"Rczs-RocoDex-Index/1.0"})
    with urllib.request.urlopen(req,timeout=35) as r:
        source=r.read(7*1024*1024).decode("utf-8")
    blocks=re.split(r"(?=pet_\d{6}=\{)",source)[1:]
    unique={}
    for block in blocks:
        pet=normalize(block)
        if pet:unique[pet["id"]]=pet
    records=sorted(unique.values(),key=lambda r:(int(r["number"]),r["id"]))
    if not 500<=len(records)<=3000 or sum(bool(x["portrait_url"]) for x in records)<len(records)*0.9:
        raise ValueError("Catalog incomplete; keeping previous index")
    path=Path("site/pokedex.json")
    if path.exists():
        prev=json.loads(path.read_text(encoding="utf-8"))
        if len(records)<0.75*len(prev.get("records",[])):raise ValueError("Index shrank unexpectedly")
        if records==prev.get("records"):print("No update");return
    result={"schema_version":2,"updated_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"source":"Rocom Wiki community mirror","source_url":"https://github.com/JayeGT002/rocom-wiki-data","license":"Community text CC BY-NC-SA 4.0; artwork belongs to respective rights holders","record_count":len(records),"records":records}
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,ensure_ascii=False,separators=(",",":"))+"\n",encoding="utf-8")
    print("Updated",len(records),"pets; images downloaded: 0")
if __name__=="__main__":main()
