from PIL import Image

def reverse_chroma_key(foreground_path, target_color, threshold=60):
    """
    foreground_path: ユーザーがアップロードした画像のパス
    target_color: (R, G, B) のタプル。残したい色
    threshold: 色の許容差（大きいほど広く残る）
    """
    img = Image.open(foreground_path).convert("RGB")
    result = img.convert("RGBA")
    pixels = result.load()

    for y in range(result.height):
        for x in range(result.width):
            r, g, b, a = pixels[x, y]
            diff = abs(r - target_color[0]) + abs(g - target_color[1]) + abs(b - target_color[2])

            # 近い色だけ残す → それ以外は透明に
            if diff >= threshold:
                pixels[x, y] = (0, 0, 0, 0)

    return result