import yaml
import os

def generate_grafana_provisioning():
    config_path = 'plc_layout.yml'
    output_path = 'grafana/influxdb.yaml'
    
    if not os.path.exists(config_path):
        print(f"Error: {config_path} not found.")
        return

    with open(config_path, 'r') as f:
        layout = yaml.safe_load(f)

    datasources = []
    
    # Static credentials and settings
    influx_url = f"http://{os.getenv('INFLUXDB_HOST', 'plc_influxdb')}:8086"
    username = os.getenv('INFLUXDB_ADMIN_USER', 'admin')
    password = os.getenv('INFLUXDB_ADMIN_PASSWORD', 'supersecretpassword')

    for plc in layout.get('plc_info', []):
        plc_name = plc.get('plc_name')
        if not plc_name:
            continue
            
        ds = {
            'name': f"InfluxDB-{plc_name}",
            'type': 'influxdb',
            'uid': f"influxdb-{plc_name.lower()}",
            'orgId': 1,
            'url': influx_url,
            'database': plc_name,
            'user': username,
            'secureJsonData': {
                'password': password
            },
            'jsonData': {
                'httpMethod': 'POST'
            },
            'access': 'proxy',
            'isDefault': False,
            'version': 1, # InfluxDB 1.x
            'editable': True
        }
        datasources.append(ds)

    # Set the first one as default if there are any
    if datasources:
        datasources[0]['isDefault'] = True

    provisioning = {
        'apiVersion': 1,
        'datasources': datasources
    }

    # Custom dumper to ensure proper indentation of list items (matching influxdb.yaml style)
    class IndentDumper(yaml.SafeDumper):
        def increase_indent(self, flow=False, indentless=False):
            return super(IndentDumper, self).increase_indent(flow, False)

    with open(output_path, 'w') as f:
        f.write("# Automatically generated from plc_layout.yml\n")
        yaml.dump(provisioning, f, Dumper=IndentDumper, default_flow_style=False, sort_keys=False, indent=2)
    
    print(f"Successfully generated {output_path} with {len(datasources)} datasources.")

if __name__ == "__main__":
    generate_grafana_provisioning()
