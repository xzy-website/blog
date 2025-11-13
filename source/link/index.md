---
aside: false
date: '2020-12-01T22:19:45+08:00'
title: 友人帐
top_img: false
type: link
updated: '2025-07-13T09:48:10.435+08:00'
---

<div id="container" tabindex="0"></div>
<script src="https://cdn.hellolin.top/gh/linusxiong/chrome_dino_game/runner.js"></script>
<script>
    initRunner('#container');
    const gameContainer = document.querySelector('#container');
    gameContainer.focus();
    document.addEventListener('keydown', function(event) {
        if (event.code === 'Space' || event.code === 'ArrowUp') {
            event.preventDefault();
            gameContainer.focus();
        }
        if (['KeyW', 'KeyA', 'KeyS', 'KeyD', 'ArrowDown'].includes(event.code)) {
            event.preventDefault();
            gameContainer.focus();
        }
    });
    gameContainer.addEventListener('click', function() {
        gameContainer.focus();
    });
</script>

# 友链交换规则

1. 站点可以在中国大陆区域（IP）正常访问且内容符合中国大陆法律法规；
2. 站点友情链接含本站链接；
3. 站点类型不限，但如果为博客会更加容易通过；
4. 由于 xzy 不是经常上线，可以[邮箱](mailto:XiaofanMango@outlook.com)或各种方式催促交换！
   {% tabs 友链添加方式 %}

<!-- tab General -->


| 名称       | 值                                                                                |
| ---------- | --------------------------------------------------------------------------------- |
| 站点名称   | xzy の 未知屋                                                                     |
| 站点地址   | https://xzy404.me                                                                 |
| 站点描述   | An OIer の Profile の Profile                                                     |
| 站点图像   | https://cdn.luogu.com.cn/upload/usericon/1062508.png                              |
| 站点页面   | https://image.thum.io/get/allowJPG/wait/20/width/600/crop/950/https://xzy404.me// |
| 站点关键词 | xzy,个人博客                                                                      |
| rss链接    | https://xzy404.me//atom.xml                                                       |

<!-- endtab -->

<!-- tab Butterfly(anzhiyu) & MengD -->

```yml
- name: xzy の 未知屋
  link: https://xzy404.me
  avatar: https://cdn.luogu.com.cn/upload/usericon/1062508.png
  descr: An OIer の Profile
  siteshot: https://image.thum.io/get/allowJPG/wait/20/width/600/crop/950/https://xzy404.me
  theme_color: "#e66744"
```

<!-- endtab -->

<!-- tab Volantis -->

```yml
- name: xzy の 未知屋
  link: https://xzy404.me
  avatar: https://cdn.luogu.com.cn/upload/usericon/1062508.png
  description: An OIer の Profile
  keywords: xzy，个人博客
  screenshot: https://image.thum.io/get/allowJPG/wait/20/width/600/crop/950/https://xzy404.me
```

<!-- endtab -->

<!-- tab Yun -->

```json
{
    "url": "https://xzy404.me",
    "avatar": "https://cdn.luogu.com.cn/upload/usericon/1062508.png",
    "name": "xzy",
    "color": "#e66744", //或者 #ef9140
    "blog": "xzy の 未知屋", 
    "desc": "An OIer の Profile"
}
```

<!-- endtab -->

<!-- tab fluid -->

```yml
- {
  name: 'xzy の 未知屋',
  intro: 'An OIer の Profile',
  link: 'https://xzy404.me',
  avatar: 'https://cdn.luogu.com.cn/upload/usericon/1062508.png'
}
```

<!-- endtab -->

<!-- tab Html -->

```html
<a href="https://xzy404.me"><img src="https://cdn.luogu.com.cn/upload/usericon/1062508.png" alt="avatar">xzy の 未知屋</a>
```

<!-- endtab -->

<!-- tab jade -->

```pug
a(href='https://xzy404.me')
  img(src='https://cdn.luogu.com.cn/upload/usericon/1062508.png', alt='avatar') xzy の 未知屋
```

或者

```pug
a(href='https://xzy404.me' rel="external nofollow") xzy の 未知屋
```

<!-- endtab -->

{% endtabs %}

# 友链交换方式

## 注意事项

1. 洛谷的友链为每次部署或凌晨 2:00 通过 Github Action 自动生成至 links.yml ，请勿通过 PR 更改，唯一方式是洛谷私信 @xzy_awa 让 ta 关注你即可，请注意关注并非立刻生效，请等待至 2:00 A.M. 后。
2. 唯一可以申请的友链文件位于 `links-fixed.yml`，请注意区分。

## 评论区申请

<div class="addBtns"><button class="addBtn btn-beautify block orange larger" onclick="leonus.linkCom()"><i class="fa-solid fa-circle-plus"></i> 点击此处进行申请 </button>

## Github 申请

自行发起 PR：[xzy-website/blog](https://github.com/xzy-website/blog)。

注意⚠️：友链文件位于 links-fixed.yml，不要更改错误，并且在发布 PR 后请 @zhao2022-Ux



<link rel="stylesheet" href="https://jsd.cdn.sinzmise.top/npm/qexo-static@1.6.0/hexo/friends.css"/>

<link rel="stylesheet" href="/css/apursuer-hexo-friend-links.css"/>
