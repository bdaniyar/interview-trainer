from fixtures import EXAMPLES, POLICY, VERSION, Prompt, demo

def build_prompt(text,note=None):
    if not isinstance(text,str) or not text.strip() or len(text)>500:
        raise ValueError("Некорректный запрос")
    if note is not None and (not isinstance(note,str) or len(note)>400):
        raise ValueError("Некорректная заметка")
    return Prompt(VERSION,POLICY,EXAMPLES,text,note if note and note.strip() else None)
if __name__=="__main__":
    demo(build_prompt)
