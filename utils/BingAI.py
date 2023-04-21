from EdgeGPT import Chatbot, ConversationStyle

async def bing_chat(prompt="", style=ConversationStyle.balanced):
    # Функция получения ответа от BingAI с использованием cookies.
    if prompt == "":
        return "Пустой запрос, повторите"
    gbot = Chatbot(cookie_path=r'C:\Projects\BotObormot\utils\cook.json')
    response_dict = await gbot.ask(prompt=prompt, conversation_style=style)
    return response_dict['item']['messages'][1]['text'].replace("[^\\d^]", "")
