import threading, os, time

from api_keys_n_variables import azure_speech_key, azure_service_region, openai_api_key, collection_name, QDRANT_URL, QDRANT_API_KEY

from scripts.client_chatbot_setup.python_client import BotSetup
from scripts.client_chatbot_setup.setup_chatbot_gender import BotGenderSetup
from scripts.speech2text.speech2text_whisper import speech2text
from scripts.client_chatbot_setup.display_w_unreal_n_audio2face import A2F, push_emotion, push_audio_file, set_to_default_emotion, close_audio2face_n_unreal, show_record_message, wait_a_min, open_unreal_exe
from scripts.text2speech.azure_tts import azure_TTS
from scripts.text2text.llm import LLM, MyCustomStreamingCallbackHandler
from scripts.vectorDB.qdrant import qdrant
from scripts.text2text.Agent import Agent

from langchain.agents import load_tools, Tool
from langchain.chains import RetrievalQA

from datetime import datetime


def main():

    bot_gender_setup_instance = BotGenderSetup()
    bot_setup_instance = BotSetup()

    # Start Audio2Face server
    _ = A2F()

    # Set the Metahuman Face into idle.
    set_to_default_emotion()

    #啟動UDP Server, 讓python與Unreal相互溝通
    udp_thread = threading.Thread(target=bot_setup_instance.setup_udp_server)
    udp_thread.start()

    # 防止一些啟動時間的dealy
    time.sleep(1)
    # 啟動Unreal
    open_unreal_exe()
    # 防止一些啟動時間的dealy
    time.sleep(1)

    # Wait for user choose the gender of the avatar
    while True:
        # Get the gender that user given
        gender = bot_setup_instance.get_gender()
        if gender in {'m', 'f'}:
            print("gender chosen")
            break

    #給予角色定義的表情參數
    if bot_gender_setup_instance.setup_bot_gender(gender):
        push_emotion(bot_gender_setup_instance.get_default_speaking_emotion())

    #Create Azure text-to-speech
    tts = azure_TTS(bot_gender_setup_instance.get_voice_name(),
                    azure_speech_key, azure_service_region)

    #Create OpenAI LLM
    llmCreator = LLM()
    llm = llmCreator.openAI(
        openai_api_key=openai_api_key,
        callbacks=[MyCustomStreamingCallbackHandler(tts)],
    )

    #Create Qdrant vector DB
    qdrantDB = qdrant(collection_name=collection_name,
                      qdrant_url=QDRANT_URL,
                      qdrant_api_key=QDRANT_API_KEY)
    qdrantDB.setVectorStore(openai_api_key=openai_api_key)

    # The order of following agent code should not be chenge.
    agentCreator = Agent()

    # ConversationSummaryBufferMemory is used for the chat history.
    agentCreator.setConversationBufferMemory(
        llm=LLM().openAI(openai_api_key=openai_api_key),
        memory_key="chat_history")

    # LLM system_message setting
    agentCreator.setSystemMessage(
        systemMessage="你是一個由工研院開發的AI陪伴者，名字叫做服科阿誠，你可以跟我聊任何話題")

    # LangChain pre-define tool: google serper
    serperTools = load_tools(["google-serper"], llm=llm)[0]
    agentCreator.add_tool(serperTools)

    # Add RAG tool for long-term memory
    state_of_union = RetrievalQA.from_chain_type(
        llm=LLM().openAI(openai_api_key=openai_api_key),
        chain_type="stuff",
        retriever=qdrantDB.vector_store.as_retriever(),
    )

    ragTool = Tool(name="Chat_history",
                   func=state_of_union,
                   description="回答 需要回憶以前聊天的內容 的問題時使用。")
    agentCreator.add_tool(ragTool)

    # Create LangChain agent
    agent = agentCreator.agent(llm=llm)

    # Chat loop
    while True:
        try:
            # No need to change
            input_file_dir = "./scripts/record_user_audio/saved_temp_audio_file/recorded_audio.wav"

            #if the recorded file from previous session still exist, remove it
            try:
                os.remove(input_file_dir)
            except:
                pass

            end = bot_setup_instance.get_end()

            #File doesn't exist and end is False, continue detecting
            while not end and not os.path.exists(input_file_dir):
                end = bot_setup_instance.get_end()
            if end:
                close_audio2face_n_unreal()
                udp_thread.join()
                exit()  # Terminate the script here

            # Unreal 出現字段"請稍等"
            wait_a_min()

            # Use OpenAI Whisper do speech-to-text
            messages = speech2text(input_file_dir)
            print(f'messages: {messages}')

            # Get now time
            nowtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S %p %A")

            # Combine input text and nowtime, for better generate result.
            combined_addtime = f"{messages}（{nowtime}）"

            # Run agent
            agent.run(combined_addtime)

            # Generate text from agent
            human_text = str(
                agentCreator.memory.load_memory_variables(
                    {})['chat_history'][-2].content)

            #Add "HumanMessage" for better retrieval quality
            combined_text = f"HumanMessage：{human_text}"

            #Split input text into several texts, a.k.a. chunks.
            texts = qdrantDB.getChunks(combined_text)

            # 將檔案內容上傳至 qdrant 雲端
            print(f'上傳: {texts}')
            qdrantDB.vector_store.add_texts(texts)

        except Exception as e:
            # 當發生異常時執行這裡的代碼
            print(f"Error: {e}")
            push_audio_file(
                bot_gender_setup_instance.get_try_again_voice_file())

        # 告訴Unreal回到等待表情
        set_to_default_emotion()

        #Unreal端show出錄音按鈕
        show_record_message()


if __name__ == "__main__":
    main()