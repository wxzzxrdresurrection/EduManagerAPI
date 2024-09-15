from openai.types.chat.chat_completion_system_message_param import ChatCompletionSystemMessageParam
from openai.types.chat.chat_completion_user_message_param import ChatCompletionUserMessageParam


def system_message(content: str):
    return ChatCompletionSystemMessageParam(
        content=content,
        role="system"
    )

def user_message(content: str):
    return ChatCompletionUserMessageParam(
        content=content,
        role="user"
    )
