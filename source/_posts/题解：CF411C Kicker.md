---
abbrlink: CF411C 题解
categories:
- - 题解
date: '2025-04-15T20:24:08.588581+08:00'
description: null
mathjax: true
tags:
- 题解
title: 题解：CF411C Kicker
updated: '2025-04-15T20:24:09.829+08:00'
---
# 题解：CF411C Kicker

## 思路

队伍一先安排，那么队伍二想要获胜一定安排能踢过队伍一的球员。

先看队伍一，怎么保证队伍一必胜呢？只要队伍一的攻击球员~~至高无上~~特别厉害，攻击力要比队伍二任意球员的防守力都要大，那么无论队伍二怎么安排防守都踢不过。同样的，只要队伍一的防守球员~~至高无上~~特别厉害，防守力要比队伍二任意球员的攻击力都要大，那么无论队伍二怎么安排攻击都踢不过。队伍二亦然。

结论：只要一个人的攻击力大于对方二人的防守力且另一个人的防守力大于对方二人的攻击力则该队伍获胜，反之亦然。如果两队都没有杰出的球员能同时踢败对方的两位球员，那么就没有保证胜利的安排方案。

当然，队伍二不能套用队伍一的代码，因为队伍二是根据队伍一进行选择的，而以队伍二为基准进行判断时我们并不知道队伍一的安排，所以要把队伍一每一种安排都列举出来。

## 代码

```cpp
#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
int a[2], b[2], c[2], d[2];
int main()
{
    cin >> afs >> agj >> bfs >> bgj >> cfs >> cgj >> dfs >> dgj;
    if (
        (afs > max(cgj, dgj) && bgj > max(cfs, dgj)) ||
        (bfs > max(cgj, dgj) && agj > max(cfs, dgj)))
        cout << "Team 1" << endl;
    else if (
        (cgj > afs && dfs > bgj || dgj > afs && cfs > bgj) &&
        (cgj > bfs && dfs > agj || dgj > bfs && cfs > agj))
        cout << "Team 2" << endl;
    else
        cout << "Draw" << endl;
    return 0;
}
```
