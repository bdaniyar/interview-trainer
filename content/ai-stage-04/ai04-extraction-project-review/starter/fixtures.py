BASELINE={"metrics":{"schema":{"rate":1},"unknown":{"rate":1}},"errors":{"A":[],"B":["city"]}}
CANDIDATE={"metrics":{"schema":{"rate":1},"unknown":{"rate":0.5}},"errors":{"A":["guests"],"B":["city"]}}
def demo(compare):
    report=compare(BASELINE,CANDIDATE)
    assert report=={"delta":{"schema":0,"unknown":-0.5},"new_errors":["A"]}
    print(report)
