---
title: 朋友圈
date: 2024-05-02 12:01:50
top_img: false
aside: false
---
{% raw %}
<div id="friend-circle-lite-root"></div>
<script>
    if (typeof UserConfig === 'undefined') {
        var UserConfig = {
            // 填写你的fc Lite地址
            private_api_url: 'https://fc.blog.sinzmise.top/',
            // 点击加载更多时，一次最多加载几篇文章，默认20
            page_turning_number: 24,
            // 头像加载失败时，默认头像地址
            error_img: 'https://blog.storical.space//img/friend_404.gif',
        }
    }
</script>
<link rel="stylesheet" href="https://jsd.cdn.sinzmise.top/gh/willow-god/Friend-Circle-Lite/main/fclite.min.css">
<script src="https://jsd.cdn.sinzmise.top/gh/willow-god/Friend-Circle-Lite/main/fclite.min.js"></script>

{% endraw %}