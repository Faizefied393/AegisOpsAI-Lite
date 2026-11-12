import os
import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title='AegisOps AI Lite',page_icon='🛡️',layout='wide')
st.title('🛡️ AegisOps AI Lite')
st.caption('Enterprise-style security operations and business risk | SYNTHETIC DATA')
api=st.sidebar.text_input('API URL',value=os.getenv('API_BASE','http://127.0.0.1:8000'))
key=st.sidebar.text_input('Demo API key',value=os.getenv('AEGIS_API_KEY',''),type='password')
st.sidebar.warning('Use synthetic data only. Do not enter production secrets or real customer data.')
def call(method,path):
    try:
        r=requests.request(method,api.rstrip('/')+path,headers={'X-API-Key':key},timeout=60)
        r.raise_for_status();return r.json()
    except requests.RequestException as exc:
        st.error(f'API request failed: {exc}');return None
if st.sidebar.button('Seed synthetic demo'):
    if call('POST','/demo/seed') is not None: st.success('Synthetic demo events loaded')
if not key:
    st.info('Enter the API key configured in your backend environment, then seed the demo.');st.stop()
metrics=call('GET','/metrics')
if metrics is None:st.stop()
a,b,c,d=st.columns(4)
a.metric('Security events',metrics['events']);b.metric('Unconfirmed alerts',metrics['alerts'])
c.metric('High risk alerts',metrics['high_risk_alerts']);d.metric('Highest risk score',metrics['highest_risk'])
t1,t2,t3=st.tabs(['SOC alerts','AI investigation','Executive risk'])
alerts=call('GET','/alerts') or []
with t1:
    st.subheader('Detection queue')
    if alerts:
        df=pd.DataFrame(alerts);st.dataframe(df[['id','rule','asset','risk_score','severity','confidence','status']],use_container_width=True)
        st.bar_chart(df.set_index('rule')['risk_score'])
    else:st.info('No alerts yet. Seed the demo.')
with t2:
    st.subheader('Evidence-grounded incident assessment')
    if alerts:
        choice=st.selectbox('Select alert',[a['id'] for a in alerts])
        if st.button('Investigate with local Ollama'):
            result=call('POST',f'/alerts/{choice}/investigate')
            if result:
                st.info('Mode: '+result['mode']);st.json(result)
    st.caption('AI reports are advisory. No automated containment actions are exposed.')
with t3:
    st.subheader('Business risk prioritization')
    st.write('Prioritize analyst review using severity (40%), asset criticality (35%), and confidence (25%).')
    st.write('Risk is a heuristic prioritization score, not a probability of compromise.')
    if alerts:
        st.dataframe(pd.DataFrame(alerts)[['asset','rule','risk_score','explanation']],use_container_width=True)
    st.markdown('**Executive interpretation:** Validate high-risk alerts first, confirm affected business assets, and document decisions. Do not equate alerts with confirmed breaches.')

st.divider()
st.subheader('AegisOps AI X — Seven technology extensions')
st.caption('Sigma rule selection · KEV offline fixture · synthetic ML baseline · LangGraph human review · promptfoo · OpenTelemetry · Trivy')
left,right=st.columns(2)
with left:
    if st.button('Inspect Sigma rule matches'):
        result=call('GET','/extensions/sigma')
        if result:st.json(result)
    if st.button('Inspect KEV demo enrichment'):
        result=call('GET','/extensions/kev/FIN-DB01')
        if result:st.json(result)
with right:
    if st.button('Evaluate synthetic ML baseline'):
        result=call('GET','/extensions/ml')
        if result:st.json(result)
    if alerts and st.button('Run LangGraph review workflow'):
        result=call('POST',f"/extensions/agent/{alerts[0]['id']}")
        if result:st.json(result)
