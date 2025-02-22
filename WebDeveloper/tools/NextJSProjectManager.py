from agency_swarm.tools import BaseTool
from pydantic import Field
import os
import subprocess
import json

class NextJSProjectManager(BaseTool):
    """
    A tool for managing Next.js project setup and commands.
    This tool helps with project initialization, dependency management, and running development commands.
    """
    
    action: str = Field(
        ..., 
        description="Action to perform: 'create', 'install', 'dev', 'build', 'start'"
    )
    
    project_name: str = Field(
        None,
        description="Name of the project (required for 'create' action)"
    )
    
    dependencies: list = Field(
        None,
        description="List of dependencies to install (for 'install' action)"
    )
    
    def run(self):
        """
        Manages Next.js project operations including creation, dependency installation,
        and running development commands.
        """
        try:
            if self.action == "create":
                if not self.project_name:
                    return "Error: project_name is required for create action"
                
                # Create Next.js project with TypeScript and App Router
                cmd = f"npx create-next-app@latest {self.project_name} --typescript --no-tailwind --no-app --src-dir --import-alias '@/*' --no-eslint --no-turbopack"
                subprocess.run(cmd, shell=True, check=True)
                
                # Add MUI dependencies
                os.chdir(self.project_name)
                mui_deps = [
                    "@mui/material",
                    "@emotion/react",
                    "@emotion/styled",
                    "@mui/icons-material"
                ]
                subprocess.run("npm install " + " ".join(mui_deps), shell=True, check=True)
                
                # Update package.json with custom scripts
                with open("package.json", "r") as f:
                    package = json.load(f)
                
                package["scripts"]["analyze"] = "ANALYZE=true next build"
                package["scripts"]["lint:fix"] = "next lint --fix"
                
                with open("package.json", "w") as f:
                    json.dump(package, f, indent=2)
                
                return f"Next.js project '{self.project_name}' created successfully with TypeScript and MUI"
            
            elif self.action == "install":
                if not self.dependencies:
                    return "Error: dependencies list is required for install action"
                
                cmd = "npm install " + " ".join(self.dependencies)
                subprocess.run(cmd, shell=True, check=True)
                return f"Dependencies installed successfully: {', '.join(self.dependencies)}"
            
            elif self.action in ["dev", "build", "start"]:
                cmd = f"npm run {self.action}"
                # Run in background for dev server
                if self.action == "dev":
                    subprocess.Popen(cmd, shell=True)
                    return "Development server started"
                else:
                    subprocess.run(cmd, shell=True, check=True)
                    return f"{self.action} command completed successfully"
            
            else:
                return f"Error: Unknown action '{self.action}'"
            
        except subprocess.CalledProcessError as e:
            return f"Command failed with error: {str(e)}"
        except Exception as e:
            return f"Error: {str(e)}"

if __name__ == "__main__":
    # Test the tool - Create new project
    manager = NextJSProjectManager(
        action="create",
        project_name="my-nextjs-app"
    )
    print(manager.run())
    
    # Test installing additional dependencies
    manager = NextJSProjectManager(
        action="install",
        dependencies=["@mui/x-data-grid", "@mui/x-date-pickers"]
    )
    print(manager.run())
    
    # Test starting dev server
    manager = NextJSProjectManager(
        action="dev"
    )
    print(manager.run()) 