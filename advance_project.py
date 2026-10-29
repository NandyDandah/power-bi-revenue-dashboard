"""Rebuild reproducible synthetic portfolio data and report queries."""
from pathlib import Path
import random, re, json, datetime as dt
from collections import defaultdict

ROOT = Path(__file__).resolve().parent
TABLES = ROOT / 'Power BI Project.SemanticModel/definition/tables'
rng = random.Random(20261029)
data = {}
for name in ('customers', 'products', 'sales_reps'):
    text = (TABLES / f'public {name}.tmdl').read_text(encoding='utf-8-sig')
    body = text.split('type table [',1)[1].split('],',1)[1].split('\n\tannotation',1)[0].strip()
    body = body[:body.rfind(')')].strip()
    body = re.sub(r'#datetime\((\d+), (\d+), (\d+), 0, 0, 0\)', lambda m: json.dumps(f'{int(m[1]):04}-{int(m[2]):02}-{int(m[3]):02}'), body)
    data[name] = json.loads(body.replace('{','[').replace('}',']'))[:8 if name=='customers' else 4]
for i in range(9,121):
    data['customers'].append([i, f'Demo Account {i:03}', ['Enterprise','Mid-Market','SMB'][i%3], ['North','South','West','East'][i%4], '2024-01-01'])
for i, name in enumerate(['Alex Morgan','Sam Rivera','Taylor Brooks','Robin Lee'],5):
    data['sales_reps'].append([i,name,'Growth' if i%2 else 'Enterprise',['North','South','West','East'][(i-1)%4]])
data['orders']=[]; data['opportunities']=[]; data['sales_activities']=[]
for month in range(24):
    year, mon = 2024+month//12, month%12+1
    for j in range(65 + month*2 + (20 if mon in (6,11,12) else 0)):
        c=rng.choice(data['customers']); p=rng.choice(data['products']); rep=rng.randrange(1,9)
        date=f'{year}-{mon:02}-{rng.randrange(1,29):02}'
        quantity=rng.randrange(1,5); discount=rng.choice([0,0,.03,.05,.10,.15])
        data['orders'].append([1001+len(data['orders']),c[0],p[0],rep,date,quantity,discount,round(p[3]*quantity*(1-discount),2)])
    for j in range(45):
        oid=2001+len(data['opportunities']); date=f'{year}-{mon:02}-{rng.randrange(1,25):02}'
        stage=rng.choices(['Closed Won','Closed Lost','Discovery','Proposal','Negotiation'],[40,20,15,15,10])[0]
        data['opportunities'].append([oid,rng.randrange(1,121),rng.randrange(1,9),date,stage,rng.randrange(5,100)*1000,stage=='Closed Won'])
        for kind in ('Discovery Call','Demo','Follow-up'):
            data['sales_activities'].append([3001+len(data['sales_activities']),oid,date,kind])
monthly=defaultdict(list)
for o in data['orders']: monthly[o[4][:7]].append(o)
data['vw_revenue_trends']=[]; data['vw_customer_retention']=[]
prior=set()
for month, orders in sorted(monthly.items()):
    customers={o[1] for o in orders}; total=round(sum(o[7] for o in orders),2)
    data['vw_revenue_trends'].append([month+'-01',total,len(orders),len(customers),round(total/len(orders),2)])
    retained=len(customers & prior)
    data['vw_customer_retention'].append([month+'-01',len(customers),retained,retained/len(customers)])
    prior=customers
data['vw_sales_funnel']=[]
for stage in ['Discovery','Proposal','Negotiation','Closed Won','Closed Lost']:
    rows=[o for o in data['opportunities'] if o[4]==stage]
    data['vw_sales_funnel'].append([stage,len(rows),sum(o[5] for o in rows),sum(o[6] for o in rows),sum(o[6] for o in rows)/len(rows)])
data['vw_rep_performance']=[]
for rep in data['sales_reps']:
    rows=[o for o in data['orders'] if o[3]==rep[0]]; total=round(sum(o[7] for o in rows),2)
    data['vw_rep_performance'].append(rep[1:]+[len(rows),total,round(total/len(rows),2),len({o[1] for o in rows})])
total=round(sum(o[7] for o in data['orders']),2)
data['vw_kpi_summary']=[[total,len(data['orders']),120,round(total/len(data['orders']),2)]]
sql=['-- Synthetic portfolio data; deterministic seed 20261029. Load into an empty schema.']
for name, rows in data.items():
    path=TABLES/f'public {name}.tmdl'; text=path.read_text(encoding='utf-8-sig')
    schema=re.search(r'type table \[([^]]+)\]',text)[1]
    fields=[x.strip().split(' = ') for x in schema.split(',')]
    assert all(len(row)==len(fields) for row in rows),name
    def mvalue(v,typ):
        if typ=='datetime':
            d=dt.date.fromisoformat(v); return f'#datetime({d.year}, {d.month}, {d.day}, 0, 0, 0)'
        return json.dumps(v)
    body=',\n'.join('\t\t\t\t    {'+', '.join(mvalue(v,typ) for v,(_,typ) in zip(row,fields))+'}' for row in rows)
    source=f'\t\t\t\t#table(type table [{schema}], {{\n{body}\n\t\t\t\t}})\n'
    start=text.index('\t\t\tsource =') if '\t\t\tsource =' in text else text.index('\t\tsource =')
    end=text.find('\n\tannotation',start)
    text=text[:start]+'\t\tsource =\n'+source+(text[end:] if end>=0 else '')
    path.write_text(text,encoding='utf-8')
    if not name.startswith('vw_'):
        def sqlv(v):
            if isinstance(v,str): return "'"+v.replace("'","''")+"'"
            return str(v).lower()
        sql.append('INSERT INTO public.'+name+' ('+', '.join(f[0] for f in fields)+') VALUES\n'+',\n'.join('('+', '.join(sqlv(v) for v in row)+')' for row in rows)+';')
(ROOT/'SQL/02_insert_sample_data.sql').write_text('\n\n'.join(sql)+'\n',encoding='utf-8')
assert len({o[0] for o in data['orders']})==len(data['orders'])
assert all(1<=o[1]<=120 and 1<=o[3]<=8 for o in data['orders'])
assert round(sum(r[1] for r in data['vw_revenue_trends']),2)==total
print(json.dumps({'orders':len(data['orders']),'customers':120,'reps':8,'opportunities':1080,'activities':3240,'months':24,'revenue':total},indent=2))

# Use one field per slicer to avoid unsupported cross-table hierarchies.
pages=ROOT/'Power BI Project.Report/definition/pages'
def projection(entity, prop, measure=False):
    return {'field':{'Measure' if measure else 'Column':{'Expression':{'SourceRef':{'Entity':entity}},'Property':prop}},'queryRef':entity+'.'+prop,'nativeQueryRef':prop,'active':True}
for path in pages.rglob('visual.json'):
    obj=json.loads(path.read_text()); v=obj['visual']; q=v.get('query',{}).get('queryState',{})
    if v['visualType']=='slicer':
        for role in q.values(): role['projections']=role['projections'][:1]
        if obj['name']=='5dfcf9680cd8b4ecd557':
            q['Values']['projections']=[projection('public opportunities','stage')]
    if v['visualType']=='lineChart':
        retention='b3bec9dbd6b0a8070c5e' in str(path)
        entity='public vw_customer_retention' if retention else 'public vw_revenue_trends'
        prop='order_month' if retention else 'month'
        q['Category']={'projections':[projection(entity,prop)]}
        field=projection(entity,'retention_rate' if retention else 'total_revenue')['field']
        agg={'Aggregation':{'Expression':field,'Function':1 if retention else 0}}
        q['Y']={'projections':[{'field':agg,'queryRef':entity+'.value','nativeQueryRef':'Returning customer share' if retention else 'Revenue'}]}
        q.pop('Y2',None)
        v['query']['sortDefinition']={'sort':[{'field':projection(entity,prop)['field'],'direction':'Ascending'}]}
        v.setdefault('visualContainerObjects',{})['title']=[{'properties':{'text':{'expr':{'Literal':{'Value':"'Monthly returning customer share'" if retention else "'Monthly revenue | 2024-2025'"}}}}}]
    path.write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8')
measures=TABLES/'Revenue_measures.tmdl'
text=measures.read_text()
text=text.replace("'public opportunities'[is_won] = FALSE()", "'public opportunities'[stage] = \"Closed Lost\"")
text=text.replace("measure 'Total Pipeline Value' = SUM('public opportunities'[estimated_value])", "measure 'Total Pipeline Value' = CALCULATE(SUM('public opportunities'[estimated_value]), NOT('public opportunities'[stage] IN {\"Closed Won\", \"Closed Lost\"}))")
text=text.replace('SUM(\'public vw_customer_retention\'[active_customers])','AVERAGE(\'public vw_customer_retention\'[active_customers])')
text=text.replace('measure \'Revenue Target\' = 750000','measure \'Revenue Target\' = 65000000')
text=text.replace('\\$#,0.###############;(\\$#,0.###############);\\$#,0.###############','\\$#,0;(\\$#,0);\\$0')
measures.write_text(text,encoding='utf-8')

import copy
executive=pages/'35a40d734aacba3e25ff'
trend=executive/'visuals/be1469aff5469100459f/visual.json'
obj=json.loads(trend.read_text()); obj['position'].update(height=240)
trend.write_text(json.dumps(obj,indent=2)+'\n')
template=json.loads((pages/'c0de5a1e5a1e00000001/visuals/a0000000000000000007/visual.json').read_text())
for index,(name,entity,field,title) in enumerate([
    ('portfolioProductRevenue','public products','product_name','Revenue by product'),
    ('portfolioSegmentRevenue','public customers','segment','Revenue by customer segment')]):
    obj=copy.deepcopy(template); obj['name']=name
    obj['position'].update(x=32+index*616,y=488,width=600,height=200,z=9000+index,tabOrder=9000+index)
    obj['visual']['query']['queryState']={'Category':{'projections':[projection(entity,field)]},'Y':{'projections':[projection('Revenue_measures','Total Revenue',True)]}}
    obj['visual']['visualContainerObjects']['title']=[{'properties':{'text':{'expr':{'Literal':{'Value':"'"+title+"'"}}}}}]
    target=executive/'visuals'/name; target.mkdir(exist_ok=True)
    (target/'visual.json').write_text(json.dumps(obj,indent=2)+'\n')
