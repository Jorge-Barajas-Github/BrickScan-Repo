from pathlib import Path
import shutil

SOURCE_DIR = Path("data/processed")
TARGET_DIR = Path("data/processed_top20")

SPLITS = ["train", "val", "test"]
TOP_N = 20


def count_images(class_dir: Path) -> int:
    exts = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
    return sum(1 for f in class_dir.rglob("*") if f.is_file() and f.suffix.lower() in exts)


def get_class_counts():
    total_counts = {}

    for split in SPLITS:
        split_dir = SOURCE_DIR / split
        if not split_dir.exists():
            raise FileNotFoundError(f"Missing split folder: {split_dir}")

        for class_dir in split_dir.iterdir():
            if class_dir.is_dir():
                total_counts.setdefault(class_dir.name, 0)
                total_counts[class_dir.name] += count_images(class_dir)

    return total_counts


def copy_selected_classes(selected_classes):
    if TARGET_DIR.exists():
        raise FileExistsError(
            f"{TARGET_DIR} already exists. Delete it first or choose a new target folder."
        )

    for split in SPLITS:
        src_split = SOURCE_DIR / split
        dst_split = TARGET_DIR / split
        dst_split.mkdir(parents=True, exist_ok=True)

        for class_name in selected_classes:
            src_class = src_split / class_name
            dst_class = dst_split / class_name

            if src_class.exists():
                shutil.copytree(src_class, dst_class)


def main():
    class_counts = get_class_counts()

    sorted_classes = sorted(
        class_counts.items(),
        key=lambda x: x[1],
        reverse=True
    )

    selected = sorted_classes[:TOP_N]

    print(f"Top {TOP_N} classes by total image count:")
    for class_name, count in selected:
        print(f"{class_name}: {count}")

    selected_class_names = [class_name for class_name, _ in selected]

    copy_selected_classes(selected_class_names)

    print(f"\nCreated filtered dataset at: {TARGET_DIR}")
    print("Selected classes:")
    print(selected_class_names)


if __name__ == "__main__":
    main()