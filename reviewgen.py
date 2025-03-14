def chat_with_ai(user_query):
    url = "https://www.ninjachat.ai/api/chat"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "messages": [
            {"role": "user", "content": user_query}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)

        # Check if response is empty
        if not response.text.strip():
            return "Error: Received an empty response from AI API."

        # Format response for Telegram users
        formatted_response = ""
        lines = response.text.split("\n")
        in_code_block = False

        for line in lines:
            if line.strip().startswith("```"):
                if in_code_block:
                    formatted_response += f"{line.strip()}\n"
                    in_code_block = False
                else:
                    formatted_response += f"{line.strip()}\n"
                    in_code_block = True
            elif in_code_block or line.strip().startswith("<") or line.strip().startswith("&lt;") or line.strip().startswith("&gt;") or line.strip().startswith("**"):
                formatted_response += f"`{line.strip()}`\n"
            else:
                formatted_response += f"{line.strip()}\n"

        return formatted_response

    except requests.exceptions.RequestException as e:
        return f"Request Error: {e}"

