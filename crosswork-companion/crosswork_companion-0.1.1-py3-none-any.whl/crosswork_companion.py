import os
import json
import requests
import aiohttp
import asyncio
import aiofiles
import rich_click as click
import yaml
import urllib3
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

urllib3.disable_warnings()

class CrossworkCompanion():
    def __init__(self,
                url,
                username,
                password):
        self.crosswork = url
        self.username = username
        self.password = password

    def crosswork_companion(self):
        self.make_directories()
        self.ticket = self.get_ticket()
        self.token = self.get_token(self.ticket)
        asyncio.run(self.main())

    def make_directories(self):
        api_list = ['Health Information/KPI Mgmt Query',
                    'YANG Modules'
        
        ]
        current_directory = os.getcwd()
        for api in api_list:
            final_directory = os.path.join(current_directory, rf'{ api }/JSON')
            os.makedirs(final_directory, exist_ok=True)
            final_directory = os.path.join(current_directory, rf'{ api }/YAML')
            os.makedirs(final_directory, exist_ok=True)
            final_directory = os.path.join(current_directory, rf'{ api }/CSV')
            os.makedirs(final_directory, exist_ok=True)
            final_directory = os.path.join(current_directory, rf'{ api }/HTML')
            os.makedirs(final_directory, exist_ok=True)
            final_directory = os.path.join(current_directory, rf'{ api }/Markdown')
            os.makedirs(final_directory, exist_ok=True)
            final_directory = os.path.join(current_directory, rf'{ api }/Mindmap')
            os.makedirs(final_directory, exist_ok=True)

    def get_ticket(self):
        payload = ""
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/plain',
        }
        url = f"{ self.crosswork }:30603/crosswork/sso/v1/tickets?username={self.username}&password={self.password}"
        ticket_request_reponse = requests.request("POST", url, headers=headers, data=payload, verify=False)
        print(f"<Authentication Status code {ticket_request_reponse.status_code} for { url }>")
        return ticket_request_reponse.text

    def get_token(self,ticket):
        payload = "service=https://198.18.134.219/app-dashboard"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/plain',
        }        
        url = f"{ self.crosswork }:30603/crosswork/sso/v1/tickets/{ ticket }"
        ticket_response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        print(f"<Authentication Status code {ticket_response.status_code} for { url }>")
        return ticket_response.text

    api_list = ["/crosswork/hi/v1/kpimgmt/query",
                "/crosswork/nca/v1/yang/modules"
            ]
    async def get_api(self, api_url):
        headers = {
            'Authorization': f'Bearer { self.token }',
            'Content-Type': 'application/json'
            }
        if api_url == "/crosswork/hi/v1/kpimgmt/query":
            payload = json.dumps({
                "kpis": [
                    "pulse_cpu_utilization",
                    "pulse_cpu_threshold",
                    "pulse_cef_drops",
                    "pulse_device_uptime",
                    "pulse_ethernet_port_error_counters",
                    "pulse_ethernet_port_packet_size_distribution",
                    "pulse_interface_packet_counters",
                    "pulse_interface_qos_egress",
                    "pulse_interface_qos_ingress",
                    "pulse_interface_rate_counters",
                    "pulse_memory_utilization"
                ],
                "limit": 1,
                "offset": 0,
                "sort_field": "details",
                "descending_order": False
            })
            session_post = True
        else:
            session_post = False
        async with aiohttp.ClientSession() as session:
            if session_post:
                async with session.post(f"{self.crosswork}:30603{api_url}",headers = headers, data=payload, verify_ssl=False) as resp:
                    raw_response_dict = await resp.text()
                    response_dict = json.loads(raw_response_dict)
                    print(f"{api_url} Status Code {resp.status}")
                    return (api_url,response_dict)
            else:
                async with session.get(f"{self.crosswork}:30603{api_url}",headers = headers, verify_ssl=False) as resp:
                    raw_response_dict = await resp.text()
                    response_dict = json.loads(raw_response_dict)
                    print(f"{api_url} Status Code {resp.status}")
                    return (api_url,response_dict)

    async def main(self):
        results = await asyncio.gather(*(self.get_api(api_url) for api_url in self.api_list))
        await self.all_files(json.dumps(results, indent=4, sort_keys=True))

    async def json_file(self, parsed_json):
        for api, payload in json.loads(parsed_json):
            if "/crosswork/hi/v1/kpimgmt/query" in api:
                async with aiofiles.open('Health Information/KPI Mgmt Query/JSON/Health Information KPI Mgmt Query.json', mode='w') as f:
                    await f.write(json.dumps(payload, indent=4, sort_keys=True))

            if "/crosswork/nca/v1/yang/modules" in api:
                async with aiofiles.open('YANG Modules/JSON/YANG Modules.json', mode='w') as f:
                    await f.write(json.dumps(payload, indent=4, sort_keys=True))

    async def yaml_file(self, parsed_json):
        for api, payload in json.loads(parsed_json):
            clean_yaml = yaml.dump(payload, default_flow_style=False)
            if "/crosswork/hi/v1/kpimgmt/query" in api:
                async with aiofiles.open('Health Information/KPI Mgmt Query/YAML/Health Information KPI Mgmt Query.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "/crosswork/nca/v1/yang/modules" in api:
                async with aiofiles.open('YANG Modules/YAML/YANG Modules.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

    async def csv_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        csv_template = env.get_template('crosswork_companion_csv.j2')
        for api, payload in json.loads(parsed_json):        
            csv_output = await csv_template.render_async(api = api,
                                         data_to_template = payload)
            if "/crosswork/hi/v1/kpimgmt/query" in api:
                async with aiofiles.open('Health Information/KPI Mgmt Query/CSV/Health Information KPI Mgmt Query.csv', mode='w' ) as f:
                    await f.write(csv_output)

                csv_output = await csv_template.render_async(api = "kpimgmt_query_alert_outputs",
                                         data_to_template = payload)
                async with aiofiles.open('Health Information/KPI Mgmt Query/CSV/Health Information KPI Mgmt Query Alert Output.csv', mode='w' ) as f:
                    await f.write(csv_output)

                csv_output = await csv_template.render_async(api = "kpimgmt_query_dashboards",
                                         data_to_template = payload)
                async with aiofiles.open('Health Information/KPI Mgmt Query/CSV/Health Information KPI Mgmt Query Dashboards.csv', mode='w' ) as f:
                    await f.write(csv_output)

                csv_output = await csv_template.render_async(api = "kpimgmt_query_scripts",
                                         data_to_template = payload)
                async with aiofiles.open('Health Information/KPI Mgmt Query/CSV/Health Information KPI Mgmt Query Scripts.csv', mode='w' ) as f:
                    await f.write(csv_output)

                csv_output = await csv_template.render_async(api = "kpimgmt_query_sensor_groups",
                                         data_to_template = payload)
                async with aiofiles.open('Health Information/KPI Mgmt Query/CSV/Health Information KPI Mgmt Query Sensor Groups.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "/crosswork/nca/v1/yang/modules" in api:
                async with aiofiles.open('YANG Modules/CSV/YANG Modules.csv', mode='w' ) as f:
                    await f.write(csv_output)

    async def markdown_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        markdown_template = env.get_template('crosswork_companion_markdown.j2')
        for api, payload in json.loads(parsed_json):        
            markdown_output = await markdown_template.render_async(api = api,
                                         data_to_template = payload)
            if "/crosswork/hi/v1/kpimgmt/query" in api:
                async with aiofiles.open('Health Information/KPI Mgmt Query/Markdown/Health Information KPI Mgmt Query.md', mode='w' ) as f:
                    await f.write(markdown_output)
            
                markdown_output = await markdown_template.render_async(api = "kpimgmt_query_alert_outputs",
                                             data_to_template = payload)
                                             
                async with aiofiles.open('Health Information/KPI Mgmt Query/Markdown/Health Information KPI Mgmt Query Alert Output.md', mode='w' ) as f:
                    await f.write(markdown_output)

                markdown_output = await markdown_template.render_async(api = "kpimgmt_query_dashboards",
                                             data_to_template = payload)
                                             
                async with aiofiles.open('Health Information/KPI Mgmt Query/Markdown/Health Information KPI Mgmt Query Dashboards.md', mode='w' ) as f:
                    await f.write(markdown_output)

                markdown_output = await markdown_template.render_async(api = "kpimgmt_query_scripts",
                                             data_to_template = payload)
                                             
                async with aiofiles.open('Health Information/KPI Mgmt Query/Markdown/Health Information KPI Mgmt Query Scripts.md', mode='w' ) as f:
                    await f.write(markdown_output)

                markdown_output = await markdown_template.render_async(api = "kpimgmt_query_sensor_groups",
                                             data_to_template = payload)
                                             
                async with aiofiles.open('Health Information/KPI Mgmt Query/Markdown/Health Information KPI Mgmt Query Sensor Groups.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "/crosswork/nca/v1/yang/modules" in api:
                async with aiofiles.open('YANG Modules/Markdown/YANG Modules.md', mode='w' ) as f:
                    await f.write(markdown_output)

    async def html_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        html_template = env.get_template('crosswork_companion_html.j2')
        for api, payload in json.loads(parsed_json):
            html_output = await html_template.render_async(api = api,
                                             data_to_template = payload)
            if "/crosswork/hi/v1/kpimgmt/query" in api:
                async with aiofiles.open('Health Information/KPI Mgmt Query/HTML/Health Information KPI Mgmt Query.html', mode='w' ) as f:
                    await f.write(html_output)

                html_output = await html_template.render_async(api = "kpimgmt_query_alert_outputs",
                                                 data_to_template = payload)
                async with aiofiles.open('Health Information/KPI Mgmt Query/HTML/Health Information KPI Mgmt Query Alert Output.html', mode='w' ) as f:
                    await f.write(html_output)

                html_output = await html_template.render_async(api = "kpimgmt_query_dashboards",
                                                 data_to_template = payload)
                async with aiofiles.open('Health Information/KPI Mgmt Query/HTML/Health Information KPI Mgmt Query Dashboards.html', mode='w' ) as f:
                    await f.write(html_output)

                html_output = await html_template.render_async(api = "kpimgmt_query_scripts",
                                                 data_to_template = payload)
                async with aiofiles.open('Health Information/KPI Mgmt Query/HTML/Health Information KPI Mgmt Query Scripts.html', mode='w' ) as f:
                    await f.write(html_output)

                html_output = await html_template.render_async(api = "kpimgmt_query_sensor_groups",
                                                 data_to_template = payload)
                async with aiofiles.open('Health Information/KPI Mgmt Query/HTML/Health Information KPI Mgmt Query Sensor Groups.html', mode='w' ) as f:
                    await f.write(html_output)

            if "/crosswork/nca/v1/yang/modules" in api:
                async with aiofiles.open('YANG Modules/HTML/YANG Modules.html', mode='w' ) as f:
                    await f.write(html_output)
          
    async def mindmap_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        mindmap_template = env.get_template('crosswork_companion_mindmap.j2')
        for api, payload in json.loads(parsed_json):
            mindmap_output = await mindmap_template.render_async(api = api,
                                             data_to_template = payload)
            if "/crosswork/hi/v1/kpimgmt/query" in api:
                async with aiofiles.open('Health Information/KPI Mgmt Query/Mindmap/Health Information KPI Mgmt Query.md', mode='w' ) as f:
                    await f.write(mindmap_output)

                mindmap_output = await mindmap_template.render_async(api = "kpimgmt_query_alert_outputs",
                                             data_to_template = payload)
    
                async with aiofiles.open('Health Information/KPI Mgmt Query/Mindmap/Health Information KPI Mgmt Query Alert Output.md', mode='w' ) as f:
                    await f.write(mindmap_output)

                mindmap_output = await mindmap_template.render_async(api = "kpimgmt_query_dashboards",
                                             data_to_template = payload)
    
                async with aiofiles.open('Health Information/KPI Mgmt Query/Mindmap/Health Information KPI Mgmt Query Dashboards.md', mode='w' ) as f:
                    await f.write(mindmap_output)

                mindmap_output = await mindmap_template.render_async(api = "kpimgmt_query_scripts",
                                             data_to_template = payload)
    
                async with aiofiles.open('Health Information/KPI Mgmt Query/Mindmap/Health Information KPI Mgmt Query Scripts.md', mode='w' ) as f:
                    await f.write(mindmap_output)

                mindmap_output = await mindmap_template.render_async(api = "kpimgmt_query_sensor_groups",
                                             data_to_template = payload)
    
                async with aiofiles.open('Health Information/KPI Mgmt Query/Mindmap/Health Information KPI Mgmt Query Sensor Groups.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "/crosswork/nca/v1/yang/modules" in api:
                async with aiofiles.open('YANG Modules/Mindmap/YANG Modules.md', mode='w' ) as f:
                    await f.write(mindmap_output)

    async def all_files(self, parsed_json):
        await asyncio.gather(self.json_file(parsed_json), self.yaml_file(parsed_json), self.csv_file(parsed_json), self.markdown_file(parsed_json), self.html_file(parsed_json), self.mindmap_file(parsed_json))

@click.command()
@click.option('--url',
    prompt="Crosswork URL",
    help="Crosswork URL",
    required=True,envvar="URL")
@click.option('--username',
    prompt="Crosswork Username",
    help="Crosswork Username",
    required=True,envvar="USERNAME")
@click.option('--password',
    prompt="Crosswork Password",
    help="Crosswork Password",
    required=True, hide_input=True,envvar="PASSWORD")
def cli(url,username,password):
    invoke_class = CrossworkCompanion(url,username,password)
    invoke_class.crosswork_companion()

if __name__ == "__main__":
    cli()
