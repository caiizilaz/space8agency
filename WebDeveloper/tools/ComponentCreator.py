from agency_swarm.tools import BaseTool
from pydantic import Field
import os

class ComponentCreator(BaseTool):
    """
    A tool for creating React components in TypeScript with Material-UI.
    This tool helps create component files with proper structure and imports.
    """
    
    component_name: str = Field(
        ..., 
        description="Name of the component to create (in PascalCase)"
    )
    
    component_code: str = Field(
        ...,
        description="The complete TypeScript React component code including imports"
    )
    
    def run(self):
        """
        Creates a new component file in the src/components directory.
        Returns the path to the created component file.
        """
        try:
            # Ensure the components directory exists
            components_dir = "src/components"
            os.makedirs(components_dir, exist_ok=True)
            
            # Create the component file path
            file_path = f"{components_dir}/{self.component_name}.tsx"
            
            # Write the component code to the file
            with open(file_path, "w") as f:
                f.write(self.component_code)
            
            return f"Component created successfully at {file_path}"
            
        except Exception as e:
            return f"Error creating component: {str(e)}"

if __name__ == "__main__":
    # Test the tool
    creator = ComponentCreator(
        component_name="Header",
        component_code="""
import React from 'react';
import { AppBar, Toolbar, Typography } from '@mui/material';

const Header: React.FC = () => {
    return (
        <AppBar position="static">
            <Toolbar>
                <Typography variant="h6">
                    My Website
                </Typography>
            </Toolbar>
        </AppBar>
    );
};

export default Header;
"""
    )
    print(creator.run()) 