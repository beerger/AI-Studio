"""
Here are the tooltips for the GUI.
"""


BATCH_SIZE_TOOLTIP = (
    "Specifies the batch size for the input tensor.\n"
    "The batch size determines how many samples are processed together during model export.\n\n"
    "Example:\n- 1 for single sample.\n- 32 for processing 32 samples simultaneously."
)

CHANNELS_TOOLTIP = (
    "Specifies the number of channels in the input tensor.\n"
    "For image-based models:\n- Use 1 for grayscale images.\n- Use 3 for RGB images.\n\n"
    "For non-image data, this value represents the depth or feature size."
)

HEIGHT_TOOLTIP = (
    "Specifies the height of the input tensor.\n"
    "For image-based models, this corresponds to the vertical dimension of the input image.\n\n"
    "Example:\n- 224 for standard ResNet models.\n- 28 for MNIST digit images."
)

WIDTH_TOOLTIP = (
    "Specifies the width of the input tensor.\n"
    "For image-based models, this corresponds to the horizontal dimension of the input image.\n\n"
    "Example:\n- 224 for standard ResNet models.\n- 28 for MNIST digit images."
)

DYNAMIC_SHAPES_TOOLTIP = (
    "Enables dynamic shapes for the input tensor.\n"
    "Dynamic shapes allow exporting the model to ONNX with flexible input sizes, "
    "meaning the model can handle varying batch sizes or dimensions at runtime.\n\n"
    "When enabled:\n- The batch size will be marked as dynamic (-1).\n\n"
    "Use this if your model needs to support inputs of varying sizes."
)

DATA_TYPE_TOOLTIP = (
    "Specifies the data type for the input tensor.\n"
    "Common data types include:\n"
    "- torch.float32 (default): 32-bit floating-point numbers.\n"
    "- torch.int32: 32-bit integers.\n"
    "- torch.bool: Boolean values (True/False).\n\n"
    "Choose the appropriate data type based on your model's requirements."
)

TENSOR_VALUE_TOOLTIP = (
    "Specifies how the values in the input tensor are initialized.\n"
    "Options include:\n"
    "- Random: Values are generated randomly.\n"
    "- Zeros: All values are set to zero.\n"
    "- Ones: All values are set to one.\n\n"
    "Use 'Random' for typical scenarios, or specific values for testing."
)

SAVE_PATH_TOOLTIP = (
    "Specifies the file path where the exported ONNX model will be saved.\n\n"
    "Use the 'Browse' button to select a location or manually enter a valid path."
)

BROWSE_BUTTON_TOOLTIP = (
    "Opens a file dialog to select the location where the ONNX model will be saved.\n"
    "Ensure the file path is writable and has a .onnx extension."
)

OK_BUTTON_TOOLTIP = (
    "Starts the export process using the specified parameters.\n"
    "Ensure all fields are correctly filled before proceeding."
)

CANCEL_BUTTON_TOOLTIP = (
    "Closes this dialog without exporting the model.\n"
    "All unsaved changes will be discarded."
)

