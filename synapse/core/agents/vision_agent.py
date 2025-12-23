import time
from synapse.core.nodes.ollama_node import OllamaNode
from synapse.core.models import AgentContribution

class VisionAgent:
    def __init__(self, agent_id: str, model: str = "llava"):
        self.agent_id = agent_id
        self.node = OllamaNode(model=model)

    async def analyze(self, image_path: str) -> AgentContribution:
        """
        Analyzes an image or text input using the multimodal model.
        """
        prompt = "Describe this input in detail."
        
        # Basic validation: check if it looks like a path or base64
        # For tests, "test command" is not a path.
        is_path = image_path.startswith(('/', './', 'file://'))
        is_base64 = len(image_path) > 100 and ',' in image_path[:20] # Very naive check
        
        images = [image_path] if (is_path or is_base64) else []
        
        if not images:
            prompt = f"Analyze the following request: {image_path}"
        
        description = await self.node.generate(prompt=prompt, images=images)
        
        return AgentContribution(
            agent_id=self.agent_id,
            timestamp=time.time(),
            content=description,
            metadata={"source": image_path, "model": self.node.model, "type": "IMAGE" if images else "TEXT"}
        )
