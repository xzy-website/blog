---
abbrlink: 洛谷 P12172 题解
categories:
- - 题解
date: '2025-04-15T20:26:12.612675+08:00'
description: null
mathjax: true
tags:
- 题解
title: 题解：P12172 [蓝桥杯 2025 省 Python B] LQ 图形
updated: '2025-04-15T20:26:13.644+08:00'
---
# 题解：P12172 [蓝桥杯 2025 省 Python B] LQ 图形

## 思路

本题考察模拟。

不规则图形不方便输出？没关系，分成两部分（两个矩形）即可，大小分别为 $h \times w$ 和 $w \times (v + w)$。

## 代码

第一个矩形的输出代码：

```cpp
for (int i = 1; i <= h; i++)
{
    for (int j = 1; j <= w; j++)
        cout << "Q";
    cout << endl;
}
```

第二个矩形是差不多的，只需要调整 $i$ 和 $j$ 的范围即可。

完整代码：

```cpp
#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
int w, h, v;
int main()
{
    // ios::sync_with_stdio(false);
    // cin.tie(nullptr);
    // cout.tie(nullptr);
    cin >> w >> h >> v;
    for (int i = 1; i <= h; i++)
    {
        for (int j = 1; j <= w; j++)
            cout << "Q";
        cout << endl;
    }
    for (int i = 1; i <= w; i++)
    {
        for (int j = 1; j <= v + w; j++)
            cout << "Q";
        cout << endl;
    }
    return 0;
}
```
