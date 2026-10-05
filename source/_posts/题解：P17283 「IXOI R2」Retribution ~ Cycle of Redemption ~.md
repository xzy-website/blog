---
abbrlink: P17283 题解
categories:
- - 题解
date: '2026-10-05T20:21:40.648609+08:00'
description: null
mathjax: true
tags:
- 题解
title: 题解：P17283 「IXOI R2」Retribution ~ Cycle of Redemption ~
updated: '2026-10-05T20:21:41.445+08:00'
---
# 题解：P17283 「IXOI R2」Retribution ~ Cycle of Redemption ~

## 思路

我们希望最小的未出现在 LCA 集合中的点尽可能小。那么，对于一个固定的点 $v$，我们能不能构造一个大小至少为 $x$ 的集合，使得 $v$ 不出现在任何点对的 LCA 中？

如果可以，那么 $v$ 就可以成为 $\mathrm{mex}$ 的候选值。于是我们首先需要计算出，为了避开点 $v$，最多能选多少个点。

要避开 $v$，首先不能选 $v$ 本身；其次，不能从 $v$ 的两个不同儿子子树中各选点，否则它们的 LCA 就是 $v$。因此我们最多只能选择 $v$ 的一个儿子子树中的所有点，再加上所有不在 $v$ 子树内的点（这些点无论怎么选都不会产生 LCA 等于 $v$）。所以这个最大值就是

$$
f(v) = (n - \mathrm{size}(v)) + \max_{u \in \mathrm{son}(v)} \mathrm{size}(u)
$$

这里 $\mathrm{size}(v)$ 是以 $v$ 为根的子树大小，$\max\mathrm{size}(u)$ 是最大的儿子子树大小。

当我们知道所有点的 $f(v)$ 后，对于询问 $x$，如果存在某个点 $v$ 满足 $f(v) \ge x$，那么我们就可以避开 $v$，并且所有比 $v$ 小的点都必然会被包含（否则我们就能用更小的点来避开），所以最小的 $\mathrm{mex}$ 就是这些可行点中的最小编号。若没有这样的点，则 $\mathrm{mex}$ 为 $n$。于是问题简化为：对所有点，按 $f(v)$ 分组，记录每个 $f(v)$ 值对应的最小点编号，然后对 $f(v)$ 从大到小做后缀最小值，就能直接回答每个 $x$。

剩下的就是如何计算每个点的子树大小和最大儿子子树大小。以 $r$ 为根进行一次搜索，记录父节点和遍历顺序，然后逆序处理，累加子树大小并更新父节点的最大儿子值。整个过程只需一次遍历，复杂度 $O(n)$。

最终对于每个询问，直接输出预处理好的后缀最小值数组即可。

## 代码

```cpp
#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

int n, q, r, hd = 1, tl = 1;
int h[1000005], e[2000005], nx[2000005], cnt;
int s[1000005], m[1000005], ans[1000005];
int qa[1000005], f[1000005];

void add(int x, int y)
{
    cnt++;
    e[cnt] = y;
    nx[cnt] = h[x];
    h[x] = cnt;
}

int main()
{
    ios::sync_with_stdio(0);
    cin.tie(0), cout.tie(0);

    cin >> n >> q >> r, r++;
    for (int u, v, i = 1; i < n; i++)
    {
        cin >> u >> v;
        u++, v++;
        add(u, v);
        add(v, u);
    }

    qa[tl] = r;
    f[r] = 0;

    while (hd <= tl)
    {
        int u = qa[hd];
        hd++;
        for (int i = h[u]; i; i = nx[i])
        {
            if (e[i] == f[u])
                continue;
            f[e[i]] = u;
            tl++;
            qa[tl] = e[i];
        }
    }

    for (int i = 1; i <= n; i++)
    {
        s[i] = 1;
        m[i] = 0;
    }

    for (int i = n; i >= 1; i--)
    {
        int u = qa[i];
        int v = f[u];
        if (v != 0)
        {
            s[v] += s[u];
            if (s[u] > m[v])
                m[v] = s[u];
        }
    }

    for (int i = 0; i <= n; i++)
        ans[i] = n;
    for (int i = 1; i <= n; i++)
        ans[n - s[i] + m[i]] = min(ans[n - s[i] + m[i]], i - 1);
    for (int i = n - 1; i >= 0; i--)
        ans[i] = min(ans[i], ans[i + 1]);
    for (int x, i = 1; i <= q; i++)
    {
        cin >> x;
        cout << ans[x] << endl;
    }
    return 0;
}
```
