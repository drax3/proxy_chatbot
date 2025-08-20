from typing import List, Dict

def _fallback_stub(history):
    user_last = ""
    for h in reversed(history):
        if h.get("role") == "user":
            user_last = h.get("content", "")
            break

    return f"(mock) YOu said: {user_last[:400]}"

def generate_gemini_reply(api_key, model_name, history):
    if not api_key:
        return _fallback_stub(history)
    try:
        import google.generativeai as genai

        genai.configure(api_key=api_key)

        lines = []
        system_prefix = "You are a concise, helpful assistant"
        lines.append(f"System: {system_prefix}")
        for m in history:
            role = m.get("role", "user")
            content = m.get("content", "")
            if role == "user":
                lines.append(f"User: {content}")
            elif role == "ai":
                lines.append(f"Assistant: {content}")
            elif role == "system":
                lines.append(f"System: {content}")

        prompt = "\n".join(lines)
        model = genai.GenerativeModel(model_name or "gemini-1.5-flash")
        response = model.generate_content(prompt)
        text = getattr(response, "text", None) or ""

        text = text.strip()
        if not text:
            return "(model returned empty content)"
        return text

    except Exception as e:
        return f"(fallback due to error: {type(e).__name__}) "+ _fallback_stub(history)