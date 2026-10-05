---
abbrlink: CF2048H 题解
categories:
- - 题解
date: '2026-10-05T20:05:56.497690+08:00'
description: null
mathjax: true
tags:
- 题解
title: 题解：CF2048H Kevin and Strange Operation
updated: '2026-10-05T20:05:57.346+08:00'
---
# 题解：CF2048H Kevin and Strange Operation

## 题意

给定一个二进制串 $s$，可以进行任意次操作：每次选择当前串的一个位置 $p$，先对 $i<p$ 的位置同时令 $t_i = \max(t_i, t_{i+1})$，再删除 $t_p$。问能得到多少种不同的非空二进制串，答案对 $998244353$ 取模。

## 思路

先理解操作会留下什么。最终串的每个字符都对应原串中某一段的最大值。设最终串长度为 $m$，第 $i$ 个字符对应原串的区间 $[l_i, r_i]$，值就是那段的最大值。

观察一次操作的影响，对于 $j < p$，新区间变为 $[l_j, r_{j+1}]$（右端点向右扩展一位），同时删掉第 $p$ 个区间。换句话说，每次操作会删掉右端点序列的第一个元素 $r_1$，并且删掉左端点序列的第 $p$ 个元素 $l_p$。初始时 $l_i = r_i = i$，经过 $k$ 次操作后剩下 $n-k$ 个区间，右端点序列固定为 $k+1 \sim n$（因为每次删最左边的右端点），左端点序列则可以是 $1 \sim n$ 中任意一个长度为 $n-k$ 的递增子序列（因为每次任意删一个左端点）。

把原串反转一下，记反转后的串仍为 $s_{1\dots n}$。此时在最终串中，左端点固定为 $1 \sim m$（顺序不变），而右端点可以是原串下标的一个递增子序列。于是问题变为：有多少个不同的字符串 $b$，使得存在递增下标序列 $r_1 < r_2 < \dots < r_m$，满足 $b_i = \max\{s_{r_{i-1}+1},\dots,s_{r_i}\}$（其中 $r_0 = 0$），且 $b$ 非空。

如何判断一个目标串 $b$ 是否合法？贪心地从左到右构造，每次为 $b_i$ 选择最小的可行 $r_i$，这样能留下最多的后续空间。设上一个右端点是 $j$，要匹配 $b_i$：若 $b_i = 0$，则区间 $[j+1, r_i]$ 中不能有 $1$，所以 $r_i$ 必须是 $j$ 之后第一个 $1$ 的前一个位置（若后面没有 $1$ 则取到 $n$）。若 $b_i = 1$，区间里至少有一个 $1$ 即可，最小可行 $r_i$ 就是 $j$ 之后第一个 $1$ 的位置。可见构造过程完全由原串中 $1$ 的位置唯一确定，这启发我们用 DP 计数所有可能的 $b$。

设已经构造了前 $len$ 个字符，最后一个字符的右端点是 $j$（即区间 $[prev+1, j]$，$prev$ 是上一个右端点）。用 $\text{dp}_j$ 表示这种状态的方案数。初始空串对应 $j = 0$，$\text{dp} = 1$。从左到右扫描反转后的原串，考虑把当前位置 $i$ 作为新右端点（即构造下一个字符）。新字符的取值只能是 $s_i$，因为区间 $[prev+1, i]$ 的最大值就是 $s_i$（前提是 $prev$ 合适）。转移时，若 $s_i = 1$，那么任意 $j < i$ 都合法（因为 $i$ 本身是 $1$），$\text{dp}_i \gets \sum_{j=0}^{i-1} \text{dp}_j$。若 $s_i = 0$，区间里不能有 $1$，所以 $j$ 必须大于等于 $i$ 之前最近的一个 $1$ 的位置，记 $\text{pre}_i$ 为 $i$ 之前最后一个 $1$ 的位置（不存在则为 $0$），则只有 $j \ge \text{pre}_i$ 才合法，$\text{dp}_i \gets \sum_{j = \text{pre}_i}^{i-1} \text{dp}_j$。

也可以不把 $i$ 作为新右端点，即跳过当前字符继续往后看。这相当于所有状态整体右移一位（因为后续区间起点要 $+1$）。我们通过维护一个全局偏移量来统一处理，扫描过程实际上在不断消耗原串的第一个字符，每处理完一个位置，有效部分就变成了 $s_{i+1 \dots n}$，所有状态的右端点索引需要减去 $i$。引入全局偏移量 $d$，初始设为 $n+1$（保证索引非负）。每处理位置 $i$，$d$ 减 $1$，状态数组中的索引自动左移一位。最终我们只需关心相对于当前扫描起点的位置。

## 实现

1. 初始化时树状数组在位置 $0$ 处插入 $1$（空串），偏移 $d = n+1$。
2. 预处理 $\text{nxt}_i$，位置 $i$ 之后（含）第一个 $1$ 的位置（若没有则为 $n+1$）。
3. 从 $i = 1$ 到 $n$ 循环：
   - $d - 1$；
   - 若 $s_i = 0$ 且 $\text{nxt}_i \le n$（后面有 $1$），则计算当前 $\text{dp}$ 值在区间 $[i, \text{nxt}_i-1]$ 上的和，将这个和加到位置 $\text{nxt}_i$ 上（因为新字符必须为 $1$，且右端点必须到达第一个 $1$）；
   - 然后把当前所有 $\text{dp}$ 值的和（即树状数组的全区间和）累加到答案中。
4. 最终答案就是所有扫描过程中产生的状态数之和，每个状态对应一个合法最终串。

## 代码

[https://codeforces.com/contest/2048/submission/373194628](https://codeforces.com/contest/2048/submission/373194628)

```cpp
#include <bits/stdc++.h>
#define endl '\n'
#define MOD 998244353
using namespace std;

struct BIT
{
    int d, limit, tr[2000005];

    void init(int n)
    {
        d = n + 1;
        limit = 2 * n + 5;
        fill(tr, tr + limit + 1, 0);
    }

    int lowbit(int x)
    {
        return x & (-x);
    }

    void update(int x, int k)
    {
        x += d;
        while (x <= limit)
            tr[x] = (tr[x] + k) % MOD, x += lowbit(x);
    }

    int query(int x)
    {
        int res = 0;
        x += d;
        while (x)
            res = (res + tr[x]) % MOD, x -= lowbit(x);
        return res;
    }
} bit;

int T, n, ans;
string s;
int nxt[1000005];

void mian()
{
    cin >> s;
    n = s.size();
    reverse(s.begin(), s.end());
    s = " " + s;
    bit.init(n);
    nxt[n + 1] = n + 1;
    for (int i = n; i >= 1; --i)
        nxt[i] = (s[i] == '1') ? i : nxt[i + 1];
    bit.update(0, 1);
    ans = 0;
    for (int i = 1; i <= n; ++i)
    {
        --bit.d;
        if (s[i] == '0' && nxt[i] <= n)
            bit.update(nxt[i], (bit.query(nxt[i] - 1) - bit.query(i - 1) + MOD) % MOD);
        ans = (ans + bit.query(n)) % MOD;
    }
    cout << ans << endl;
}

int main()
{
    ios::sync_with_stdio(0);
    cin.tie(0), cout.tie(0);
    cin >> T;
    while (T--)
        mian();
    return 0;
}

```
