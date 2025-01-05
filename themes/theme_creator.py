import importlib
import re

class ThemeCreator:
    def __init__(self, theme_colors_module: str, template_path: str, output_path: str):
        """
        Initialize the ThemeCreator.

        :param theme_colors_module: Module name for theme colors (e.g., 'theme_colors')
        :param template_path: Path to the QSS template file
        :param output_path: Path to save the generated QSS file
        """
        self.theme_colors_module = theme_colors_module
        self.template_path = template_path
        self.output_path = output_path

    def load_colors(self):
        """
        Dynamically load the theme_colors module and extract constants.
        
        :return: Dictionary of color constants and their values
        """
        try:
            module = importlib.import_module(self.theme_colors_module)
        except ImportError as e:
            raise ImportError(f"Failed to load theme colors module: {e}")
        
        # Extract constants (all-uppercase variables)
        return {name: value for name, value in vars(module).items() if name.isupper()}

    def create_theme(self):
        """
        Create a QSS theme file by replacing placeholders with theme color values.
        """
        # Load colors
        colors = self.load_colors()

        # Read the template
        try:
            with open(self.template_path, 'r') as template_file:
                qss_template = template_file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Template file not found: {self.template_path}")

        # Replace placeholders with actual color values
        qss = qss_template
        for placeholder, value in colors.items():
            # Use regex to replace exact matches of placeholders (e.g., PRIMARY_BACKGROUND)
            qss = re.sub(rf'\b{placeholder}\b', value, qss)

        # Save the generated QSS file
        with open(self.output_path, 'w') as output_file:
            output_file.write(qss)

        print(f"Theme successfully created and saved to {self.output_path}")
