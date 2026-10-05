---
abbrlink: P17242 题解
categories:
- - 题解
date: '2026-10-05T20:19:11.570563+08:00'
description: null
mathjax: true
tags:
- 题解
title: 题解：P17242 [IOI 2026] 方块游戏 / tiling
updated: '2026-10-05T20:19:12.300+08:00'
---
# 题解：P17242 [IOI 2026] 方块游戏 / tiling

笑点解析：越南老哥切了个黑没切青：

![](https://cdn.luogu.com.cn/upload/image_hosting/1iz630pk.png)

## 思路

由于我们只关心方块中某一个白格的位置（如果有多个，按优先顺序取一个），其余视为黑色，因此把问题简化为“每个方块只有一个白格”。

我们把网格看成 $\mathrm{N} \times \mathrm{M}$ 个 $2 \times 2$ 的大块，每个大块用坐标 $(i,j)$ 表示，$0 \le i < \mathrm{N}, 0 \le j < \mathrm{M}$，实际左上角为 $(2 \times i, 2 \times j)$。

然后考虑放置规则：

- 若白格在右下（$\mathrm{BR}=0$），则倾向于放在“左上角”（$i+j$ 尽量小）的大块。
- 若白格在左下（$\mathrm{BL}=0$），则倾向于放在“右上角”（$i-j$ 尽量小）的大块。
- 若白格在右上（$\mathrm{TR}=0$），则倾向于放在“左下角”（$-i+j$ 尽量小）的大块。
- 若白格在左上（$\mathrm{TL}=0$），则倾向于放在“右下角”（$-i-j$ 尽量小）的大块。

这个规则确保了任意相邻大块之间的边界处都有白格交错，从而整个网格中任何一个 $2\times2$ 窗口（包括跨大块的）都不会全黑。

接下来考虑如何动态实现“取当前最小”？

我们预先对全部 $\mathrm{N} \times \mathrm{M}$ 个大块按照上述四种方式分别排序，得到四个排序后的数组 $\mathrm{sa}_{0 \dots 3}$。每个数组维护一个指针 $\mathrm{pos}_k$，指向下一个待考虑的元素。同时我们用一个二维布尔数组 $\mathrm{vis}_{i,j}$ 记录大块是否已被占用。

当收到方块并选定数组 $k$ 后，我们从 $\mathrm{pos}_k$ 开始往后扫描。先检查 $\mathrm{sa}_{k, \mathrm{pos}_k}$ 对应的大块，如果 $\mathrm{vis}$ 为 $\mathrm{true}$（已被别的顺序占用），说明这个位置不能用了，我们就将 $\mathrm{pos}_k$ 加 $1$，跳过它，继续检查下一个。

重复扫描直到找到一个 $\mathrm{vis}$ 为 $\mathrm{false}$ 的大块，它就是当前未使用中最小的那个（因为数组已升序排列，且指针之前的所有元素要么已用，要么已被跳过，不会再有未用的）。找到后，标记 $\mathrm{vis}$ 为 $\mathrm{true}$，然后将 $\mathrm{pos}_k$ 移动到该位置的下一个位置。这样，下次再来这个数组时，不会重复考虑已经扫描过的位置。

然后就做完了。

## 代码

```cpp
#include <bits/stdc++.h>
using namespace std;

int n, m;
vector<pair<int, int>> sa[4]; // 四个排序数组
int pos[4];                   // 每个数组当前的扫描位置
bool vis[105][105];           // 标记大块是否已被占用

// 按 i+j 升序
bool cmp0(const pair<int, int> &a, const pair<int, int> &b) { return a.first + a.second < b.first + b.second; }
// 按 i-j 升序
bool cmp1(const pair<int, int> &a, const pair<int, int> &b) { return a.first - a.second < b.first - b.second; }
// 按 -i+j 升序
bool cmp2(const pair<int, int> &a, const pair<int, int> &b) { return -a.first + a.second < -b.first + b.second; }
// 按 -i-j 升序
bool cmp3(const pair<int, int> &a, const pair<int, int> &b) { return -a.first - a.second < -b.first - b.second; }

void init(int N, int M)
{
    memset(vis, 0, sizeof(vis));
    for (int i = 0; i < 4; i++)
        pos[i] = 0;

    // 生成所有大块坐标
    vector<pair<int, int>> posa;
    posa.reserve(N * M);
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < M; j++)
            posa.push_back({i, j});
    }

    // 分别排序
    sa[0] = posa;
    sort(sa[0].begin(), sa[0].end(), cmp0);
    sa[1] = posa;
    sort(sa[1].begin(), sa[1].end(), cmp1);
    sa[2] = posa;
    sort(sa[2].begin(), sa[2].end(), cmp2);
    sa[3] = posa;
    sort(sa[3].begin(), sa[3].end(), cmp3);
}

pair<int, int> receive_block(int TL, int TR, int BL, int BR)
{
    int idx;
    if (!BR)
        idx = 0; // 右下白 -> 左上优先
    else if (!BL)
        idx = 1; // 左下白 -> 右上优先
    else if (!TR)
        idx = 2; // 右上白 -> 左下优先
    else
        idx = 3; // 左上白 -> 右下优先

    // 在 sa[idx] 中从 pos[idx] 开始找第一个未使用的大块
    auto &vec = sa[idx];
    int &p = pos[idx];
    while (p < (int)vec.size() && vis[vec[p].first][vec[p].second])
        ++p;
    // 题目保证一定有未使用的位置
    auto [i, j] = vec[p];
    vis[i][j] = true;
    ++p; // 指针移到下一个，提高后续效率
    return {i * 2, j * 2};
}
```
