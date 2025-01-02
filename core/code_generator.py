import os
from core.model_manager import ModelManager

class CodeGenerator:
    def __init__(self, output_dir, model_name):
        self.model_manager = ModelManager()
        self.output_dir = output_dir
        self.model_name = model_name
        
    def generate_config_file(self):
        """Generates the configuration file."""
        config_file_path = os.path.join(self.output_dir, "config", "config.yaml")
        os.makedirs(os.path.dirname(config_file_path), exist_ok=True)

        with open(config_file_path, "w") as config_file:
            config_file.write(self._generate_config_content())

        print(f"Configuration file generated at {config_file_path}")

    # TODO: Implement the _generate_config_content method correctly
    def _generate_config_content(self):
        """Generates the content of the configuration file."""
        config_content = [
            "model:",
            self._indent(f"name: {self.model_name}", 1),
            self._indent("input_shape: [1, 3, 224, 224]", 1),
            self._indent("output_shape: [1, 1000]", 1),
            "training:",
            self._indent("batch_size: 32", 1),
            self._indent("num_epochs: 100", 1),
            self._indent("learning_rate: 0.001", 1),
            "data:",
            self._indent("path: /path/to/dataset", 1),
        ]
        return "\n".join(config_content) + "\n"
    
    def generate_training_script(self):
        """Generates the training script file."""
        training_script_path = os.path.join(self.output_dir, "scripts", "train.py")
        os.makedirs(os.path.dirname(training_script_path), exist_ok=True)

        with open(training_script_path, "w") as training_script:
            training_script.write(self._generate_training_script_content())

        print(f"Training script generated at {training_script_path}")
        
    # TODO: Implement the _generate_training_script_content method correctly
    def _generate_training_script_content(self):
        """Generates the content of the training script."""
        training_script_content = [
            "import torch",
            "import torch.nn as nn",
            "from torch.utils.data import DataLoader",
            "from dataset import CustomDataset",
            f"from models.model import {self.model_name}",
            "from utils import train, evaluate",
            "from config import Config",
            "",
            "def main():",
            self._indent("config = Config('config/config.yaml')", 1),
            self._indent("device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')", 1),
            self._indent(f"model = {self.model_name}()", 1),
            self._indent("model.to(device)", 1),
            self._indent("train_dataset = CustomDataset(config.data.path, train=True)", 1),
            self._indent("train_loader = DataLoader(train_dataset, batch_size=config.training.batch_size, shuffle=True)", 1),
            self._indent("optimizer = torch.optim.Adam(model.parameters(), lr=config.training.learning_rate)", 1),
            self._indent("criterion = nn.CrossEntropyLoss()", 1),
            self._indent("for epoch in range(config.training.num_epochs):", 1),
            self._indent("train(model, train_loader, optimizer, criterion, device)", 2),
            self._indent("evaluate(model, train_loader, criterion, device)", 2),
            "",
            "if __name__ == '__main__':",
            self._indent("main()", 1),
        ]
        return "\n".join(training_script_content) + "\n"
        
    
    def generate_model_code(self, tmp_path=None):
        """Generates the model definition file."""
        if not tmp_path:
            model_code_path = os.path.join(self.output_dir, "models", "model.py")
            os.makedirs(os.path.dirname(model_code_path), exist_ok=True)
        else:
            model_code_path = tmp_path

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
            f"class {self.model_name}(nn.Module):",
            self._indent("def __init__(self):", 1),
            self._indent(f"super({self.model_name}, self).__init__()", 2),
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
        layers.append(self._indent(")", 2))
        layers.append("")
        return "\n".join(layers)

    def _indent(self, text, level=0):
        """Indents the given text by the specified level."""
        return " " * 4 * level + text

    def generate_all(self):
        """Generates all required files and folders."""
        #self._generate_folders()
        self.generate_model_code()
        self.generate_config_file()
        self.generate_training_script()

    #def _generate_folders(self):
    #    """Creates necessary folders."""
    #    os.makedirs(os.path.join(self.output_dir, "models"), exist_ok=True)