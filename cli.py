import argparse
from .service import handle_request
from .costing import cost_record

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--interactive",action="store_true")
    p.add_argument("--text")
    a=p.parse_args()
    if a.interactive:
        print("LLM Application Engineering Demo - type exit to stop")
        while True:
            x=input("> ")
            if x.strip().lower()=="exit": break
            out,u=handle_request(x)
            print(out.model_dump_json(indent=2))
            print(cost_record(u))
    elif a.text:
        out,u=handle_request(a.text); print(out.model_dump_json(indent=2)); print(cost_record(u))
if __name__=="__main__": main()
