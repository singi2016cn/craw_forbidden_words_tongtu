import muggle_ocr

def ocrCap(captcha):
    with open(captcha, "rb") as f:
        captcha_bytes = f.read()

    # ModelType.Captcha 可识别4-6位验证码
    sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)
    text = sdk.predict(image_bytes=captcha_bytes)
    return text

def pageData(html):
    res = []
    for i in range(0, 50):
        word = html.xpath('//*[@id="datagrid-row-r1-2-'+ str(i) +'"]/td[1]/div//text()')
        if len(word) == 0:
            break
        res.append(word[0].strip())
    return res
