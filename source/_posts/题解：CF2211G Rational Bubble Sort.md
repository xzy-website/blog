---
abbrlink: CF2211G 题解
categories:
- - 题解
date: '2026-10-05T20:17:41.855865+08:00'
description: null
mathjax: true
tags:
- 题解
title: 题解：CF2211G Rational Bubble Sort
updated: '2026-10-05T20:17:42.571+08:00'
---
# 题解：CF2211G Rational Bubble Sort

## 思路

如果直接维护原序列 $a$ 的变化非常困难，因此我们引入前缀和序列 $S$，其中 $S_i = \sum_{j=1}^i a_j$（规定 $S_0 = 0$）。

根据题目要求，最终需要使序列 $a$ 单调不降，即满足 $a_i \le a_{i+1}$。因为 $a_i = S_i - S_{i-1}$，所以该条件可以变为：

$$
S_i - S_{i-1} \le S_{i+1} - S_i
$$

在平面直角坐标系中，这表示点集 $(i, S_i)$ 构成的折线段的斜率是单调递增的，即整个前缀和序列对应的图形必须是**下凸**的。

现在我们来看操作对前缀和序列 $S$ 的影响。当我们选择下标 $i$ 对 $a_i, a_{i+1}$ 取平均时，显然只有 $S_i$ 的值会发生改变，其余所有的 $S_j$（$j \neq i$）都保持不变。变化后的 $S_i'$ 为：

$$
S_i' = S_{i-1} + a_i' = S_{i-1} + \frac{a_i + a_{i+1}}{2} = S_{i-1} + \frac{(S_i - S_{i-1}) + (S_{i+1} - S_i)}{2} = \frac{S_{i-1} + S_{i+1}}{2}
$$

这说明，每次操作的几何本质就是将点 $(i, S_i)$ 移动到其左右两个邻居 $(i-1, S_{i-1})$ 和 $(i+1, S_{i+1})$ 连线段的中点上，也就是把这一处的折线“拉直”。

我们注意到，序列的总和 $S_n$ 和起点 $S_0 = 0$ 在整个操作过程中是固定不变的。连接 $(0,0)$ 和 $(n, S_n)$ 的线段即为我们的基准线，其方程为 $y = \frac{S_n}{n} \times x$。

## 证明

我们可以将初始点集 $(i, S_i)$ 与基准线 $y = \frac{S_n}{n} \times x$ 的相对位置关系分为以下两种情况进行讨论：

### 情况 $1$：存在至少一个点在基准线严格下方

即存在某个下标 $i$ 满足 $S_i < \frac{S_n}{n} \times i$，等价于 $S_i \times n < S_n \times i$。

证明：

由于可以通过对一段区间内的点交替进行“拉直”操作，使其在方差意义下无限逼近于两端点连成的线段。我们可以先将 $(0,0) \to (i, S_i)$ 的折线以及 $(i, S_i) \to (n, S_n)$ 的折线分别通过大量操作拉得“足够直”。

因为点 $(i, S_i)$ 在基准线下方，这两条被拉直的线段组合起来会形成一个以 $(i, S_i)$ 为底部的“V”形下凸壳，且整条折线（除端点外）全部严格位于基准线的下方。此时，我们以这个下凸壳为基准，在局部进行微调，总能在不破坏全局下凸性的前提下，消除微小的扰动。因此，只要存在一个点在基准线下方，就一定可以通过有限次操作构造出一个合法的下凸折线，此时必定有解，输出 `Yes`。

### 情况 $2$：所有点都在基准线上方或就在基准线上

即对任意的 $1 \le i \le n$，均有 $S_i \ge \frac{S_n}{n} \times i$，等价于 $S_i \times n \ge S_n \times i$。

证明：

因为最终的目标状态必须是下凸的，而两端点 $(0,0)$ 和 $(n, S_n)$ 已经在基准线上，任何整体位于基准线上方或相切的折线，如果想要保持下凸，唯一的可能就是所有的点**全部落在基准线上**（即最终 $S_i \times n = S_n \times i$ 对所有 $i$ 成立，对应原序列 $a$ 变为所有元素均相等的常数序列）。

如果某个点严格在基准线上方（$S_i \times n > S_n \times i$），我们只能依靠其左右邻居将其“拉低”：

- 若该高点的左右邻居都在基准线上，我们对其进行一次操作即可直接将其拉回基准线上。
- 若存在连续的两个或多个点都严格在基准线上方（即存在 $i$ 满足 $S_i \times n > S_n \times i$ 且 $S_{i+1} \times n > S_n \times (i+1)$），由于操作的本质是取邻居的平均值（凸组合），这组连续的高点内部无法自发产生向下的拉力，而边界上的点即便受到基准线上邻居的拉动，也无法在有限步内将整个连续段的所有点全部带回基准线上。

因此，在所有点均大于等于基准线的前提下，若存在连续两个点严格在基准线上方，则必然无解，输出 `No`；否则可以通过相互独立的拉直操作将零星的高点消去，输出 `Yes`。

## 代码

[https://codeforces.com/contest/2211/submission/377446616](https://codeforces.com/contest/2211/submission/377446616)。

```cpp
#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

long long T, n;
long long a[1000005];
long long s[1000005];
long long b[1000005];

void mian()
{
    cin >> n;
    for (long long i = 1; i <= n; i++)
    {
        cin >> a[i];
        s[i] = s[i - 1] + a[i];
    }
    for (long long i = 1; i <= n; i++)
    {
        if (s[i] * n < s[n] * i)
            return cout << "Yes" << endl, void();
        if (s[i] * n == s[n] * i)
            b[i] = 1;
        else
            b[i] = 0;
    }
    for (long long i = 1; i < n; i++)
    {
        if (b[i] == 0 && b[i + 1] == 0)
            return cout << "No" << endl, void();
    }
    cout << "Yes" << endl;
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
