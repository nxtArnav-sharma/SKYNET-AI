class ConversationMemory:
    def __init__(self):
        self.messages = []
        self.system_prompt = ""

    def set_system_prompt(self, prompt: str):
        self.system_prompt = prompt
        # Initialize or reset the conversation with the system prompt
        if not self.messages or self.messages[0]["role"] != "system":
            self.messages.insert(0, {"role": "system", "content": prompt})
        else:
            self.messages[0]["content"] = prompt

    def add_user_message(self, content: str):
        self.messages.append({"role": "user", "content": content})

    def add_assistant_message(self, content: str):
        self.messages.append({"role": "assistant", "content": content})

    def add_tool_message(self, tool_id: str, name: str, content: str):
        self.messages.append({
            "role": "tool",
            "tool_call_id": tool_id,
            "name": name,
            "content": content
        })

    def get_messages(self):
        return self.messages

    def clear(self):
        self.messages = []
        if self.system_prompt:
            self.set_system_prompt(self.system_prompt)

conversation_memory = ConversationMemory()
