from contracts import Conversation, Message, Principal


def cost(message):
    return 1 + len(message.text.split()) + len(message.call_ids)


def demo(build_context):
    actor = Principal("training", "lee")
    exchange = (Message("assistant", call_ids=("one", "two")),
                Message("tool", "результат два", call_id="two"),
                Message("tool", "результат один", call_id="one"))
    history = {"c1": Conversation(actor, ((Message("user", "старый вопрос"),), exchange))}
    print(build_context(history, "c1", actor, "бережная политика", "текущий вопрос",
                        capacity=18, reserve=3, count=cost))
