---
abbrlink: Game
categories:
- - 环境
date: '2025-04-15T21:10:21.331164+08:00'
description: null
mathjax: true
tags:
- 环境
title: game
updated: '2025-04-16T20:24:54.959+08:00'
---
```cpp
#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

int main()
{
    // ios::sync_with_stdio(false);
    // cin.tie(nullptr);
    // cout.tie(nullptr);
    cout << "Hello World!" << endl;
    return 0;
}
```

test 

<div class="tab-container">
  <div class="tab-buttons">
    <button class="tab-btn active" data-tab="webadmin">webadmin</button>
    <button class="tab-btn" data-tab="memos">memos</button>
  </div>
  
  <div class="tab-content">
    <div class="frame-wrapper">
      <iframe class="content-frame" data-src="https://webadmin.xzy404.me"></iframe>
      <button class="fullscreen-btn" title="全屏">⛶</button>
    </div>
  </div>
</div>

<style>
.tab-container {
  border: 1px solid #e1e5e9;
  border-radius: 8px;
  overflow: hidden;
  background: white;
}

.tab-buttons {
  display: flex;
  background: #f8f9fa;
  border-bottom: 1px solid #e1e5e9;
}

.tab-btn {
  padding: 12px 24px;
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 14px;
  color: #666;
  border-bottom: 2px solid transparent;
  transition: all 0.2s;
}

.tab-btn.active {
  color: #1890ff;
  border-bottom-color: #1890ff;
  background: white;
}

.tab-btn:hover:not(.active) {
  background: #f0f0f0;
}

.frame-wrapper {
  position: relative;
  height: 600px;
}

.content-frame {
  width: 100%;
  height: 100%;
  border: none;
  background: white;
}

.fullscreen-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 4px;
  background: rgba(0,0,0,0.6);
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  transition: background 0.2s;
}

.fullscreen-btn:hover {
  background: rgba(0,0,0,0.8);
}
</style>

<script>
const tabBtns = document.querySelectorAll('.tab-btn');
const frame = document.querySelector('.content-frame');
const fullscreenBtn = document.querySelector('.fullscreen-btn');

tabBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    tabBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    
    const targetSrc = btn.dataset.tab === 'webadmin' 
      ? 'https://webadmin.xzy404.me'
      : 'http://43.247.135.19:5230';
    
    frame.src = targetSrc;
  });
});

fullscreenBtn.addEventListener('click', () => {
  if (!document.fullscreenElement) {
    frame.requestFullscreen().catch(err => {
      console.error('全屏失败:', err);
    });
  } else {
    document.exitFullscreen();
  }
});

// 初始化加载webadmin
frame.src = 'https://webadmin.xzy404.me';
</script>
