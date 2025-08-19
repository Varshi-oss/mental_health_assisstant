# chat_engine.py

import os
from llama_index.core.chat_engine import CondensePlusContextChatEngine
from llama_index.core.memory import ChatMemoryBuffer
from doc_engine import retriever  # <-- Import the retriever here
from typing import Dict
from llama_index.core.llms import ChatMessage, MessageRole
from doc_engine import llm as global_llm # <-- Import the global llm instance

# Dictionary to store chat engine for each session
session_chat_engines: Dict[str, CondensePlusContextChatEngine] = {}

def get_response(session_id: str, user_query: str) -> str:
    """
    Get a response from the chat engine with memory, using the document retriever.
    """
    if session_id not in session_chat_engines:
        # Create a new chat engine for a new session_id
        chat_memory = ChatMemoryBuffer.from_defaults(token_limit=3000)
        session_chat_engines[session_id] = CondensePlusContextChatEngine.from_defaults(
            retriever=retriever, # <-- Use the retriever here
            llm=global_llm, # <-- Pass the llm instance here
            memory=chat_memory,
            verbose=True
        )

    # Retrieve the chat engine for the current session
    chat_engine = session_chat_engines[session_id]

    # Use the chat engine to get a response
    response = chat_engine.chat(user_query)
    
    return str(response)