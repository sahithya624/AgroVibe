
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, models, transforms
import os
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def train_model():
    # Configuration
    DATA_DIR = "backend/ml_models/datasets/plant_disease"
    MODEL_SAVE_PATH = "backend/ml_models/saved_models/disease_resnet18.pth"
    CLASSES_SAVE_PATH = "backend/ml_models/saved_models/classes.json"
    BATCH_SIZE = 32
    NUM_EPOCHS = 5  # Start with 5 epochs for quick fine-tuning
    LEARNING_RATE = 0.001

    # check if data directory exists
    if not os.path.exists(DATA_DIR):
        logger.error(f"Data directory not found: {DATA_DIR}")
        return

    # Data transformations
    data_transforms = {
        'train': transforms.Compose([
            transforms.RandomResizedCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
        'val': transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
    }

    # Load datasets
    image_datasets = {}
    dataloaders = {}
    dataset_sizes = {}
    
    for x in ['train', 'val']:
        path = os.path.join(DATA_DIR, x)
        if not os.path.exists(path):
            logger.warning(f"{x} directory not found at {path}. using train for both if needed or skipping.")
            # Fallback if val doesn't exist, just use train but split or skip
            continue
            
        image_datasets[x] = datasets.ImageFolder(path, data_transforms[x])
        dataloaders[x] = torch.utils.data.DataLoader(image_datasets[x], batch_size=BATCH_SIZE, shuffle=True, num_workers=0)
        dataset_sizes[x] = len(image_datasets[x])

    if 'train' not in image_datasets:
        logger.error("Train dataset not found!")
        return

    class_names = image_datasets['train'].classes
    num_classes = len(class_names)
    logger.info(f"Found {num_classes} classes: {class_names}")

    # Set device
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    logger.info(f"Using device: {device}")

    # Load pre-trained ResNet18
    model = models.resnet18(pretrained=True)
    
    # Freeze initial layers (optional, but good for small datasets)
    # for param in model.parameters():
    #     param.requires_grad = False

    # Replace final layer
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, num_classes)

    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=LEARNING_RATE, momentum=0.9)
    # Decay LR by a factor of 0.1 every 7 epochs
    exp_lr_scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=7, gamma=0.1)

    # Training loop
    logger.info("Starting training...")
    
    for epoch in range(NUM_EPOCHS):
        logger.info(f'Epoch {epoch+1}/{NUM_EPOCHS}')
        logger.info('-' * 10)

        for phase in ['train', 'val']:
            if phase not in dataloaders:
                continue

            if phase == 'train':
                model.train()
            else:
                model.eval()

            running_loss = 0.0
            running_corrects = 0

            for inputs, labels in dataloaders[phase]:
                inputs = inputs.to(device)
                labels = labels.to(device)

                optimizer.zero_grad()

                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model.forward(inputs)
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)

                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)

            if phase == 'train':
                exp_lr_scheduler.step()

            epoch_loss = running_loss / dataset_sizes[phase]
            epoch_acc = running_corrects.double() / dataset_sizes[phase]

            logger.info(f'{phase} Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}')

    # Save model
    os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)
    torch.save(model.state_dict(), MODEL_SAVE_PATH)
    logger.info(f"Model saved to {MODEL_SAVE_PATH}")

    # Save classes
    with open(CLASSES_SAVE_PATH, 'w') as f:
        json.dump(class_names, f)
    logger.info(f"Classes saved to {CLASSES_SAVE_PATH}")

if __name__ == "__main__":
    train_model()
