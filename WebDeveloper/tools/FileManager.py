from agency_swarm.tools import BaseTool
from pydantic import Field
import os

class FileManager(BaseTool):
    """
    A tool for managing file operations including writing new files and modifying existing ones.
    This tool combines file writing and line modification capabilities.
    """
    
    file_path: str = Field(
        ..., 
        description="Path to the file to create or modify"
    )
    
    content: str = Field(
        None,
        description="Content to write to the file (for new files or complete overwrites)"
    )
    
    line_changes: dict = Field(
        None,
        description="Dictionary of line numbers and their new content for specific line modifications"
    )
    
    def run(self):
        """
        Creates a new file or modifies an existing one based on the provided parameters.
        Can either write complete content or modify specific lines.
        """
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            
            # If content is provided, write/overwrite the entire file
            if self.content is not None:
                with open(self.file_path, "w") as f:
                    f.write(self.content)
                return f"File written successfully: {self.file_path}"
            
            # If line changes are provided, modify specific lines
            elif self.line_changes is not None:
                # Read existing content
                with open(self.file_path, "r") as f:
                    lines = f.readlines()
                
                # Apply changes
                for line_num, new_content in self.line_changes.items():
                    if 0 <= line_num < len(lines):
                        lines[line_num] = new_content + "\n"
                
                # Write back to file
                with open(self.file_path, "w") as f:
                    f.writelines(lines)
                
                return f"File modified successfully: {self.file_path}"
            
            else:
                return "Error: Either content or line_changes must be provided"
            
        except Exception as e:
            return f"Error managing file: {str(e)}"

if __name__ == "__main__":
    # Test the tool - Writing a new file
    manager = FileManager(
        file_path="src/styles/globals.css",
        content="""
:root {
    --primary-color: #1976d2;
    --secondary-color: #dc004e;
}

body {
    margin: 0;
    padding: 0;
    font-family: 'Roboto', sans-serif;
}
"""
    )
    print(manager.run())
    
    # Test the tool - Modifying specific lines
    manager = FileManager(
        file_path="src/styles/globals.css",
        line_changes={
            2: "    --primary-color: #2196f3;",
            3: "    --secondary-color: #f50057;"
        }
    )
    print(manager.run()) 