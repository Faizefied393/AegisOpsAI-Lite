"""CISA KEV enrichment. Never turn absence from KEV into proof of safety."""
import json
from pathlib import Path
import requests
KEV_URL='https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json'
DEMO_CVES={'FIN-DB01':['CVE-2021-44228'],'FIN-DC01':['CVE-2021-44228']}

def enrich(asset, catalog=None):
    if catalog is None:
        catalog=json.loads((Path(__file__).resolve().parents[1]/'data/kev_sample.json').read_text())
    known={x['cveID']:x for x in catalog.get('vulnerabilities',[])}
    return [{'cve':cve,'in_kev':cve in known,'vendor':known.get(cve,{}).get('vendorProject','unknown')} for cve in DEMO_CVES.get(asset,[])]

def fetch_live(timeout=12):
    response=requests.get(KEV_URL,timeout=timeout)
    response.raise_for_status()
    data=response.json()
    if not isinstance(data.get('vulnerabilities'),list):raise ValueError('Unexpected KEV schema')
    return data
