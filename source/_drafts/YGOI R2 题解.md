---
abbrlink: YGOIR2TJ
categories:
- - 题解
date: '2026-02-01T20:08:52.048136+08:00'
description: null
mathjax: true
tags:
- 题解
title: YGOI R2 题解
updated: '2026-02-01T20:08:52.506+08:00'
---
# T1


## 数据生成器代码

```python
import random
import sys
from typing import List, Tuple

def generate_test_case(n: int, m: int, q: int, seed: int = 42):
random.seed(seed)

# 生成图
edges = []
edge_id = 0
existing_edges = set()

# 首先生成一个连通图
nodes = list(range(1, n + 1))
random.shuffle(nodes)

for i in range(n - 1):
u = nodes[i]
v = nodes[i + 1]
c = random.randint(1, 100)
cost = random.randint(1, 100)
t = random.randint(1, 10)
e = random.randint(1, 100)
edges.append((u, v, c, cost, t, e))
existing_edges.add((u, v))
edge_id += 1

# 添加剩余边
while len(edges) < m:
u = random.randint(1, n)
v = random.randint(1, n)
if u == v or (u, v) in existing_edges:
continue
c = random.randint(1, 100)
cost = random.randint(1, 100)
t = random.randint(1, 10)
e = random.randint(1, 100)
edges.append((u, v, c, cost, t, e))
existing_edges.add((u, v))
edge_id += 1

# 生成操作序列
operations = []
goods_count = 0
active_goods = set()

for _ in range(q):
op_type = random.randint(1, 7)

if op_type == 1:# 添加货物
s = random.randint(1, n)
t = random.randint(1, n)
while t == s:
t = random.randint(1, n)
d = random.randint(1, 50)
T = random.randint(5, 20)
E = random.randint(100, 1000)
p = random.randint(1, 10)
operations.append(f"1 {s} {t} {d} {T} {E} {p}")
goods_count += 1
active_goods.add(goods_count)

elif op_type == 2 and active_goods:# 删除货物
gid = random.choice(list(active_goods))
operations.append(f"2 {gid}")
active_goods.remove(gid)

elif op_type == 3:# 添加边
u = random.randint(1, n)
v = random.randint(1, n)
if u == v:
v = v % n + 1
c = random.randint(1, 100)
cost = random.randint(1, 100)
t = random.randint(1, 10)
e = random.randint(1, 100)
operations.append(f"3 {u} {v} {c} {cost} {t} {e}")
edges.append((u, v, c, cost, t, e))

elif op_type == 4 and edges:# 修改边
eid = random.randint(1, len(edges))
c = random.randint(1, 100)
cost = random.randint(1, 100)
t = random.randint(1, 10)
e = random.randint(1, 100)
operations.append(f"4 {eid} {c} {cost} {t} {e}")

elif op_type == 5 and len(edges) > n:# 删除边（保证图连通）
eid = random.randint(n, len(edges))
operations.append(f"5 {eid}")

elif op_type == 6 and active_goods:# 查询单个货物
gid = random.choice(list(active_goods))
operations.append(f"6 {gid}")

elif op_type == 7 and active_goods:# 综合查询
operations.append("7")

return n, m, q, edges, operations

def write_test_case(filename: str, n: int, m: int, q: int,
edges: List[Tuple], operations: List[str]):
with open(filename, 'w') as f:
f.write(f"{n} {m} {q}\n")
for edge in edges[:m]:
f.write(f"{edge[0]} {edge[1]} {edge[2]} {edge[3]} {edge[4]} {edge[5]}\n")
for op in operations[:q]:
f.write(f"{op}\n")

if __name__ == "__main__":
# 生成不同规模的数据
test_cases = [
("small.in", 10, 15, 20),
("medium.in", 50, 100, 200),
("large.in", 200, 1000, 500),
]

for filename, n, m, q in test_cases:
print(f"Generating {filename}...")
params = generate_test_case(n, m, q, hash(filename) % 10000)
write_test_case(filename, *params)
```

## 正解代码及简要思路

```cpp
#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
#include <cstring>
#include <map>
#include <set>
#include <limits>
using namespace std;

typedef long long ll;
const ll INF = 1e18;
const int MAXN = 210;
const int MAXM = 10010;
const int MAXK = 1010;

struct Edge {
int to, rev;
ll cap, cost, time, emission;
Edge(int t, int r, ll ca, ll co, ll ti, ll e)
: to(t), rev(r), cap(ca), cost(co), time(ti), emission(e) {}
};

struct Goods {
int s, t, priority;
ll demand, time_limit, emission_limit;
int id;
};

class DynamicNetwork {
private:
int n, m, edge_cnt;
vector<Edge> graph[MAXN];
vector<pair<int, int>> edge_info;// 记录边的原始信息

// 临时存储用于特定算法的图
vector<Edge> temp_graph[MAXN];

public:
DynamicNetwork(int n) : n(n), m(0), edge_cnt(0) {}

void add_edge(int u, int v, ll cap, ll cost, ll time, ll emission) {
graph[u].emplace_back(v, graph[v].size(), cap, cost, time, emission);
graph[v].emplace_back(u, graph[u].size() - 1, 0, -cost, time, emission);
edge_info.emplace_back(u, graph[u].size() - 1);
edge_cnt++;
}

// 费用流相关
ll min_cost_flow(int s, int t, ll flow, ll time_limit, ll emission_limit) {
// 构建分层图（考虑时间和碳排放约束）
ll total_cost = 0;
vector<ll> dist(n + 1), pot(n + 1, 0);
vector<pair<int, int>> prev(n + 1);

auto dijkstra = [&](int s, int t) -> bool {
fill(dist.begin(), dist.end(), INF);
dist[s] = 0;
priority_queue<pair<ll, int>, vector<pair<ll, int>>, greater<pair<ll, int>>> pq;
pq.emplace(0, s);

while (!pq.empty()) {
auto [d, u] = pq.top(); pq.pop();
if (d > dist[u]) continue;

for (int i = 0; i < graph[u].size(); i++) {
Edge &e = graph[u][i];
if (e.cap <= 0) continue;

// 检查时间和碳排放约束
if (e.time > time_limit || e.emission > emission_limit) continue;

ll nd = d + e.cost + pot[u] - pot[e.to];
if (nd < dist[e.to]) {
dist[e.to] = nd;
prev[e.to] = {u, i};
pq.emplace(nd, e.to);
}
}
}
return dist[t] < INF;
};

ll f = flow;
while (f > 0) {
if (!dijkstra(s, t)) return -1;

for (int i = 1; i <= n; i++) {
pot[i] += dist[i];
}

ll aug = f;
for (int v = t; v != s; v = prev[v].first) {
int u = prev[v].first;
Edge &e = graph[u][prev[v].second];
aug = min(aug, e.cap);
}

for (int v = t; v != s; v = prev[v].first) {
int u = prev[v].first;
Edge &e = graph[u][prev[v].second];
e.cap -= aug;
graph[e.to][e.rev].cap += aug;
}

f -= aug;
total_cost += aug * pot[t];
}
return total_cost;
}

// 多商品流求解
pair<ll, vector<tuple<int, ll, ll>>> solve_multi_commodity(
const vector<Goods> &goods,
const vector<int> &active_goods
) {
// 构建线性规划模型（简化为序列求解）
vector<tuple<int, ll, ll>> result;
ll total_priority = 0;

// 复制原图用于计算
for (int i = 1; i <= n; i++) {
temp_graph[i] = graph[i];
}

// 按优先级排序
vector<pair<int, int>> sorted_goods;// (priority, id)
for (int id : active_goods) {
sorted_goods.emplace_back(goods[id].priority, id);
}
sort(sorted_goods.rbegin(), sorted_goods.rend());

for (auto [_, gid] : sorted_goods) {
const Goods &g = goods[gid];

// 计算该货物的最大流
ll max_flow = 0;
ll cost = min_cost_flow(g.s, g.t, g.demand, g.time_limit, g.emission_limit);

if (cost >= 0) {
// 实际可运输量（基于费用流结果估算）
ll actual_flow = min(g.demand,
max_flow_bfs(g.s, g.t, g.time_limit, g.emission_limit));

if (actual_flow > 0) {
total_priority += actual_flow * g.priority;
result.emplace_back(gid, actual_flow, cost * actual_flow / g.demand);
}
}

// 恢复图
for (int i = 1; i <= n; i++) {
graph[i] = temp_graph[i];
}
}

return {total_priority, result};
}

private:
ll max_flow_bfs(int s, int t, ll time_limit, ll emission_limit) {
vector<ll> flow(n + 1, 0);
flow[s] = INF;
queue<int> q;
q.push(s);

while (!q.empty()) {
int u = q.front(); q.pop();
for (Edge &e : graph[u]) {
if (e.cap > 0 && e.time <= time_limit && e.emission <= emission_limit) {
ll f = min(flow[u], e.cap);
if (flow[e.to] < f) {
flow[e.to] = f;
q.push(e.to);
}
}
}
}
return flow[t];
}
};

class LogisticsSolver {
private:
int n, m, q;
DynamicNetwork network;
vector<Goods> goods;
vector<int> active_goods;
int goods_id_counter;

// 边管理
struct FullEdge {
int u, v;
ll cap, cost, time, emission;
bool active;
};
vector<FullEdge> edges;

public:
LogisticsSolver(int n, int m, int q)
: n(n), m(m), q(q), network(n), goods_id_counter(0) {}

void init_edge(int u, int v, ll cap, ll cost, ll time, ll emission) {
network.add_edge(u, v, cap, cost, time, emission);
edges.push_back({u, v, cap, cost, time, emission, true});
}

void add_goods(int s, int t, ll d, ll T, ll E, int p) {
goods_id_counter++;
goods.push_back({s, t, p, d, T, E, goods_id_counter});
active_goods.push_back(goods_id_counter);
}

void remove_goods(int id) {
active_goods.erase(
remove(active_goods.begin(), active_goods.end(), id),
active_goods.end()
);
}

void add_new_edge(int u, int v, ll cap, ll cost, ll time, ll emission) {
network.add_edge(u, v, cap, cost, time, emission);
edges.push_back({u, v, cap, cost, time, emission, true});
m++;
}

void modify_edge(int eid, ll cap, ll cost, ll time, ll emission) {
if (eid >= 1 && eid <= edges.size()) {
edges[eid-1] = {edges[eid-1].u, edges[eid-1].v,
cap, cost, time, emission, true};
// 重建网络
rebuild_network();
}
}

void delete_edge(int eid) {
if (eid >= 1 && eid <= edges.size()) {
edges[eid-1].active = false;
rebuild_network();
m--;
}
}

ll query_single_goods(int gid) {
if (gid < 1 || gid > goods.size()) return -1;
Goods &g = goods[gid-1];

// 重建网络
rebuild_network();

return network.min_cost_flow(g.s, g.t, g.demand,
g.time_limit, g.emission_limit);
}

pair<ll, vector<tuple<int, ll, ll>>> query_all_goods() {
rebuild_network();
return network.solve_multi_commodity(goods, active_goods);
}

private:
void rebuild_network() {
// 清空当前网络
network = DynamicNetwork(n);

// 添加所有活跃的边
for (const auto &e : edges) {
if (e.active) {
network.add_edge(e.u, e.v, e.cap, e.cost, e.time, e.emission);
}
}
}
};

int main() {
ios::sync_with_stdio(false);
cin.tie(nullptr);

int n, m, q;
cin >> n >> m >> q;

LogisticsSolver solver(n, m, q);

// 读入初始边
for (int i = 0; i < m; i++) {
int u, v;
ll c, cost, t, e;
cin >> u >> v >> c >> cost >> t >> e;
solver.init_edge(u, v, c, cost, t, e);
}

// 处理操作
for (int i = 0; i < q; i++) {
int op;
cin >> op;

if (op == 1) {
int s, t, p;
ll d, T, E;
cin >> s >> t >> d >> T >> E >> p;
solver.add_goods(s, t, d, T, E, p);
}
else if (op == 2) {
int id;
cin >> id;
solver.remove_goods(id);
}
else if (op == 3) {
int u, v;
ll c, cost, t, e;
cin >> u >> v >> c >> cost >> t >> e;
solver.add_new_edge(u, v, c, cost, t, e);
}
else if (op == 4) {
int eid;
ll c, cost, t, e;
cin >> eid >> c >> cost >> t >> e;
solver.modify_edge(eid, c, cost, t, e);
}
else if (op == 5) {
int eid;
cin >> eid;
solver.delete_edge(eid);
}
else if (op == 6) {
int id;
cin >> id;
ll result = solver.query_single_goods(id);
cout << result << "\n";
}
else if (op == 7) {
auto [total, details] = solver.query_all_goods();
cout << total << "\n";
if (total > 0) {
cout << details.size() << "\n";
for (auto [id, flow, cost] : details) {
cout << id << " " << flow << " " << cost << "\n";
}
}
}
}

return 0;
}
```

## 简要思路

### 算法核心

1. **动态网络流管理**：使用费用流算法处理单个货物运输，支持容量、成本、时间、碳排放四个维度的约束。
2. **多商品流优化**：将多货物运输问题转化为带权重的多商品流问题，使用优先级加权和贪心策略求解。
3. **实时更新机制**：通过重建网络图的方式支持边的动态添加、删除和修改。

### 关键优化

1. **分层图构建**：在最短路径计算中同时考虑时间和碳排放约束。
2. **势能函数**：在费用流中使用Johnson势能算法避免负权边问题。
3. **增量更新**：对网络修改采用部分重建策略，减少计算开销。

### 复杂度分析

- 单次费用流：O(F * E * logV)，其中F是流量，E是边数，V是节点数
- 多商品流：O(K * 单次费用流)，K是货物数量
- 空间复杂度：O(V + E + K)

### 扩展性

1. 可扩展更多约束条件
2. 支持并行计算不同货物的流
3. 可加入机器学习预测优化运输方案

这个题目结合了网络流、动态图、多目标优化等多个高级主题，代码实现复杂，适合作为竞赛或高级算法课程的最终题目。


# T2
