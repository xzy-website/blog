---
abbrlink: P15894 题解
categories: []
date: '2026-10-05T20:00:01.913422+08:00'
description: null
mathjax: true
tags: []
title: 题解：P15894 [TOPC 2025] Twin Guardians
updated: '2026-10-05T20:00:02.561+08:00'
---
# 题解：P15894 \[TOPC 2025] Twin Guardians

判断素数时请记得**特判 $\bm{1}$**。

## 思路

题意：$T$ 组数据，每组给定两个整数 $a, b$，若 $b - a$ 为 $2$，并且两个数都是素数则输出 `Y`，否则输出 `N`。

根据题意模拟即可。

读入 $T$ 后循环 $T$ 次，读入 $a$ 和 $b$，接下来判断 $b - a$ 是否为 $2$，并且两者是否为素数。

对于素数的定义：该数的因数（两个数相乘可以得到另外一个数，则这两个数都是另外这个数的因数）除了 $1$ 和自己以外，没有其他因数则为素数。

如何判断因数呢？考虑循环检查每一个数（$i$）是否为这个数（$x$）的因数（仅需循环到 $x - 1$，$x$ 为 $x$ 的因数）。对于是否是因数，可以检查 $x$ 对 $i$ 取余是否为 $0$，只要为 $0$ 意味着 $x$ 能整除 $i$，即 $i$ 是 $x$ 的因数，那么这个数就不是素数，可以直接返回假。对于循环后都没有找到符合 $x \bmod i$ 的 $i$，可以直接返回真，即这个数是素数。在 C++ 中，取余可以使用 `%` 符号，即 `x % i == 0`。

对于一些特殊的情况：$1$ 不是素数；循环从 $2$ 开始，因为 $1$ 为每一个数的因数。

到这里其实已经可以结束了，但这里有一个简单的优化，循环条件可以从 $i < n$ 改为 $i \times i \le n$，对于证明如下：

:::info[证明]
我们假设 $x$ 不是素数，那么则有 $x = a \times b$，且 $1 < a \le b < x$。

由此可得 $a^2 \le a \times b \le x$，即 $a \le \sqrt{x}$。

因此 $x$ 必有一个小于等于 $\sqrt{x}$ 的因数。

所以只需检查 $2$ 到 $\sqrt{x}$ 之间的整数即可判断 $x$ 是否为素数。
:::

## 代码

```cpp
#include<bits/stdc++.h>
#define endl '\n'
#define int long long
using namespace std;
int T, a, b;
bool check(int x){ // 判断素数
    if(x == 1) // 记得特判 1
        return false;
    for(int i = 2;i * i <= x;i++){ // i * i <= x 等价于 i <= sqrt(n)，对于为什么只需要枚举到 i * i 请见上文证明。
        if(x % i == 0) // 如果有因数，则不是素数
            return false;
    }
    return true; // 以上情况都不是则是素数
}
signed main(){
    cin >> T; // 多组数据
    while(T--){
        cin >> a >> b; // 读入 a 和 b
        if(b - a == 2 && check(a) && check(b)) // b - 2 为 2 并且两个数均为 素数
            cout << "Y" << endl; // 输出 Y
        else
            cout << "N" << endl; // 否则输出 N
    }
    return 0;
}
```
