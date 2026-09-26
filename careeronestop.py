# --- Imports ---
import pandas as pd
import requests
from lxml import html

# --- Load file configuration ---
site_config = pd.read_csv('/Users/yanha/Downloads/data.csv')

def convert_headers(raw_header):
    header = dict()
    for line in raw_header.split("\n"):
        a,b = line.split(":",1)
        header[a.strip()] = b.strip()
    return header


raw_header='''user-agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'''

headers=convert_headers(raw_header)

# --- Fetch and parse CareerOneStop scholarship list page ---
url=site_config[site_config.site_name=='CareerOneStop'].site_link.values[0]
r=requests.get(url,headers=headers)
raw_html=r.content.decode()
tree = html.fromstring(raw_html)

# --- Extract fields via config-defined XPaths ---
award_name = tree.xpath(site_config[site_config.site_name=='CareerOneStop'].award_name_xpath.values[0])        
award_link = tree.xpath(site_config[site_config.site_name=='CareerOneStop'].award_link_xpath.values[0])        
award_amount = tree.xpath(site_config[site_config.site_name=='CareerOneStop'].award_amount_xpath.values[0])
award_deadline = tree.xpath(site_config[site_config.site_name=='CareerOneStop'].deadline_xpath.values[0])        

# --- Clean extracted text ---
award_name=[award.strip() for award in award_name]
award_link=[award.strip() for award in award_link]
award_amount=[award.strip() for award in award_amount]
award_deadline=[award.strip() for award in award_deadline]


careeronestop_scholarships=pd.DataFrame({'award_name':award_name,'award_link':award_link,'level_of_study':'High School','award_amount':award_amount,'deadline_month':award_deadline})

# NOTE: hardcoded to this machine's local Downloads folder - update path before running
output = '/Users/yanha/Downloads/CareerOneStop.csv'
careeronstop_scholarships.to_csv(output, index=False)

# --- Static confirmation message ---
print(f"\nUpdated DataFrame potentially saved to '{output}'")
