import os
from pathlib import Path
from collections import Counter

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms, models
from sklearn.model_selection import train_test_split
from PIL import Image

# -------------------------------
# [1] 경로 설정
# -------------------------------
DATA_ROOT = r"C:\Users\KDT-57-\OneDrive\Desktop\KDT9\[10] DL\PROJECT\second_idol_faces"
NEW_IMAGE_DIR = r"C:\Users\KDT-57-\OneDrive\Desktop\KDT9\[10] DL\PROJECT\New_image"
VALID_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 5
LR = 1e-4

# -------------------------------
# [2] 커스텀 Dataset
# -------------------------------
class IdolMemberDataset(Dataset):
    def __init__(self, filepaths, labels, transform=None):
        self.filepaths = filepaths
        self.labels = labels
        self.transform = transform
    def __len__(self):
        return len(self.filepaths)
    def __getitem__(self, idx):
        img = Image.open(self.filepaths[idx]).convert("RGB")
        if self.transform:
            img = self.transform(img)
        return img, self.labels[idx]

# -------------------------------
# [3] 데이터셋 로더 함수
# -------------------------------
def load_dataset_by_member(DATA_ROOT, img_size=224, val_ratio=0.2, seed=42):
    root = Path(DATA_ROOT)

    files, members = [], []
    for group_dir in sorted([p for p in root.iterdir() if p.is_dir()]):
        for member_dir in sorted([p for p in group_dir.iterdir() if p.is_dir()]):
            member_name = member_dir.name
            imgs = [str(p) for p in member_dir.rglob("*") if p.suffix.lower() in VALID_EXTS]
            files.extend(imgs)
            members.extend([member_name] * len(imgs))

    if len(files) == 0:
        raise RuntimeError("이미지가 없습니다. 폴더 구조 확인하세요.")

    classes = sorted(list(set(members)))
    class_to_idx = {c: i for i, c in enumerate(classes)}
    labels = [class_to_idx[m] for m in members]

    print("총 이미지 개수:", len(files))
    print("클래스(멤버) 수:", len(classes))
    print("예시 클래스:", classes[:10])

    train_files, val_files, train_labels, val_labels = train_test_split(
        files, labels, test_size=val_ratio, stratify=labels, random_state=seed
    )

    print("train:", len(train_files), "val:", len(val_files))

    tf_train = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.RandomHorizontalFlip(),
        transforms.ColorJitter(0.2,0.2,0.2,0.1),
        transforms.ToTensor(),
        transforms.Normalize((0.5,0.5,0.5),(0.5,0.5,0.5)),
    ])
    tf_val = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.ToTensor(),
        transforms.Normalize((0.5,0.5,0.5),(0.5,0.5,0.5)),
    ])

    train_ds = IdolMemberDataset(train_files, train_labels, tf_train)
    val_ds   = IdolMemberDataset(val_files, val_labels, tf_val)
    return train_ds, val_ds, classes, class_to_idx

# -------------------------------
# [4] 모델 정의 (ResNet18 Fine-tuning)
# -------------------------------
def build_resnet(num_classes):
    model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
    for param in model.parameters():
        param.requires_grad = False  # 특징 추출기로 사용
    in_features = model.fc.in_features
    model.fc = nn.Linear(in_features, num_classes)  # 마지막 FC 교체
    return model

# -------------------------------
# [5] 학습 루프
# -------------------------------
def train_model(model, train_dl, val_dl, epochs=5, lr=1e-4):
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.fc.parameters(), lr=lr)

    for epoch in range(epochs):
        model.train()
        total_loss, total_correct = 0, 0
        for imgs, labels in train_dl:
            imgs, labels = imgs.to(DEVICE), labels.to(DEVICE)
            optimizer.zero_grad()
            outputs = model(imgs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item() * imgs.size(0)
            total_correct += (outputs.argmax(1) == labels).sum().item()
        avg_loss = total_loss / len(train_dl.dataset)
        avg_acc = total_correct / len(train_dl.dataset)

        # 검증
        model.eval()
        val_loss, val_correct = 0, 0
        with torch.no_grad():
            for imgs, labels in val_dl:
                imgs, labels = imgs.to(DEVICE), labels.to(DEVICE)
                outputs = model(imgs)
                loss = criterion(outputs, labels)
                val_loss += loss.item() * imgs.size(0)
                val_correct += (outputs.argmax(1) == labels).sum().item()
        val_loss /= len(val_dl.dataset)
        val_acc = val_correct / len(val_dl.dataset)

        print(f"[{epoch+1}/{epochs}] Train Loss {avg_loss:.4f} Acc {avg_acc:.4f} | Val Loss {val_loss:.4f} Acc {val_acc:.4f}")

    return model

# -------------------------------
# [6] 새로운 이미지 예측 함수
# -------------------------------
def predict_new_images(model, new_dir, classes, img_size=224):
    tf = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.ToTensor(),
        transforms.Normalize((0.5,0.5,0.5),(0.5,0.5,0.5)),
    ])

    for img_file in Path(new_dir).glob("*"):
        if img_file.suffix.lower() not in VALID_EXTS:
            continue
        img = Image.open(img_file).convert("RGB")
        x = tf(img).unsqueeze(0).to(DEVICE)
        with torch.no_grad():
            output = model(x)
            pred_idx = output.argmax(1).item()
            print(f"[{img_file.name}] → 닮은꼴: {classes[pred_idx]}")

# -------------------------------
# [7] 실행
# -------------------------------
if __name__ == "__main__":
    train_ds, val_ds, classes, class_to_idx = load_dataset_by_member(DATA_ROOT, img_size=IMG_SIZE)

    train_dl = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True)
    val_dl   = DataLoader(val_ds, batch_size=BATCH_SIZE)

    model = build_resnet(num_classes=len(classes)).to(DEVICE)
    model = train_model(model, train_dl, val_dl, epochs=EPOCHS, lr=LR)

    # 새로운 이미지 예측
    predict_new_images(model, NEW_IMAGE_DIR, classes, img_size=IMG_SIZE)
