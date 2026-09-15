import argparse, json
p=argparse.ArgumentParser()
p.add_argument("--infra-hourly-usd",type=float,required=True)
p.add_argument("--measured-rps",type=float,required=True)
p.add_argument("--api-cost-per-request-usd",type=float,required=True)
a=p.parse_args()
req_per_hour=a.measured_rps*3600
self_host_cost=a.infra_hourly_usd/req_per_hour
break_even_requests=a.infra_hourly_usd/a.api_cost_per_request_usd
print(json.dumps({"measured_requests_per_hour":req_per_hour,"self_host_cost_per_request_usd":self_host_cost,"break_even_requests_per_hour":break_even_requests},indent=2))
