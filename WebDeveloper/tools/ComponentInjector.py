from agency_swarm.tools import BaseTool
from pydantic import Field
import os

class ComponentInjector(BaseTool):
    """
    A tool for injecting React components into pages.
    This tool helps manage the import and usage of components in page files.
    """
    
    page_path: str = Field(
        ..., 
        description="Path to the page file where the component should be injected"
    )
    
    component_name: str = Field(
        ...,
        description="Name of the component to inject"
    )
    
    component_import: str = Field(
        ...,
        description="Import statement for the component"
    )
    
    component_usage: str = Field(
        ...,
        description="JSX code for using the component"
    )
    
    def run(self):
        """
        Injects a component into a page file by adding the import statement
        and the component usage code.
        """
        try:
            # Read the current content of the page file
            with open(self.page_path, "r") as f:
                content = f.read()
            
            # Add import statement after the last import
            import_index = content.rfind("import")
            if import_index != -1:
                last_import_end = content.find("\n", import_index)
                content = (
                    content[:last_import_end + 1] +
                    self.component_import + "\n" +
                    content[last_import_end + 1:]
                )
            else:
                content = self.component_import + "\n" + content
            
            # Add component usage before the last closing tag
            last_closing = content.rfind("</")
            if last_closing != -1:
                content = (
                    content[:last_closing] +
                    "  " + self.component_usage + "\n" +
                    content[last_closing:]
                )
            
            # Write the modified content back to the file
            with open(self.page_path, "w") as f:
                f.write(content)
            
            return f"Component {self.component_name} injected successfully into {self.page_path}"
            
        except Exception as e:
            return f"Error injecting component: {str(e)}"

if __name__ == "__main__":
    # Test the tool
    injector = ComponentInjector(
        page_path="src/pages/index.tsx",
        component_name="Header",
        component_import="import Header from '../components/Header';",
        component_usage="<Header />"
    )
    print(injector.run()) 