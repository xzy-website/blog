---
abbrlink: 闲话
categories:
- - 闲话
date: '2025-04-15T20:45:34.500730+08:00'
description: null
mathjax: true
tags:
- 转载
- 闲话
title: 【转载于 qwqerty】一种基于积性性质快速计算 lowbit 的方法
updated: '2025-04-15T20:45:35.731+08:00'
---
# 本文转载于[https://www.luogu.com.cn/article/mgu1aigs](https://www.luogu.com.cn/article/mgu1aigs)。

可惜休闲娱乐分区不能全站推荐（
我们不难打出一下暴力代码：

```cpp
int lowbit(int x) {
	int res = 0;
	while (!(x & 1)) {
		res++;
		x >>= 1;
	}
	return (1 << res);
} 
```

容易证明，$\operatorname{lowbit}(x)$ 是积性函数。看到积性函数，我们首先联想到分解质因数，所以我们可以将 $x$ 分解质因数，计算其质因数之积。
接下来我们考虑质数幂的情况，很显然，除了 $\operatorname{lowbit}(2^k)=2^k$ 之外，其它都是 $0$。所以我们只需要分解质因数，套公式计算即可。代码如下：

```cpp
int qpow(int x, int y) {
	int res = 0;
	while (y) {
		if (y & 1) res *= x;
		x *= x;
		y >>= 1;
	}
	return res;
}
int lowbit(int x) {
	int res = 1;
	for (int i = 2; i <= x / i; i++) {
		int cnt = 0;
		while (x % i == 0) {
			x /= i;
			cnt++;
		}
		if (i == 2) res *= qpow(2, cnt);
	}
	if (x != 1) {
		if (x == 2) {
			res *= 2;
		}
	}
	return res;
} 
```

考虑优化，只需统计 $=2$ 的质因数即可，代码可以优化成这样：

```cpp
int qpow(int x, int y) {
	int res = 0;
	while (y) {
		if (y & 1) res *= x;
		x *= x;
		y >>= 1;
	}
	return res;
}
int lowbit(int x) {
	int cnt = 0;
	while (x % 2 == 0) {
		x /= 2;
		cnt++;
	}
	return qpow(2, cnt);
} 
```

最后再使用位运算优化一下常数，代码就会变成这样：

```cpp
int lowbit(int x) {
	int res = 0;
	while (!(x & 1)) {
		res++;
		x >>= 1;
	}
	return (1 << res);
} 
```

这样，我们就将一个 $O(\log n)$ 的代码优化成了 $O(\log n)$，优化效果非常明显。
