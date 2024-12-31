import pickle
import os

class ModelManager():
    
    _instance = None # Singleton instance
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, "initialized"):  # Prevent reinitialization
            self.component_wrappers = []
            self.initialized = True
            self.undo_stack = []
            self.redo_stack = []
    
    def __len__(self):
        return len(self.component_wrappers)
    
    def __iter__(self):
        for component in self.component_wrappers:
            yield component
    
    def undo(self):
        if self.undo_stack:
            self.redo_stack.append(self.component_wrappers.copy())
            self.component_wrappers = self.undo_stack.pop()
    
    def redo(self):
        if self.redo_stack:
            self.undo_stack.append(self.component_wrappers.copy())
            self.component_wrappers = self.redo_stack.pop()
    
    def reset(self):
        # treat reset as a brand new action
        self.undo_stack.append(self.component_wrappers.copy())
        self.component_wrappers = []
        self.redo_stack.clear()
    
    def add_component(self, component):
        self.undo_stack.append(self.component_wrappers.copy())
        self.component_wrappers.append(component)
        self.redo_stack.clear()
        
    def remove_component(self, component):
        self.undo_stack.append(self.component_wrappers.copy())
        self.component_wrappers.remove(component)
        self.redo_stack.clear()
        
    def remove_component_at(self, index):
        self.undo_stack.append(self.component_wrappers.copy())
        del self.component_wrappers[index]
        self.redo_stack.clear()
        
    def remove_last_component(self):
        if len(self.component_wrappers) > 0:
            self.undo_stack.append(self.component_wrappers.copy())
            self.component_wrappers.pop()
            self.redo_stack.clear()
            
    def duplicate_component(self, component):
        self.undo_stack.append(self.component_wrappers.copy())
        self.component_wrappers.append(component)
        self.redo_stack.clear()
    
    def duplicate_component_at(self, index):
        self.undo_stack.append(self.component_wrappers.copy())
        self.component_wrappers.insert(index, self.component_wrappers[index])
        self.redo_stack.clear()
    
    def duplicate_last_component(self):
        if len(self.component_wrappers) > 0:
            self.undo_stack.append(self.component_wrappers.copy())
            self.component_wrappers.append(self.component_wrappers[-1])
            self.redo_stack.clear()
            
    def save(self, filepath):
        """
        Saves the ModelManager to a pickle file.
        """
        try:
            with open(filepath, 'wb') as file:
                pickle.dump(self, file)
            print(f"ModelManager saved to {filepath}")
        except IOError as e:
            print(f"Failed to save ModelManager to {filepath}: {e}")

    @staticmethod
    def load(filepath):
        """
        Loads a ModelManager from a pickle file.
        """
        with open(filepath, 'rb') as file:
            model_manager = pickle.load(file)
            #  undo and redo stacks
            model_manager.undo_stack = []
            model_manager.redo_stack = []
            return model_manager
    
    @staticmethod
    def load_from_session_state(session_state):
        """
        Loads a ModelManager from the last saved path in the session state.
        If the file path is invalid or loading fails, it returns a new ModelManager instance.
        """
        last_save_path = session_state.load().get("last_save_path")
        if last_save_path and os.path.exists(last_save_path):
            try:
                return ModelManager.load(last_save_path)
            except (pickle.PickleError, IOError, Exception) as e:
                print(f"Failed to load ModelManager from {last_save_path}: {e}")
        return ModelManager()

    def forward(self, x):
        # apply forward pass to all components
        for component in self.component_wrappers:
            x = component.forward(x)

    def __str__(self):
        representation = []
        for component in self.component_wrappers:
            representation.append(str(component))
        return "\n".join(representation)