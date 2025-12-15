from PIL import Image

def chroma_key(foreground_path, bg_color, threshold=60):
    """
    foreground_path: ユーザーがアップロードした画像のパス
    bg_color: (R, G, B) のタプル。消したい色
    threshold: 色の許容差（大きいほど広く色が消える）
    """

    # 画像を開く
    img = Image.open(foreground_path).convert("RGB")

    # 出力用にRGBA画像を作成（透明を扱うため）
    result = img.convert("RGBA")
    pixels = result.load()

    # 指定色にどれだけ近いかを判定して透明にする
    for y in range(result.height):
        for x in range(result.width):

            r, g, b, a = pixels[x, y]

            # 現在の画素と背景色の距離を計算
            diff = abs(r - bg_color[0]) + abs(g - bg_color[1]) + abs(b - bg_color[2])

            # 近い色なら透明にする
            if diff < threshold:
                pixels[x, y] = (0, 0, 0, 0)

    return result
