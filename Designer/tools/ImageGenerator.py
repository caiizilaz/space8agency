from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from dotenv import load_dotenv
import openai

load_dotenv()

class ImageGenerator(BaseTool):
    """
    A tool for generating images using DALL-E 3.
    This tool helps create visual assets for websites such as icons, logos, and filler images.
    """
    
    prompt: str = Field(
        ..., 
        description="Detailed description of the image to be generated"
    )
    
    size: str = Field(
        "1024x1024",
        description="Size of the image to generate. Options: 1024x1024, 1024x1792, 1792x1024"
    )
    
    quality: str = Field(
        "standard",
        description="Quality of the image. Options: standard, hd"
    )
    
    def run(self):
        """
        Generate an image using DALL-E 3 based on the provided prompt.
        Returns the URL of the generated image.
        """
        try:
            response = openai.images.generate(
                model="dall-e-3",
                prompt=self.prompt,
                size=self.size,
                quality=self.quality,
                n=1
            )
            
            return response.data[0].url
            
        except Exception as e:
            return f"Error generating image: {str(e)}"

if __name__ == "__main__":
    # Test the tool
    generator = ImageGenerator(
        prompt="A modern, minimalist logo for a tech company, using blue and white colors",
        size="1024x1024",
        quality="standard"
    )
    print(generator.run()) 