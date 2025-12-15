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

# ---- KYLE FUNCTIONS TO HANDLE REPLACING PIXELS WITH IMAGE ----
def color_distance(pixel, color):
    return (
        (pixel[0] - color[0])**2 +
        (pixel[1] - color[1])**2 +
        (pixel[2] - color[2])**2        
    )

def chroma_key_with_img(src, bg, color, threshold):
    for x in range(src.width):
       for y in range(src.height):
           cur_pixel = src.getpixel((x,y))

           if color_distance(cur_pixel, color) < threshold:
               src.putpixel((x,y), bg.getpixel((x,y)))
      
    return src

