# Summarization logic using DeepSeek Chat (OpenRouter)
import sys
sys.path.append('./chat_engine')
from chat_engine.openai_chat_connection import llm


def summarize_content(title, body, ministry):
    prompt = f"""
You are an assistant for UPSC students. Read the following PIB press release and write a very short, clear summary in 3-5 bullet points, using easy English. Each bullet should be concise and focus on the most important facts. The summary should be so short that a student can grasp all points in under 60 seconds. Avoid extra explanation, just the key facts.\n\nTitle: {title}\nMinistry: {ministry}\nContent:\n{body}\n\nSummary (3-5 bullet points, each as short as possible):"""
    response = llm.invoke(prompt)
    return response.content.strip()

def summarize_article(title, body, ministry):
    """
    Returns summary using DeepSeek Chat API (title is not optimized).
    """
    summary = summarize_content(title, body, ministry)
    return title, summary
