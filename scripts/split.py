import random
import shutil
from pathlib import Path

RAW_ROOT = Path(r"data\raw\lego_extracted")   # Category/BrickID/images
OUT_ROOT = Path(r"data\processed")           # train/val/test output

TRAIN, VAL, TEST = 0.80, 0.10, 0.10
SEED = 6767
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}

def main():
    random.seed(SEED)

    # Create split root folders
    for split in ("train", "val", "test"):
        (OUT_ROOT / split).mkdir(parents=True, exist_ok=True)

    # Loop: Category -> BrickID -> images
    for category_dir in RAW_ROOT.iterdir():
        if not category_dir.is_dir():
            continue

        for brick_dir in category_dir.iterdir():
            if not brick_dir.is_dir():
                continue

            class_name = brick_dir.name  # BrickID becomes the class label

            images = [
                p for p in brick_dir.iterdir()
                if p.is_file() and p.suffix.lower() in IMAGE_EXTS
            ]

            # (Assuming every class has images, per your note)
            random.shuffle(images)

            n = len(images)
            n_train = int(n * TRAIN)
            n_val = int(n * VAL)

            train_imgs = images[:n_train]
            val_imgs = images[n_train:n_train + n_val]
            test_imgs = images[n_train + n_val:]

            # Create class folders
            (OUT_ROOT / "train" / class_name).mkdir(parents=True, exist_ok=True)
            (OUT_ROOT / "val" / class_name).mkdir(parents=True, exist_ok=True)
            (OUT_ROOT / "test" / class_name).mkdir(parents=True, exist_ok=True)

            # Copy images into split folders
            for p in train_imgs:
                shutil.copy2(p, OUT_ROOT / "train" / class_name / p.name)
            for p in val_imgs:
                shutil.copy2(p, OUT_ROOT / "val" / class_name / p.name)
            for p in test_imgs:
                shutil.copy2(p, OUT_ROOT / "test" / class_name / p.name)

            print(f"{class_name}: {len(train_imgs)} train, {len(val_imgs)} val, {len(test_imgs)} test")

    print("Done. Splits created at:", OUT_ROOT.resolve())

if __name__ == "__main__":
    main()
