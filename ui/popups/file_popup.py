from PyQt5 import QtWidgets

def get_output_popup() -> str:
    """
    Opens a file dialog to select an output directory.
    
    Return: 
        The selected directory or an empty string if canceled.
    """
    answer = QtWidgets.QFileDialog.getExistingDirectory(None, "Select Output Directory", "")
    if answer == QtWidgets.QFileDialog.Rejected:
        return ""
    return answer