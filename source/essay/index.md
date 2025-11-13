---
title: 即刻短文
date: 2023-01-17 13:38:17
top_img: false
aside: false
top_page: true
top_bg: https://images1.blog.sinzmise.top/images/40311014_1591849369.969sikabhl.webp
top_item: 即刻短文
top_title: 一颗颗故事的种子
top_tips: 使用 哔哔点啥 2.0 By Memos 构建
top_link: /link/
top_text: 友情链接
comments: false
---
<center>
<span onclick="randomMemo()">回忆</span>
<span onclick="serchMemo()">搜索</span>
<span onclick="setOpenID()">设置</span> · 
<span onclick="showTaglist(this)" data-api="https://tag.diary.storisinz.site/">分类</span>

<link rel="icon" href="https://cdn.jsdmirror.com/gh/zhao2022-Ux/memos-blog/public/assets/img/logo.webp" type="image/*" />
<link href="https://cdn.jsdmirror.com/gh/zhao2022-Ux/memos-blog/public/assets/css/style.css" rel="stylesheet" type="text/css"> 
<link href="https://cdn.jsdmirror.com/gh/zhao2022-Ux/memos-blog/public/assets/css/APlayer.min.css" rel="stylesheet" type="text/css">
<link href="https://cdn.jsdmirror.com/gh/zhao2022-Ux/memos-blog/public/assets/css/highlight.github.min.css" rel="stylesheet" type="text/css">
<link href="https://cdn.jsdmirror.com/gh/zhao2022-Ux/memos-blog/public/assets/css/custom.css" rel="stylesheet" type="text/css">

<section id="main" class="container">
	<blockquote>
		<p>Je <del>memos</del>, donc je suis - <em>René Descartes fans</em></p>
    </blockquote>
    <blockquote id="tag-filter" class="filter">
	    <div id="tags"></div>
    </blockquote>
    <div id="memos" class="memos">
	    <!-- Memos Container -->
    </div>
</section>

<script type="text/javascript">
	var memos = {
		host: 'https://memos.xzy404.me/',  // Your Memos instance.
		limit: '20',	// Pagination to show.
		creatorId: '1',  // The old instance is 101, and the new instance is 1. 
		domId: '#memos',	// Default #memos.
		username: 'xzy',	// You can customize the display ID that is not related to memos.
		name: 'Mascot',	// You can customize the displayed full name, that is not related to memos.
		language: 'zh-CN', // 'en' 'zh-CN' etc. Used by Relative Time.
		APIVersion: 'legacy',
		total: true, // Display total memos. No interface is displayed in the new version.
    }
</script>

<script type="text/javascript" src="https://cdn.jsdmirror.com/gh/zhao2022-Ux/memos-blog/public/assets/js/marked.umd.min.js?v=14.0.0"></script>
<script type="text/javascript" src="https://cdn.jsdmirror.com/gh/zhao2022-Ux/memos-blog/public/assets/js/view-image.min.js"></script>
<script type="text/javascript" src="https://cdn.jsdmirror.com/gh/zhao2022-Ux/memos-blog/public/assets/js/APlayer.min.js"></script>
<script type="text/javascript" src="https://cdn.jsdmirror.com/gh/zhao2022-Ux/memos-blog/public/assets/js/Meting.min.js"></script>
<script type="text/javascript" src="https://cdn.jsdmirror.com/gh/zhao2022-Ux/memos-blog/public/assets/js/main.js"></script>
<script type="text/javascript" src="https://cdn.jsdmirror.com/gh/zhao2022-Ux/memos-blog/public/assets/js/custom.js"></script>
