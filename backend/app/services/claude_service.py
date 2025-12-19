import os
import json
import re
import httpx
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()


def get_http_client():
    """Create an httpx client with optional proxy support."""
    proxy_url = os.getenv("PROXY_URL")
    
    if proxy_url:
        # Convert socks:// to socks5:// if needed (httpx requires socks5://)
        if proxy_url.startswith("socks://"):
            proxy_url = proxy_url.replace("socks://", "socks5://", 1)
        
        return httpx.Client(
            proxy=proxy_url,
            timeout=httpx.Timeout(120.0, connect=30.0)
        )
    
    return httpx.Client(timeout=httpx.Timeout(120.0, connect=30.0))


class ClaudeService:
    """Service for interacting with Claude API to generate learning roadmaps."""

    def __init__(self):
        api_key = os.getenv("CLAUDE_API_KEY")
        if not api_key:
            raise ValueError("CLAUDE_API_KEY environment variable is not set")
        
        # Create client with optional proxy support
        http_client = get_http_client()
        self.client = Anthropic(api_key=api_key, http_client=http_client)
        self.model = "claude-sonnet-4-20250514"

    def generate_roadmap(self, query: str) -> dict:
        """
        Generate a learning roadmap based on the user's query.
        
        Args:
            query: The user's learning goal (e.g., "I want to learn Go language")
            
        Returns:
            Dictionary containing title, content (markdown), and visual_data (JSON)
        """
        system_prompt = """You are an expert learning mentor and curriculum designer. Your task is to create comprehensive, actionable learning roadmaps for users who want to learn new skills.

When creating a roadmap, you must:
1. Break down the learning journey into clear phases
2. Provide specific, actionable steps within each phase
3. Suggest high-quality resources (books, courses, tutorials, projects)
4. Include estimated timeframes for each phase
5. Add practical projects and milestones to track progress

You MUST respond with a JSON object in the following exact format (no additional text before or after):
{
    "title": "A concise title for this learning roadmap",
    "content": "Full markdown content with detailed roadmap including phases, resources, and tips",
    "visual_data": {
        "phases": [
            {
                "id": 1,
                "title": "Phase name",
                "description": "Brief description",
                "duration": "e.g., 2-3 weeks",
                "milestones": ["milestone 1", "milestone 2"]
            }
        ],
        "total_duration": "e.g., 3-6 months"
    }
}

The markdown content should be well-structured with:
- Clear headers (##, ###)
- Bullet points for lists
- Code examples where relevant
- Links to resources (use placeholder URLs if needed)
- Tips and best practices
- Common pitfalls to avoid"""

        user_message = f"""Create a comprehensive learning roadmap for the following goal:

"{query}"

Remember to respond ONLY with the JSON object, no additional text."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )

        # Extract the text content from the response
        response_text = response.content[0].text.strip()
        
        # Try to parse the JSON response
        try:
            # Handle case where response might have markdown code blocks
            if response_text.startswith("```"):
                # Extract JSON from code block
                json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', response_text)
                if json_match:
                    response_text = json_match.group(1)
            
            roadmap_data = json.loads(response_text)
            return roadmap_data
        except json.JSONDecodeError:
            # If parsing fails, create a structured response from the raw text
            return {
                "title": f"Learning Roadmap: {query[:50]}",
                "content": response_text,
                "visual_data": {
                    "phases": [
                        {
                            "id": 1,
                            "title": "Getting Started",
                            "description": "Begin your learning journey",
                            "duration": "1-2 weeks",
                            "milestones": ["Complete initial setup", "Understand basics"]
                        }
                    ],
                    "total_duration": "Varies based on dedication"
                }
            }


# Singleton instance
claude_service = ClaudeService() if os.getenv("CLAUDE_API_KEY") else None


def get_claude_service() -> ClaudeService:
    """Get or create Claude service instance."""
    global claude_service
    if claude_service is None:
        claude_service = ClaudeService()
    return claude_service
