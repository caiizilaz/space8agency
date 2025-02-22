from agency_swarm.tools import BaseTool
from pydantic import Field
import openai
from dotenv import load_dotenv

load_dotenv()

class ScreenshotAnalyzer(BaseTool):
    """
    A tool for analyzing website screenshots using GPT-4 Vision.
    This tool helps evaluate the visual design and layout of web pages.
    """
    
    image_url: str = Field(
        ..., 
        description="URL of the screenshot image to analyze"
    )
    
    analysis_type: str = Field(
        "general",
        description="Type of analysis to perform: 'general', 'layout', 'design', 'accessibility'"
    )
    
    def run(self):
        """
        Analyzes a website screenshot using GPT-4 Vision and returns detailed feedback.
        """
        try:
            # Prepare the prompt based on analysis type
            prompts = {
                "general": "Analyze this website screenshot and provide general feedback on its design, layout, and user experience.",
                "layout": "Analyze the layout of this website. Focus on spacing, alignment, hierarchy, and overall structure.",
                "design": "Evaluate the visual design elements including colors, typography, imagery, and overall aesthetic.",
                "accessibility": "Assess the accessibility of this design, including contrast, text size, and navigation clarity."
            }
            
            prompt = prompts.get(self.analysis_type, prompts["general"])
            
            response = openai.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": self.image_url}
                        ]
                    }
                ],
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error analyzing screenshot: {str(e)}"

if __name__ == "__main__":
    # Test the tool
    analyzer = ScreenshotAnalyzer(
        image_url="https://example.com/screenshot.png",
        analysis_type="general"
    )
    print(analyzer.run()) 