---
abbrlink: P16780 题解
categories:
- - 题解
date: '2026-10-05T20:01:42.041039+08:00'
description: null
mathjax: true
tags:
- 题解
title: 题解：P16780 ⌈Xzy OI R1 T2⌋ 成成边
updated: '2026-10-05T20:01:42.904+08:00'
---
# 题解：P16780 ⌈Xzy OI R1 T2⌋ 成成边

这里是出题人题解。

## 思路

我们注意到，可以转化为点对 $\mathrm{LCP}$ 之和。

设完全图 $K_n$ 的生成树个数为 $T_n$，对于一条固定的边 $e = (i, j)$，包含 $e$ 的生成树个数为 $C_e$。则所有生成树的权值和为：

$$
\mathrm{ans} = \sum_{1 \le i < j \le n} \mathrm{LCP}(s_i, s_j) \times C_{(i,j)}
$$

由 Cayley 公式，$T_n = n^{n - 2}$。对于完全图中一条特定的边，包含它的生成树个数为：

$$
C_{(i,j)} = 2 \times n^{n - 3} \quad (n \ge 2)
$$

::::info[有一点点长的证明]
:::info[方法一（Prufer 序列）]
$K_n$ 的生成树与长度为 $n - 2$ 的 Prufer 序列一一对应。要计数包含边 $(i, j)$ 的生成树，等价于计数满足以下条件的 Prufer 序列：在生成树中删除叶子时，$i$ 和 $j$ 不会在同时与其他点都不相连的情况下被删除，直到最后剩下边 $(i, j)$。更直接地，可以利用已知结论：对于完全图，包含特定边 $(i, j)$ 的生成树数为 $2 \times n^{n - 3}$（参见 J. W. Moon 的著作 *Counting Labeled Trees*）。

这里给出一个组合推导：固定边 $(i, j)$，考虑所有生成树。若一棵生成树包含 $(i, j)$，则删除该边后得到两棵子树，分别包含 $k$ 个点和 $n - k$ 个点（$1 \le k \le n - 1$）。两部分的连接方式有 $\binom{n - 2}{k - 1}$ 种选择（除 $i, j$ 外分配顶点），且两部分内部的生成树数分别为 $k^{k - 2}$ 和 $(n - k)^{n - k - 2}$。因此

$$
C_e = \sum_{k = 1}^{n - 1} \binom{n - 2}{k - 1} \times k^{k - 2} \times (n - k)^{n - k - 2}
$$

利用 Abel 恒等式或生成函数可证明该和式为 $2 \times n^{n - 3}$，不做详细说明。
:::

:::info[方法二（矩阵树定理）]
对完全图 $K_n$，拉普拉斯矩阵为 $L = nI - \mathbf{1}\mathbf{1}^T$。固定边 $(i, j)$，欲求包含该边的生成树数，可考虑从 $K_n$ 中删去该边得到的图 $G'$。设 $L'$ 为 $G'$ 的拉普拉斯矩阵，则包含边 $(i, j)$ 的生成树数等于 $K_n$ 的生成树数减去 $G'$ 的生成树数：

$$
C_e = n^{n-2} - \tau(G')
$$

其中 $\tau(G')$ 为 $G'$ 的生成树个数。由矩阵树定理可算得 $\tau(G') = (n-2)n^{n-3}$，从而

$$
C_e = n^{n-2} - (n-2) \times n^{n-3} = 2 \times n^{n-3}
$$

因此对于 $n \ge 2$，结论成立。
:::

综上，对 $n \ge 2$，有

$$
C_{(i,j)} = 2 \times n^{n-3}
$$

代入原式即得所求权值和，当然你也可以手算一些小的值进行模拟。
::::

因此，对于 $n \ge 2$：

$$
\mathrm{ans} = 2 \times n^{n-3} \times \sum_{1 \le i < j \le n} \mathrm{LCP}(s_i, s_j)
$$

那么对于 $n \le 2$ 的情况有：

- 当 $n = 1$ 时，生成树为空树，权值和为 $0$。
- 当 $n = 2$ 时，只有一条边，权值和即为 $\mathrm{LCP}(s_1,s_2)$，公式 $2 \times n^{n - 3} = 2 \times 2^{-1}$ 需模逆处理，因此需要单独特判。

此时，题意已经变为给定 $n$ 个字符串，求 $\displaystyle \sum_{i < j} \mathrm {LCP}(s_i, s_j)$。

接下来我们考虑如何计算。

考虑使用字典树（Trie）解决。将所有字符串插入 $\mathrm{Trie}$，每个节点维护：

- $\mathrm{cnt}$：经过该节点的字符串个数（即该节点对应的前缀出现在多少个字符串中）。
- $\mathrm{depth}$：根到该节点的距离（即前缀长度）。

对于任意两个字符串，它们的 LCP 长度等于它们从根出发的第一个分叉点的深度。因此，所有点对的 LCP 之和可以通过统计每个节点作为“最近公共祖先”（LCA）的贡献得到。

具体地，对于节点 $u$（深度为 $\mathrm {dep}_u$），设其子节点集合为 $\mathrm {son}(u)$。记 $\mathrm{total} = \mathrm{cnt}_u$，则所有以 $u$ 为 LCA 的字符串对数量为：

$$
\binom{\mathrm{total}}{2} - \sum_{v \in \mathrm{son}(u)} \binom{\mathrm{cnt}_v}{2}
$$

这些字符串对的 LCP 恰好为 $\mathrm {dep}_u$，因此节点 $u$ 对总和的贡献为：

$$
\left( \binom{\mathrm{total}}{2} - \sum_{v \in \mathrm{son}(u)} \binom{\mathrm{cnt}_v}{2} \right) \times \mathrm{dep}_u
$$

对所有节点求和即得 $\sum_{i < j} \mathrm {LCP}(s_i, s_j)$。

## 实现

1. 读入 $n$ 和所有字符串。
2. 特判：
   - 若 $n = 1$，输出 $0$。
   - 若 $n = 2$，输出 $\mathrm {LCP}(s_1, s_2)$（直接逐字符比较）。
3. 若 $n \ge 3$：
   - 构建 Trie，插入所有字符串，记录每个节点的 $\mathrm{cnt}$ 和 $\mathrm{depth}$。
   - 计算 $\mathrm{total}_{lcp} = \sum_{i < j} LCP (s_i, s_j)$，通过上述 Trie 方法。
   - 计算系数 $coef = 2 \times n^{n - 3} \bmod MOD$。
   - 答案 $\mathrm{ans} = \mathrm{total}_{lcp} \bmod MOD \times coef \bmod MOD$。
4. 输出 $\mathrm{ans}$。

## 代码

```cpp
#include <bits/stdc++.h>
#define endl '\n'
#define MOD 1000000007
using namespace std;

struct TrieNode
{
    int cnt;   // 经过该节点的字符串个数
    int depth; // 节点深度（前缀长度）
    TrieNode *child[26];
    TrieNode() : cnt(0), depth(0) { memset(child, 0, sizeof(child)); }
};

// 快速幂
long long qpow(long long a, long long b, long long mod)
{
    long long res = 1;
    a %= mod;
    while (b)
    {
        if (b & 1)
            res = res * a % mod;
        a = a * a % mod;
        b >>= 1;
    }
    return res;
}

// 计算组合数 C(x, 2)
long long comb(long long x)
{
    if (x < 2)
        return 0;
    return x * (x - 1) / 2;
}

int n;
string str[100005];

long long total; // 用于累加所有 LCP 贡献
void dfs(TrieNode *u)
{
    long long cnt = u->cnt; // 当前节点经过的字符串数
    long long ccomb = 0;    // 所有子节点的 C(cnt, 2) 之和
    for (int i = 0; i < 26; i++)
    {
        if (u->child[i])
        {
            dfs(u->child[i]); // 递归处理子节点
            ccomb += comb(u->child[i]->cnt);
        }
    }
    long long tmp = comb(cnt) - ccomb; // 恰好以当前节点为 LCP 的点对数
    if (tmp > 0)
        total = (total + tmp * u->depth) % MOD; // 累加贡献
}

int main()
{
    ios::sync_with_stdio(0);
    cin.tie(0), cout.tie(0);
    cin >> n;
    for (int i = 1; i <= n; i++)
        cin >> str[i];

    if (n == 1)
        return cout << 0 << endl, 0;
    if (n == 2)
    {
        // 直接计算 LCP
        int lcp = 0;
        while (lcp < str[1].size() && lcp < str[2].size() && str[1][lcp] == str[2][lcp])
            lcp++;
        return cout << lcp % MOD << endl, 0;
    }

    // 构建 Trie
    TrieNode *root = new TrieNode();
    root->depth = 0;
    for (int i = 1; i <= n; i++)
    {
        string s = str[i];
        TrieNode *cur = root;
        cur->cnt++;
        for (int j = 0; j < s.size(); j++)
        {
            int c = s[j] - 'a';
            if (!cur->child[c])
            {
                cur->child[c] = new TrieNode();
                cur->child[c]->depth = cur->depth + 1;
            }
            cur = cur->child[c];
            cur->cnt++;
        }
    }

    dfs(root), total %= MOD;
    long long coef = 2 * qpow(n, n - 3, MOD) % MOD;
    long long ans = total * coef % MOD;
    return cout << ans << endl, 0;
}
```
