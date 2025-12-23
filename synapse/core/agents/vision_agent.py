import time
from synapse.core.nodes.ollama_node import OllamaNode
from synapse.core.models import AgentContribution

class VisionAgent:
    def __init__(self, agent_id: str, model: str = "llava"):
        self.agent_id = agent_id
        self.node = OllamaNode(model=model)

    async def analyze(self, image_path: str) -> AgentContribution:
        """
        Analyzes an image using the multimodal model.
        """
        prompt = "Describe this image in detail."
        # In a real scenario, we might need to handle reading the image bytes 
        # if Ollama expects base64, but the python client handles paths too usually.
        # We'll assume paths for now as per Ollama python docs.
        description = await self.node.generate(prompt=prompt, images=[image_path])
        
        return AgentContribution(
            agent_id=self.agent_id,
            timestamp=time.time(),
            content=description,
            metadata={"source": image_path, "model": self.node.model}
        )
