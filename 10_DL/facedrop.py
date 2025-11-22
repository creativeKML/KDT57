import os, cv2
import mediapipe as mp

SRC_ROOT = r"C:\Users\KDT-57-\OneDrive\Desktop\KDT9\[10] DL\PROJECT\second_idol"
DST_ROOT = r"C:\Users\KDT-57-\OneDrive\Desktop\KDT9\[10] DL\PROJECT\second_idol_faces"
os.makedirs(DST_ROOT, exist_ok=True)


mp_fd = mp.solutions.face_detection
fd = mp_fd.FaceDetection(model_selection=1, min_detection_confidence=0.5)  # 원거리 얼굴엔 model_selection=1

VALID_EXTS = {".jpg",".jpeg",".png",".bmp",".webp",".tif",".tiff"}
RESIZE_TO = (224, 224)

def ensure_dir(p): os.makedirs(p, exist_ok=True)

def process_image(src_path, dst_dir, base_name):
    img = cv2.imread(src_path)
    if img is None:
        print(f"[SKIP read error] {src_path}")
        return 0

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    res = fd.process(img_rgb)
    if not res.detections:
        print(f"[NO FACE] {src_path}")
        return 0

    h, w = img.shape[:2]
    saved = 0
    for i, det in enumerate(res.detections):
        bbox = det.location_data.relative_bounding_box
        x1 = max(0, int(bbox.xmin * w))
        y1 = max(0, int(bbox.ymin * h))
        x2 = min(w-1, int((bbox.xmin + bbox.width) * w))
        y2 = min(h-1, int((bbox.ymin + bbox.height) * h))

        pad = int(0.1 * max(x2-x1, y2-y1))
        xx1 = max(0, x1 - pad); yy1 = max(0, y1 - pad)
        xx2 = min(w-1, x2 + pad); yy2 = min(h-1, y2 + pad)

        crop = img[yy1:yy2, xx1:xx2]
        if RESIZE_TO:
            crop = cv2.resize(crop, RESIZE_TO, interpolation=cv2.INTER_AREA)
        cv2.imwrite(os.path.join(dst_dir, f"{base_name}_face{i}.jpg"), crop)
        saved += 1
    return saved

def main():
    total_imgs, total_saved = 0, 0
    for root, _, files in os.walk(SRC_ROOT):
        rel_dir = os.path.relpath(root, SRC_ROOT)
        dst_dir = os.path.join(DST_ROOT, rel_dir) if rel_dir != "." else DST_ROOT
        ensure_dir(dst_dir)
        for fname in files:
            ext = os.path.splitext(fname)[1].lower()
            if ext not in VALID_EXTS: 
                continue
            total_imgs += 1
            src_path  = os.path.join(root, fname)
            base_name = os.path.splitext(fname)[0]
            total_saved += process_image(src_path, dst_dir, base_name)

    print(f"Scanned: {total_imgs}, Saved faces: {total_saved}, Out: {DST_ROOT}")

if __name__ == "__main__":
    main()
