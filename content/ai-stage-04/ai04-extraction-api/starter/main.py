def create_app(provider,*,timeout=0.5):
    raise NotImplementedError
if __name__=="__main__":
    from fixtures import demo
    demo(create_app)
