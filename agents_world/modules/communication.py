from agents_world.core.game_state import GameState, ChatMessage

class CommunicationSystem:
    """Manages chat messages queue and distribution."""
    def __init__(self):
        self.message_queue = []
        
    def broadcast(self, message: ChatMessage, game_state: GameState) -> None:
        """Adds a message to queue and state log."""
        self.message_queue.append(message)
        game_state.log_chat(message.author_id, message.content)
        
    def flush(self) -> None:
        """Clears the message queue."""
        self.message_queue.clear()
