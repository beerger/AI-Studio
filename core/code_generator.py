import os

class CodeGenerator:
    def __init__(self, model_manager, output_dir):
        self.model_manager = model_manager
        self.output_dir = output_dir

    def generate_model_code(self):
        """Generates the model definition file."""
        model_code_path = os.path.join(self.output_dir, "models", "model.py")
        os.makedirs(os.path.dirname(model_code_path), exist_ok=True)

        with open(model_code_path, "w") as model_file:
            model_file.write(self._generate_imports())
            model_file.write(self._generate_class_definition())

        print(f"Model definition generated at {model_code_path}")

    def _generate_imports(self):
        """Generates import statements."""
        imports = [
            "import torch",
            "import torch.nn as nn",
        ]
        return "\n".join(imports) + "\n\n"

    def _generate_class_definition(self):
        """Generates the main class definition."""
        class_def = [
            "class GeneratedModel(nn.Module):",
            self._indent("def __init__(self):", 1),
            self._indent("super(GeneratedModel, self).__init__()", 2),
            self._indent(self._generate_layers(), 2),
            self._indent("def forward(self, x):", 1),
            self._indent("return self.model(x)", 2),
        ]
        return "\n".join(class_def) + "\n"

    def _generate_layers(self):
        """Generates the layers of the model."""
        layers = ["self.model = nn.Sequential("]
        for component in self.model_manager.component_wrappers:
            layers.append(self._indent(f"nn.{component},", 3))
        layers.append(")")
        return "\n".join(layers)

    def _indent(self, text, level=0):
        """Indents the given text by the specified level."""
        return " " * 4 * level + text

    def generate_all(self):
        """Generates all required files and folders."""
        self._generate_folders()
        self.generate_model_code()

    def _generate_folders(self):
        """Creates necessary folders."""
        os.makedirs(os.path.join(self.output_dir, "models"), exist_ok=True)