---
abbrlink: 洛谷 P7063 题解
categories:
- - 题解
date: '2026-01-24T22:25:04.700399+08:00'
description: null
mathjax: true
tags:
- 题解
title: 题解：P7063 [NWRRC 2014] Digits
updated: '2026-01-24T22:25:06.380+08:00'
---
# 题解：P7063 \[NWRRC 2014] Digits

如果你样例过了但答案错了，记得使用 `long long` 哦！

## 思路

题目让我们找出 $n$ 个数，并且这 $n$ 个数的各个位上的数字之和要最小，求出这个和。

对于样例 $1$，可以为 $1$ 和 $10$，和为 $11$。

那么考虑暴力枚举 $i$（$i$ 的枚举范围要尽可能大），对于当前的 $i$，我们将它的数位和定义为 $t$：

- 我们将存放数位和为 $t$ 的和增加 $i$，用来存放各种搭配方案的答案。
- 我们将存放数位和为 $t$ 的个数增加 $1$，用来判断这种搭配方案的个数是不是 $n$ 了，如果是那么就对这种搭配方案的结果取最小值。

最后输出最小值即可。

## 代码

```cpp
#include<bits/stdc++.h>
#define endl '\n'
using namespace std;
long long n, t, ans = INT_MAX, cnt[5005], sum[5005];
string s;
int main(){
    cin >> n;
    for(long long i = 1;i <= 1000000;i++){
        s = to_string(i); // 将 i 转成字符串
        t = 0; // 数位和清零
        for(long long j = 0;j < s.size();j++) // 枚举每一位
            t += s[j] - '0'; // 加上这个数位上的数
        sum[t] += i; // 我们将存放数位和为 t 的和增加 i，用来存放各种搭配方案的答案
        cnt[t]++; // 我们将存放数位和为 t 的个数增加 1，用来判断这种搭配方案的个数是不是 n 了
        if(cnt[t] == n) // 如果是
            ans = min(ans, sum[t]); // 那么就对这种搭配方案的结果取最小值
    }
    cout << ans << endl; // 最后输出最小值即可
    return 0;
}
```
