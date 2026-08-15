import os, sqlite3, json
from datetime import datetime
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
DB='skyheights.db'

def conn():
    c=sqlite3.connect(DB)
    c.execute('CREATE TABLE IF NOT EXISTS candidates(id INTEGER PRIMARY KEY,name TEXT,phone TEXT,city TEXT,experience REAL,role TEXT,status TEXT,interview TEXT,created TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS leads(id INTEGER PRIMARY KEY,name TEXT,phone TEXT,city TEXT,product TEXT,status TEXT,notes TEXT,created TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS employees(id INTEGER PRIMARY KEY,name TEXT,phone TEXT,role TEXT,joining TEXT,status TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS performance(id INTEGER PRIMARY KEY,employee TEXT,date TEXT,calls INTEGER,leads INTEGER,applications INTEGER,vkyc INTEGER,target INTEGER,achieved INTEGER)')
    c.commit(); return c
c=conn()

def add(table, cols, vals):
    q=f"INSERT INTO {table}({','.join(cols)}) VALUES({','.join(['?']*len(vals))})"
    c.execute(q,vals); c.commit()

def ai(q):
    if not os.getenv('OPENAI_API_KEY'):
        return 'AI is not connected yet. Add OPENAI_API_KEY in the cloud app secrets.'
    data={t:pd.read_sql_query(f'SELECT * FROM {t}',c).to_dict('records') for t in ['candidates','leads','employees','performance']}
    client=OpenAI(api_key=os.environ['OPENAI_API_KEY'])
    r=client.responses.create(model=os.getenv('OPENAI_MODEL','gpt-4.1-mini'),input=f'''You are the internal AI manager for Sky Heights Outsourcing Solutions. Use only this business data. Never invent figures. Give concise actionable answers. DATA={json.dumps(data,default=str)} QUESTION={q}''')
    return r.output_text

st.set_page_config(page_title='Sky Heights AI',page_icon='🤖',layout='wide')
st.title('🤖 SKY HEIGHTS AI')
st.caption('Recruitment • Sales • MIS • HR • Management')
t=st.tabs(['Dashboard','Recruitment','Sales Leads','Performance','HR','AI Manager'])
with t[0]:
    for label,table in [('Candidates','candidates'),('Leads','leads'),('Employees','employees'),('Performance rows','performance')]:
        st.metric(label,len(pd.read_sql_query(f'SELECT * FROM {table}',c)))
    st.subheader('Recent leads'); st.dataframe(pd.read_sql_query('SELECT * FROM leads ORDER BY id DESC LIMIT 20',c),use_container_width=True)
with t[1]:
    with st.form('cand'):
        n=st.text_input('Name'); p=st.text_input('Phone'); city=st.text_input('City'); exp=st.number_input('Experience',0.0,50.0,0.0); role=st.selectbox('Role',['Telecaller Executive','Team Leader','Other']); status=st.selectbox('Status',['New','Screening','Shortlisted','Interview','Selected','Rejected']); interview=st.text_input('Interview date/time')
        if st.form_submit_button('Save candidate'): add('candidates',['name','phone','city','experience','role','status','interview','created'],[n,p,city,exp,role,status,interview,datetime.now().isoformat()]); st.success('Candidate saved')
    st.dataframe(pd.read_sql_query('SELECT * FROM candidates ORDER BY id DESC',c),use_container_width=True)
with t[2]:
    with st.form('lead'):
        n=st.text_input('Lead name'); p=st.text_input('Lead phone'); city=st.text_input('City'); product=st.text_input('Product/campaign'); status=st.selectbox('Status',['New','Contacted','Interested','Application','vKYC','Converted','Follow-up','Not Interested']); notes=st.text_area('Notes')
        if st.form_submit_button('Save lead'): add('leads',['name','phone','city','product','status','notes','created'],[n,p,city,product,status,notes,datetime.now().isoformat()]); st.success('Lead saved')
    st.dataframe(pd.read_sql_query('SELECT * FROM leads ORDER BY id DESC',c),use_container_width=True)
with t[3]:
    with st.form('perf'):
        e=st.text_input('Agent'); d=st.date_input('Date'); calls=st.number_input('Calls',0); leads=st.number_input('Leads',0); apps=st.number_input('Applications',0); v=st.number_input('vKYC',0); target=st.number_input('Target',0); achieved=st.number_input('Achieved',0)
        if st.form_submit_button('Save performance'): add('performance',['employee','date','calls','leads','applications','vkyc','target','achieved'],[e,str(d),calls,leads,apps,v,target,achieved]); st.success('Performance saved')
    st.dataframe(pd.read_sql_query('SELECT * FROM performance ORDER BY id DESC',c),use_container_width=True)
with t[4]:
    with st.form('emp'):
        n=st.text_input('Employee name'); p=st.text_input('Phone'); role=st.text_input('Role'); joining=st.date_input('Joining date'); status=st.selectbox('Employee status',['Active','On Leave','Inactive'])
        if st.form_submit_button('Add employee'): add('employees',['name','phone','role','joining','status'],[n,p,role,str(joining),status]); st.success('Employee added')
    st.dataframe(pd.read_sql_query('SELECT * FROM employees ORDER BY id DESC',c),use_container_width=True)
with t[5]:
    q=st.text_area('Ask your AI Manager',placeholder='Example: Which agents are below target?')
    if st.button('Ask AI',type='primary') and q: st.write(ai(q))
