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
def chroma_key_with_img(foreground_path, background_path, color, threshold=100):
    src = Image.open(foreground_path).convert("RGB") 
    bg = Image.open(background_path).convert("RGB") 

    # resize images to match
    if src.size != bg.size:
        bg = bg.resize(src.size, Image.LANCZOS)
        
    result = src.convert("RGBA")
    pixels_result = result.load()
    pixels_bg = bg.load()
    
    for x in range(result.width):
       for y in range(result.height):
            r, g, b, a = pixels_result[x, y] 
            cur_pixel = (r, g, b)

            # get distance
            distance = (
                (cur_pixel[0] - color[0])**2 +
                (cur_pixel[1] - color[1])**2 +
                (cur_pixel[2] - color[2])**2        
            )

            if distance < threshold * threshold:
                bg_r, bg_g, bg_b = pixels_bg[x, y]
                pixels_result[x, y] = (bg_r, bg_g, bg_b, 255)
     
    return result 

