from langchain.callbacks.base import BaseCallbackHandler
from langchain.chat_models import ChatOpenAI


class MyCustomStreamingCallbackHandler(BaseCallbackHandler):

    def __init__(self, tts):

        self.single_sentence = ''
        self.comma_cunt = 0
        # Azure tts object
        self.tts = tts

    def on_chat_model_start(self, serialized, prompts, **kwargs) -> None:
        """Run when LLM starts running. Clean the queue."""
        if self.single_sentence != '':
            self.single_sentence = ''

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        token = token.replace('\n', '')
        if token == '，':
            self.comma_cunt += 1

        if token == '。' or token == '？' or token == '！' or token == '：' or token == '）。':

            self.single_sentence += (token)
            print('text_to_speech: ', self.single_sentence)
            self.tts.text_to_speech(self.single_sentence)
            self.single_sentence = ''
            self.comma_cunt = 0

        else:
            self.single_sentence += (token)


class LLM():

    def __init__(self):
        pass

    def openAI(
        self,
        openai_api_key,
        callbacks=None,
        streaming=True,
        temperature=0.7,
        max_tokens=350,
    ):

        #Create OpenAI LLM
        return ChatOpenAI(
            model='gpt-4o',
            streaming=streaming,
            callbacks=callbacks,
            temperature=temperature,
            openai_api_key=openai_api_key,
            max_tokens=max_tokens,
            organization = "org-YjmdJOex8ynecZHmgpIrRNRq"
        )
