from themes.theme_creator import ThemeCreator

# Initialize ThemeCreator
creator = ThemeCreator(
    theme_colors_module='themes.standard_theme.standard_theme_colors',
    template_path='D:/OneDrive - Uppsala universitet/General/AI-Studio/themes/theme_template.qss',
    output_path='D:/OneDrive - Uppsala universitet/General/AI-Studio/themes/standard_theme/standard_theme_generated.qss'
)

# Create the theme
creator.create_theme()
