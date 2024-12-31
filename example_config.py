config = {
    "data": {
        "train_dataset_path": "path/to/train",
        "validation_dataset_path": "path/to/validation",
        "test_dataset_path": "path/to/test",
        "batch_size": 32,
        "num_workers": 4,
        "shuffle_train_data": True,
        "data_augmentation": {"rotation": 30, "horizontal_flip": True},
    },
    "training": {
        "epochs": 50,
        "device": "cuda",
        "seed": 42,
        "gradient_clipping": 5.0,
        "accumulation_steps": 2,
        "mixed_precision": True,
    },
    "optimization": {
        "optimizer": "Adam",
        "learning_rate": 0.001,
        "momentum": 0.9,
        "weight_decay": 1e-4,
        "learning_rate_scheduler": "StepLR",
        "scheduler_params": {"step_size": 10, "gamma": 0.1},
    },
    "loss": {
        "loss_function": "CrossEntropyLoss",
        "loss_weights": [0.7, 0.3],
    },
    "checkpointing": {
        "save_model_path": "path/to/save",
        "checkpoint_interval": 5,
        "resume_from_checkpoint": None,
    },
    "logging": {
        "log_dir": "logs/",
        "log_interval": 10,
        "validation_interval": 1,
        "early_stopping": True,
        "early_stopping_patience": 10,
    },
    "evaluation": {
        "evaluation_metrics": ["accuracy", "precision", "recall", "F1"],
        "evaluation_thresholds": {"accuracy": 0.8},
    },
    "misc": {
        "experiment_name": "MyExperiment",
        "debug_mode": False,
        "save_config": True,
    },
}
