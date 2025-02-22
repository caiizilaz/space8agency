from agency_swarm.tools import BaseTool
from pydantic import Field
import json
from typing import Optional, Dict, Any, List

class MUIThemeGenerator(BaseTool):
    """
    A tool for generating Material-UI themes with customized color schemes, typography, and component styles.
    It follows the MUI theming specification from https://mui.com/material-ui/customization/theming/
    """
    
    primary_color: str = Field(
        default="#1976d2",
        description="Primary color in hex format (e.g., #1976d2)"
    )
    
    secondary_color: str = Field(
        default="#9c27b0",
        description="Secondary color in hex format (e.g., #9c27b0)"
    )
    
    mode: str = Field(
        default="light",
        description="Theme mode: 'light' or 'dark'"
    )
    
    font_family: str = Field(
        default="'Roboto', 'Helvetica', 'Arial', sans-serif",
        description="Primary font family for the theme"
    )
    
    border_radius: float = Field(
        default=4,
        description="Default border radius for components in pixels"
    )
    
    spacing_unit: int = Field(
        default=8,
        description="Base spacing unit in pixels"
    )
    
    custom_components: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Custom component style overrides"
    )

    def run(self) -> str:
        """
        Generates a complete MUI theme configuration based on the provided parameters.
        Returns the theme as a JSON string that can be directly used in a React/MUI application.
        """
        theme = {
            "palette": {
                "mode": self.mode,
                "primary": {
                    "main": self.primary_color,
                    "light": self._adjust_color(self.primary_color, 0.2),  # Lighter version
                    "dark": self._adjust_color(self.primary_color, -0.2),  # Darker version
                    "contrastText": "#ffffff"
                },
                "secondary": {
                    "main": self.secondary_color,
                    "light": self._adjust_color(self.secondary_color, 0.2),
                    "dark": self._adjust_color(self.secondary_color, -0.2),
                    "contrastText": "#ffffff"
                },
                "background": {
                    "default": "#ffffff" if self.mode == "light" else "#121212",
                    "paper": "#ffffff" if self.mode == "light" else "#1e1e1e"
                },
                "text": {
                    "primary": "rgba(0, 0, 0, 0.87)" if self.mode == "light" else "rgba(255, 255, 255, 0.87)",
                    "secondary": "rgba(0, 0, 0, 0.6)" if self.mode == "light" else "rgba(255, 255, 255, 0.6)"
                }
            },
            "typography": {
                "fontFamily": self.font_family,
                "fontSize": 14,
                "fontWeightLight": 300,
                "fontWeightRegular": 400,
                "fontWeightMedium": 500,
                "fontWeightBold": 700,
                "h1": {
                    "fontSize": "6rem",
                    "fontWeight": 300,
                    "lineHeight": 1.167
                },
                "h2": {
                    "fontSize": "3.75rem",
                    "fontWeight": 300,
                    "lineHeight": 1.2
                },
                "h3": {
                    "fontSize": "3rem",
                    "fontWeight": 400,
                    "lineHeight": 1.167
                },
                "h4": {
                    "fontSize": "2.125rem",
                    "fontWeight": 400,
                    "lineHeight": 1.235
                },
                "h5": {
                    "fontSize": "1.5rem",
                    "fontWeight": 400,
                    "lineHeight": 1.334
                },
                "h6": {
                    "fontSize": "1.25rem",
                    "fontWeight": 500,
                    "lineHeight": 1.6
                }
            },
            "shape": {
                "borderRadius": self.border_radius
            },
            "spacing": self.spacing_unit,
            "components": self.custom_components if self.custom_components else {
                "MuiButton": {
                    "styleOverrides": {
                        "root": {
                            "textTransform": "none"
                        }
                    }
                },
                "MuiTextField": {
                    "defaultProps": {
                        "variant": "outlined"
                    }
                }
            }
        }
        
        return json.dumps(theme, indent=2)
    
    def _adjust_color(self, hex_color: str, factor: float) -> str:
        """
        Helper method to adjust a hex color by a factor (-1 to 1)
        Returns a new hex color
        """
        # Remove the hash if present
        hex_color = hex_color.lstrip('#')
        
        # Convert to RGB
        r = int(hex_color[:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:], 16)
        
        # Adjust each component
        r = max(0, min(255, int(r * (1 + factor))))
        g = max(0, min(255, int(g * (1 + factor))))
        b = max(0, min(255, int(b * (1 + factor))))
        
        # Convert back to hex
        return f"#{r:02x}{g:02x}{b:02x}"

if __name__ == "__main__":
    # Test the theme generator with custom values
    generator = MUIThemeGenerator(
        primary_color="#2196f3",
        secondary_color="#f50057",
        mode="light",
        font_family="'Poppins', sans-serif",
        border_radius=8,
        spacing_unit=8,
        custom_components={
            "MuiButton": {
                "styleOverrides": {
                    "root": {
                        "borderRadius": 24,
                        "textTransform": "none",
                        "fontWeight": 600
                    }
                }
            }
        }
    )
    
    print(generator.run()) 