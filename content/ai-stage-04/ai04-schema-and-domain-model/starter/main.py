from pydantic import BaseModel

class TripRequest(BaseModel):
    pass

if __name__=="__main__":
    from fixtures import demo
    demo(TripRequest)
