
class ConversationMemory:

    def __init__(self, max_messages=10):
        self.max_messages = max_messages
        self.history = []

    def add_message(self, role, content):

        message = {
            "role": role,
            "content": content
        }

        self.history.append(message)

        # Keep only the latest messages
        self.history = self.history[-self.max_messages:]

    def get_history(self):
        return self.history

    def get_context(self):

        context = ""

        for message in self.history:
            context += (
                f"{message['role'].capitalize()}: "
                f"{message['content']}\n"
            )

        return context

    def clear_memory(self):
        self.history = []


if __name__ == "__main__":

    memory = ConversationMemory(max_messages=10)

    # First conversation
    memory.add_message(
        "user",
        "How many patients are registered?"
    )

    memory.add_message(
        "assistant",
        "There are 100 registered patients."
    )

    # Follow-up question
    memory.add_message(
        "user",
        "How many appointments are scheduled?"
    )

    memory.add_message(
        "assistant",
        "There are 25 scheduled appointments."
    )

    print("\n========== CONVERSATION MEMORY ==========")

    print("\nConversation History:")

    for message in memory.get_history():
        print(f"{message['role'].capitalize()}: {message['content']}")

    print("\nConversation Context:")
    print(memory.get_context())

    print("Total messages:", len(memory.get_history()))

    print("\n========== MEMORY TEST COMPLETED ==========")
