from fixtures import demo

def compare(before,after):
    if before["metrics"].keys()!=after["metrics"].keys() or before["errors"].keys()!=after["errors"].keys():
        raise ValueError("Reports require the same cases and metrics")
    delta={}
    for name,left in before["metrics"].items():
        a,b=left["rate"],after["metrics"][name]["rate"]
        delta[name]=b-a if a is not None and b is not None else None
    new_errors=sorted(key for key,errors in after["errors"].items() if errors and not before["errors"][key])
    return {"delta":delta,"new_errors":new_errors}
if __name__=="__main__":
    demo(compare)
