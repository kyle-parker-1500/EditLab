from PIL import Image

# credit goes to haruka for the idea of the eraser and the implementation
# I (kyle) didn't realize that I couldn't use Pillow as an eraser due to how javascript updates things
# so I wasn't able to use it in the final product.

def erase_area(image_path, x, y, size=20):
    """
    image_path: 編集する画像のパス
    x, y: 消したい中心座標（フロントエンドから送られる）
    size: 消しゴムの半径（px）
    """

    # 画像をRGBAとして開く（透明を扱うため）
    img = Image.open(image_path).convert("RGBA")
    pixels = img.load()

    # 消しゴムの範囲を走査
    for dy in range(-size, size):
        for dx in range(-size, size):

            # 円形にしたいので距離で判定
            if dx*dx + dy*dy <= size*size:

                # 実際の座標
                px = x + dx
                py = y + dy

                # 画像範囲内なら透明にする
                if 0 <= px < img.width and 0 <= py < img.height:
                    pixels[px, py] = (0, 0, 0, 0)

    return img