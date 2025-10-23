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

## 评论区申请

<div class="addBtns"><button class="addBtn btn-beautify block orange larger" onclick="leonus.linkCom()"><i class="fa-solid fa-circle-plus"></i> 点击此处进行申请 </button>

## Github 申请

自行发起 PR：[xzy-website/blog](https://github.com/xzy-website/blog)。

## Qexo 申请

<article class="message is-info">
    <div class="message-header">
        通过 Qexo 申请友链。
    </div>
    <div class="message-body">
        <div class="form-ask-friend">
            <div class="field">
                <label class="label">友链名称</label>
                <div class="control has-icons-left">
                    <input class="input" type="text" placeholder="例：xzy の 未知屋" id="friend-name" required>
                    <span class="icon is-small is-left">
                        <i class="fas fa-signature"></i>
                    </span>
                </div>
            </div>
            <div class="field">
                <label class="label">友链链接</label>
            <div class="control has-icons-left">
                <input class="input" type="url" placeholder="例：https://xzy404.me" id="friend-link" required>
                <span class="icon is-small is-left">
                    <i class="fas fa-link"></i>
                </span>
            </div>
            <p class="help ">注：请确保该网站符合友链交换规则！</p>
            </div>
            <div class="field">
                <label class="label">友链图标</label>
                <div class="control has-icons-left">
                    <input class="input" type="url" placeholder="例：https://cdn.luogu.com.cn/upload/usericon/1062508.png" id="friend-icon" required>
                    <span class="icon is-small is-left">
                        <i class="fas fa-image"></i>
                    </span>
                </div>
            </div>
            <div class="field">
                <label class="label">友链简介</label>
                <div class="control has-icons-left">
                    <input class="input" type="text" placeholder="例：An OIer の Profile" id="friend-des" required>
                    <span class="icon is-small is-left">
                        <i class="fas fa-info"></i>
                    </span>
                </div>
            </div>
            <div class="field">
                <div class="control">
                    <label class="checkbox">
                        <input type="checkbox" id="friend-check"/> 我不会提交无意义的友链申请，并且保证友链符合友链交换申请规则。
                    </label>
                </div>
            </div>
            <div class="field is-grouped">
                <div class="control">
                    <button class="button is-info" type="submit" onclick="askFriend(event)">提交！</button>
                </div>
            </div>
        </div>
    </div>
</article>
<script data-pjax src="https://recaptcha.net/recaptcha/api.js?render=6LftRhgrAAAAAE_YJ-KXKavs_DABCjPY1_VckqrJ"></script>
<script data-pjax>
function TestUrl(url) {
    var Expression=/http(s)?:\/\/([\w-]+\.)+[\w-]+(\/[\w- .\/?%&=]*)?/;
    var objExp=new RegExp(Expression);
    if(objExp.test(url) != true){
        return false;
    }
    return true;
}
function askFriend (event) {
    let check = $("#friend-check").is(":checked");
    let name = $("#friend-name").val();
    let url = $("#friend-link").val();
    let image = $("#friend-icon").val();
    let des = $("#friend-des").val();
    if(!check){
        alert("Please check \"I am not submitting nonsense information\"");
        return;
    }
    if(!(name&&url&&image&&des)){
        alert("The information is incomplete! ");
        return;
    }
    if (!(TestUrl(url))){
        alert("URL format error! Need to include HTTP protocol header! ");
        return;
    }
    if (!(TestUrl(image))){
        alert("The format of the slice URL is wrong! It needs to contain the HTTP protocol header! ");
        return;
    }
    event.target.classList.add('is-loading');
    grecaptcha.ready(function() {
          grecaptcha.execute('6LftRhgrAAAAAE_YJ-KXKavs_DABCjPY1_VckqrJ', {action: 'submit'}).then(function(token) {
              $.ajax({
                type: 'get',
                cache: false,
                url: url,
                dataType: "jsonp",
                async: false,
                processData: false,
                //timeout:10000, 
                complete: function (data) {
                    if(data.status==200){
                    $.ajax({
                        type: 'POST',
                        dataType: "json",
                        data: {
                            "name": name,
                            "url": url,
                            "image": image,
                            "description": des,
                            "verify": token,
                        },
                        url: 'https://webadmin.xzy404.me/pub/ask_friend/',
                        success: function (data) {
                            alert(data.msg);
                        }
                    });}
                    else{
                        alert("The URL cannot be reached!");
                    }
                    event.target.classList.remove('is-loading');
                }
          });
        });
    });
}
</script>

<link rel="stylesheet" href="https://jsd.cdn.sinzmise.top/npm/qexo-static@1.6.0/hexo/friends.css"/>

<link rel="stylesheet" href="/css/apursuer-hexo-friend-links.css"/>
