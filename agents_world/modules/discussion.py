from agents_world.core.game_state import GameState, ChatMessage

class DiscussionSystem:
    """Manages generation of chat replies based on personality and memory."""
    def __init__(self, prompt_builder: 'PromptBuilder'):
        from agents_world.llm.llm_client import LLMClient
        self.llm = LLMClient()
        self.prompt_builder = prompt_builder

    def contribute(self, agent_id: str, memory: 'MemorySystem', personality: 'PersonalityProfile', game_state: GameState) -> ChatMessage:
        """Generates and posts a message to game chat."""
        recent_msgs = game_state.chat_log[-5:]
        chat_hist = "\n".join([f"{msg.author_id}: {msg.content}" for msg in recent_msgs])
        
        mem_sum = memory.get_context_summary(max_tokens=300)
        
        prompt = self.prompt_builder.render("discuss", chat_history=chat_hist, memory_summary=mem_sum)
        prompt = self.prompt_builder.apply_personality(prompt, personality)
        
        try:
            response = self.llm.complete(prompt, max_tokens=100)
        except Exception:
            response = "*silence*"
            
        msg = ChatMessage(author_id=agent_id, content=response, tick=game_state.tick)
        return msg

    def get_transcript(self, game_state: GameState) -> str:
        """Returns string representation of complete chat log."""
        return "\n".join([f"[{msg.tick}] {msg.author_id}: {msg.content}" for msg in game_state.chat_log])
