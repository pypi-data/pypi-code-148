    def download_pic(self, htmls):
            htmls = htmls.split('\n')
            img_urls = []
            for html in htmls:
                if html == '':
                    continue
                for img_url in get_img_src(html, set_proxy=True):
                    img_urls.append(img_url)

            # 处理 telegra.sh 的图片
            if 'https' not in img_urls[0]:
                img_urls = list('https://telegra.ph' + i for i in img_urls)
                folder = "C:/Users/24172/Downloads/pic"
                d = Download(img_urls, folder)
                d.normal()
                exit()

            folder = "C:/Users/24172/Downloads/pic"
            d = Download(img_urls, folder, set_proxy=True)
            d.concurrent()
            return '下载完成！'