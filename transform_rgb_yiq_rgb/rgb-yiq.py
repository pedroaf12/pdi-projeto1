def rgb_to_yiq(rgb):
    r,g,b = rgb[0], rgb[1], rgb[2]

    y = 0.299*r + 0.587*g + 0.114*b
    i = 0.596*r - 0.274*g - 0.322*b
    q = 0.211*r - 0.523*g + 0.312*b

    return y, i, q

def yiq_to_rgb(yiq):
    y, i, q = yiq[0], yiq[1], yiq[2]

    r = 1*y + 0.956*i + 0.621*q
    g = 1*y - 0.272*i - 0.647*q
    b = 1*y - 1.106*i + 1.703*q

    return round(r), round(g), round(b)

