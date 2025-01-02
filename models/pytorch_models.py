MODELS = {
    "Classification": {
        "ResNet": {
            "models": {
                "resnet18": {
                    "weights": ["IMAGENET1K_V1", "IMAGENET1K_V2"],
                    "description": "ResNet18 model for image classification.",
                },
                "resnet50": {
                    "weights": ["IMAGENET1K_V1", "IMAGENET1K_V2"],
                    "description": "ResNet50 model for image classification.",
                },
            },
            "description": "Residual Networks (ResNet) for image classification.",
        },
        "EfficientNet": {
            "models": {
                "efficientnet_b0": {
                    "weights": ["IMAGENET1K_V1"],
                    "description": "EfficientNet B0 for image classification.",
                },
                "efficientnet_b1": {
                    "weights": ["IMAGENET1K_V1", "IMAGENET1K_V2"],
                    "description": "EfficientNet B1 for image classification.",
                },
            },
            "description": "EfficientNet models for scalable and efficient image classification.",
        },
    },
    "Object Detection": {
        "Faster R-CNN": {
            "models": {
                "fasterrcnn_resnet50_fpn": {
                    "weights": ["COCO_V1"],
                    "description": "Faster R-CNN with ResNet50 backbone.",
                },
                "fasterrcnn_mobilenet_v3_large_fpn": {
                    "weights": ["COCO_V1"],
                    "description": "Faster R-CNN with MobileNetV3 backbone.",
                },
            },
            "description": "Faster R-CNN for object detection.",
        },
    },
    "Semantic Segmentation": {
        "DeepLabV3": {
            "models": {
                "deeplabv3_resnet50": {
                    "weights": ["COCO_WITH_VOC_LABELS_V1"],
                    "description": "DeepLabV3 with ResNet50 backbone for segmentation.",
                },
                "deeplabv3_mobilenet_v3_large": {
                    "weights": ["COCO_WITH_VOC_LABELS_V1"],
                    "description": "DeepLabV3 with MobileNetV3 backbone for segmentation.",
                },
            },
            "description": "DeepLabV3 models for semantic segmentation.",
        },
    },
}
