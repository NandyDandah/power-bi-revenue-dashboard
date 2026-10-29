"""Apply presentation and filter-aware analytical fixes after generating data."""
from pathlib import Path
import json, re, copy
R=Path(__file__).resolve().parent
T=R/'Power BI Project.SemanticModel/definition/tables'
P=R/'Power BI Project.Report/definition/pages'
date='LocalDateTable_c51026c0-8e8c-4070-ab05-1ee43b05a57e'
def save(p,o): p.write_text(json.dumps(o,indent=2)+'\n',encoding='utf-8')
def lit(x): return {'expr':{'Literal':{'Value':x}}}
def col(e,p): return {'Column':{'Expression':{'SourceRef':{'Entity':e}},'Property':p}}
def measure(p): return {'Measure':{'Expression':{'SourceRef':{'Entity':'Revenue_measures'}},'Property':p}}
def proj(f,label): return {'field':f,'queryRef':label,'nativeQueryRef':label,'active':True}
path=T/(date+'.tmdl'); text=path.read_text()
if '\tcolumn MonthStart ' not in text:
    text=text.replace('\thierarchy', '\tcolumn MonthStart = DATE(YEAR([Date]), MONTH([Date]), 1)\n\t\tdataType: dateTime\n\t\tformatString: MMM yyyy\n\t\tsummarizeBy: none\n\n\thierarchy',1)
path.write_text(text,encoding='utf-8')
path=T/'Revenue_measures.tmdl'; text=path.read_text()
def setmeasure(name,expr):
    global text
    expr=' '.join(expr.split())
    text=re.sub(r"(\tmeasure '"+re.escape(name)+r"' =)\s*.*?(?=\n\t\tformatString:)",lambda m:m[1]+' '+expr,text,flags=re.S)
setmeasure('Retention Rate',f'''VAR CurrentCustomers = VALUES('public orders'[customer_id])
            VAR PriorCustomers = CALCULATETABLE(VALUES('public orders'[customer_id]), DATEADD('{date}'[Date], -1, MONTH))
            RETURN DIVIDE(COUNTROWS(INTERSECT(CurrentCustomers, PriorCustomers)), COUNTROWS(CurrentCustomers))''')
setmeasure('Monthly Active Customers',f"AVERAGEX(VALUES('{date}'[MonthStart]), CALCULATE([Active Customers]))")
setmeasure('Total Pipeline Value', "CALCULATE(SUM('public opportunities'[estimated_value]), KEEPFILTERS(NOT('public opportunities'[stage] IN {\"Closed Won\", \"Closed Lost\"})))")
path.write_text(text,encoding='utf-8')
for path in P.rglob('visual.json'):
    o=json.loads(path.read_text()); v=o['visual']; typ=v['visualType']; q=v.get('query',{}).get('queryState',{})
    if typ=='lineChart':
        retention='b3bec9dbd6b0a8070c5e' in str(path)
        q['Category']={'projections':[proj(col(date,'MonthStart'),'Month')]}
        q['Y']={'projections':[proj(measure('Retention Rate' if retention else 'Total Revenue'),'Returning customer share' if retention else 'Revenue')]}
        if 'c0de5a1e5a1e00000001' in str(path): q['Y']['projections'].append(proj(measure('Revenue Previous Year'),'Prior year'))
        v['query']['sortDefinition']={'sort':[{'field':col(date,'MonthStart'),'direction':'Ascending'}]}
    if typ=='cardVisual':
        # Classic cards provide predictable labels and compact number formatting.
        role=q.get('Data',{}); fields=role.get('projections',[])
        if fields:
            v['visualType']='card'; v['query']['queryState']={'Values':{'projections':fields}}
            v['objects']={'labels':[{'properties':{'fontSize':lit('23D'),'labelPrecision':lit('1L'),'color':{'solid':{'color':lit("'#202B35'")}}}}], 'categoryLabels':[{'properties':{'show':lit('true'),'fontSize':lit('10D')}}]}
            v['visualContainerObjects'].pop('title',None)
    if typ not in ('textbox','slicer','cardVisual'):
        v.setdefault('objects',{})['dataPoint']=[{'properties':{'defaultColor':{'solid':{'color':lit("'#7188E8'")}}}}]
    save(path,o)
executive=P/'35a40d734aacba3e25ff'
template=json.loads((executive/'visuals/portfolioProductRevenue/visual.json').read_text())
for name,entity,field,title,pos,typ in [
 ('portfolioRegionRevenue','public customers','region','Regional revenue contribution',(900,232,348,220),'clusteredColumnChart'),
 ('portfolioDiscountRevenue','public orders','discount','Revenue by discount rate',(448,472,384,216),'clusteredBarChart')]:
    o=copy.deepcopy(template); o['name']=name
    o['position'].update(x=pos[0],y=pos[1],width=pos[2],height=pos[3],z=9500,tabOrder=9500)
    v=o['visual']; v['visualType']=typ
    v['query']['queryState']={'Category':{'projections':[proj(col(entity,field),field)]},'Y':{'projections':[proj(measure('Total Revenue'),'Revenue')]}}
    v['visualContainerObjects']['title']=[{'properties':{'text':lit("'"+title+"'")}}]
    d=executive/'visuals'/name; d.mkdir(exist_ok=True); save(d/'visual.json',o)
for name,pos in {'be1469aff5469100459f':(32,232,848,220),'portfolioProductRevenue':(32,472,396,216),'portfolioSegmentRevenue':(852,472,396,216)}.items():
    path=executive/'visuals'/name/'visual.json'; o=json.loads(path.read_text()); o['position'].update(x=pos[0],y=pos[1],width=pos[2],height=pos[3]); save(path,o)
path=P/'pages.json'; o=json.loads(path.read_text()); o['activePageName']=o['pageOrder'][0]; save(path,o)
for path in P.rglob('visual.json'):
    o=json.loads(path.read_text()); p=o['position']
    assert p['x']>=0 and p['y']>=0 and p['x']+p['width']<=1280 and p['y']+p['height']<=720,path
print('Report JSON and visual bounds validated.')

# Section accents identify pages; categorical charts retain a varied palette.
section_colors={
    '35a40d734aacba3e25ff':('#2563EB','#EFF6FF'),
    'b3bec9dbd6b0a8070c5e':('#0F766E','#F0FDFA'),
    'eae489f85a747848cfbe':('#B45309','#FFFBEB'),
    'c0de5a1e5a1e00000001':('#7C3AED','#F5F3FF'),
}
chart_colors=['#2563EB','#0F766E','#C2410C','#7C3AED','#BE185D','#047857']
for directory in (p for p in P.iterdir() if p.is_dir()):
    accent,tint=section_colors[directory.name]
    chart_index=0
    for path in sorted(directory.rglob('visual.json')):
        o=json.loads(path.read_text()); v=o['visual']; typ=v['visualType']
        objects=v.setdefault('objects',{})
        containers=v.setdefault('visualContainerObjects',{})
        if typ=='textbox':
            for paragraph in objects.get('general',[{}])[0].get('properties',{}).get('paragraphs',[]):
                for run in paragraph.get('textRuns',[]): run.setdefault('textStyle',{})['color']=accent
        elif typ in ('card','cardVisual','slicer'):
            containers['background']=[{'properties':{'color':{'solid':{'color':lit("'"+tint+"'")}},'transparency':lit('0D')}}]
            if typ=='card': objects['labels'][0]['properties']['color']={'solid':{'color':lit("'"+accent+"'")}}
        else:
            color=chart_colors[chart_index%len(chart_colors)]; chart_index+=1
            if typ in ('donutChart','pieChart','lineChart'):
                objects.pop('dataPoint',None)
            else:
                objects['dataPoint']=[{'properties':{'defaultColor':{'solid':{'color':lit("'"+color+"'")}}}}]
            title=containers.get('title',[{'properties':{}}])
            title[0]['properties']['fontColor']={'solid':{'color':lit("'"+color+"'")}}
            containers['title']=title
        save(path,o)
theme_path=R/'Power BI Project.Report/StaticResources/SharedResources/BaseThemes/CY26SU04.json'
theme=json.loads(theme_path.read_text())
theme['dataColors']=['#2563EB','#D97706','#0F766E','#7C3AED','#BE185D','#65A30D','#0891B2','#DC2626']
save(theme_path,theme)
print('Applied blue, teal, amber and violet section accents with contrasting chart series.')
