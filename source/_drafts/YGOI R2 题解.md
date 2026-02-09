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
updated: '2026-02-09T19:13:18.378+08:00'
---
# T1

暴力枚举所有区间是 $O(n^2)$，会超时。正解：考虑每个元素作为最大值和最小值对答案的贡献。对于每个 $a_i$，计算它作为最大值的区间个数 $cnt\_max[i]$ 和作为最小值的区间个数 $cnt\_min[i]$。答案 = $\sum a_i \times (cnt\_max[i] - cnt\_min[i])$。使用单调栈可以在 $O(n)$ 时间内求出每个元素的支配区间范围。

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
const int MOD = 1e9 + 7;
const int N = 2e5 + 5;
int n;
ll a[N];
int left_max[N], right_max[N];
int left_min[N], right_min[N];
void solve_max()
{
    stack<int> st;
    for (int i = 1; i <= n; i++)
    {
        while (!st.empty() && a[st.top()] <= a[i])
        {
            st.pop();
        }
        left_max[i] = st.empty() ? 1 : (st.top() + 1);
        st.push(i);
    }
    while (!st.empty())
        st.pop();
    for (int i = n; i >= 1; i--)
    {
        while (!st.empty() && a[st.top()] < a[i])
        {
            st.pop();
        }
        right_max[i] = st.empty() ? n : (st.top() - 1);
        st.push(i);
    }
}
void solve_min()
{
    stack<int> st;
    for (int i = 1; i <= n; i++)
    {
        while (!st.empty() && a[st.top()] >= a[i])
        {
            st.pop();
        }
        left_min[i] = st.empty() ? 1 : (st.top() + 1);
        st.push(i);
    }
    while (!st.empty())
        st.pop();
    for (int i = n; i >= 1; i--)
    {
        while (!st.empty() && a[st.top()] > a[i])
        {
            st.pop();
        }
        right_min[i] = st.empty() ? n : (st.top() - 1);
        st.push(i);
    }
}
int main()
{
    ios::sync_with_stdio(false);
    cin.tie(0);
    cin >> n;
    for (int i = 1; i <= n; i++)
        cin >> a[i];
    solve_max();
    solve_min();
    ll ans = 0;
    for (int i = 1; i <= n; i++)
    {
        ll cnt_max = (ll)(i - left_max[i] + 1) * (right_max[i] - i + 1);
        ll cnt_min = (ll)(i - left_min[i] + 1) * (right_min[i] - i + 1);
        ll contribution = (cnt_max - cnt_min) % MOD * (a[i] % MOD) % MOD;
        ans = (ans + contribution) % MOD;
    }
    ans = (ans + MOD) % MOD;
    cout << ans << endl;
    return 0;
}
```

# T2

直接模拟所有操作，需要注意：

1. 使用优先队列维护可执行进程（按最终优先级排序）
2. 使用并查集维护进程组，记录每个组的额外优先级偏移
3. 合并时更新所有受影响的进程在优先队列中的位置

由于 $m \le 5000$，暴力更新可以接受。

代码：

```cpp
#include <iostream>
#include <unordered_map>
#include <set>
#include <string>
#include <algorithm>
using namespace std;

// 比较器：用于每个组内的进程集合，按原始优先级降序，相同则 pid 升序
struct ComparePair {
    bool operator()(const pair<int, int>& a, const pair<int, int>& b) const {
        if (a.first != b.first) return a.first > b.first;
        return a.second < b.second;
    }
};

// 全局候选结构，按最终优先级降序，相同则 pid 升序
struct GlobalCandidate {
    int final_priority;
    int pid;
    bool operator<(const GlobalCandidate& other) const {
        if (final_priority != other.final_priority) return final_priority > other.final_priority;
        return pid < other.pid;
    }
};

unordered_map<int, int> parent;       // 并查集父节点
unordered_map<int, int> delta;        // 组优先级偏移量
unordered_map<int, set<pair<int, int>, ComparePair>> group_members; // 每个组的进程集合
set<GlobalCandidate> global_set;      // 全局候选集合
unordered_map<int, int> proc_priority;// 进程原始优先级

int find(int x) {
    if (parent[x] != x) parent[x] = find(parent[x]);
    return parent[x];
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int m;
    cin >> m;
    string op;
    while (m--) {
        cin >> op;
        if (op == "CREATE") {
            int pid, priority;
            cin >> pid >> priority;
            parent[pid] = pid;
            proc_priority[pid] = priority;
            delta[pid] = 0;
            group_members[pid].insert({priority, pid});
            global_set.insert({priority + delta[pid], pid});
        }
        else if (op == "RUN") {
            auto it = global_set.begin();
            int pid = it->pid;
            int final_priority = it->final_priority;
            global_set.erase(it);

            int gid = find(pid);
            int p = proc_priority[pid];
            auto& mem = group_members[gid];
            mem.erase({p, pid});
            if (!mem.empty()) {
                auto it_mem = mem.begin();
                int new_top_p = it_mem->first;
                int new_top_pid = it_mem->second;
                int new_final = new_top_p + delta[gid];
                global_set.insert({new_final, new_top_pid});
            }
            proc_priority.erase(pid);
            cout << pid << '\n';
        }
        else if (op == "UP") {
            int pid, x;
            cin >> pid >> x;
            int gid = find(pid);
            int old_p = proc_priority[pid];
            auto& mem = group_members[gid];
            auto it_mem = mem.begin();
            int old_top_p = it_mem->first;
            int old_top_pid = it_mem->second;
            int old_final = old_top_p + delta[gid];
            global_set.erase({old_final, old_top_pid});

            mem.erase({old_p, pid});
            int new_p = old_p + x;
            proc_priority[pid] = new_p;
            mem.insert({new_p, pid});

            it_mem = mem.begin();
            int new_top_p = it_mem->first;
            int new_top_pid = it_mem->second;
            int new_final = new_top_p + delta[gid];
            global_set.insert({new_final, new_top_pid});
        }
        else if (op == "MERGE") {
            int pid1, pid2;
            cin >> pid1 >> pid2;
            int g1 = find(pid1);
            int g2 = find(pid2);
            if (g1 == g2) continue;

            // 启发式合并：保证 g1 的集合更大
            if (group_members[g1].size() < group_members[g2].size()) swap(g1, g2);

            auto& mem1 = group_members[g1];
            auto& mem2 = group_members[g2];

            // 删除两个组的旧候选
            auto it1 = mem1.begin();
            int top1_p = it1->first;
            int top1_pid = it1->second;
            int final1 = top1_p + delta[g1];
            global_set.erase({final1, top1_pid});

            auto it2 = mem2.begin();
            int top2_p = it2->first;
            int top2_pid = it2->second;
            int final2 = top2_p + delta[g2];
            global_set.erase({final2, top2_pid});

            // 合并集合
            for (const auto& elem : mem2) mem1.insert(elem);
            delta[g1] += delta[g2];

            // 清除被合并组的信息
            group_members.erase(g2);
            delta.erase(g2);
            parent[g2] = g1;   // 并查集合并

            // 插入新候选
            auto it_new = mem1.begin();
            int new_top_p = it_new->first;
            int new_top_pid = it_new->second;
            int new_final = new_top_p + delta[g1];
            global_set.insert({new_final, new_top_pid});
        }
        else if (op == "QUERY") {
            int pid;
            cin >> pid;
            int gid = find(pid);
            int p = proc_priority[pid];
            int final_priority = p + delta[gid];
            cout << final_priority << '\n';
        }
    }
    return 0;
}
```

# T3

1. 使用动态规划：$dp[t][state]$ 表示第 $t$ 个时间单位后的资源分布状态
2. 状态转移：对于每个状态，计算可能通过网络流传输到达的下一个状态
3. 网络流建模：源点向每个节点连边（容量为当前资源量），节点间按管道连边，节点向汇点连边（容量为目标状态资源量）
4. 优化：状态数可能很多，需要剪枝和合并等价状态

代码：

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;
const int MAXN = 5000; // 最大节点数
const ll INF = 1e18;
const ll M = 1000000; // 足够大的权重，确保方差最小化优先

struct Edge {
    int to, cap, cost, rev;
};

vector<Edge> graph[MAXN];
ll h[MAXN]; // 势函数
ll dist[MAXN];
int prevv[MAXN], preve[MAXN];

void add_edge(int from, int to, int cap, int cost) {
    graph[from].push_back((Edge){to, cap, cost, (int)graph[to].size()});
    graph[to].push_back((Edge){from, 0, -cost, (int)graph[from].size()-1});
}

// 最小费用流，从s到t输送f单位流量，返回最小费用
ll min_cost_flow(int s, int t, int f, int n) {
    ll res = 0;
    // 初始势：由于存在负权边，先用Bellman-Ford计算最短路
    fill(h, h+n, 0);
    // 实际上，因为我们的图是DAG，且初始势为0即可，但为了处理负权，我们还是运行一次Bellman-Ford
    bool updated = true;
    for (int iter = 0; iter < n && updated; iter++) {
        updated = false;
        for (int v = 0; v < n; v++) {
            if (h[v] == INF) continue;
            for (Edge &e : graph[v]) {
                if (e.cap > 0 && h[e.to] > h[v] + e.cost) {
                    h[e.to] = h[v] + e.cost;
                    updated = true;
                }
            }
        }
    }

    while (f > 0) {
        // 使用Dijkstra求最短路（基于势）
        fill(dist, dist+n, INF);
        dist[s] = 0;
        priority_queue<pair<ll,int>, vector<pair<ll,int>>, greater<pair<ll,int>>> pq;
        pq.push({0, s});
        while (!pq.empty()) {
            auto p = pq.top(); pq.pop();
            ll d = p.first;
            int v = p.second;
            if (dist[v] < d) continue;
            for (int i = 0; i < graph[v].size(); i++) {
                Edge &e = graph[v][i];
                if (e.cap > 0) {
                    ll nd = d + e.cost + h[v] - h[e.to];
                    if (dist[e.to] > nd) {
                        dist[e.to] = nd;
                        prevv[e.to] = v;
                        preve[e.to] = i;
                        pq.push({nd, e.to});
                    }
                }
            }
        }
        if (dist[t] == INF) {
            // 无法输送更多流量（理论上不会发生）
            return -1;
        }
        for (int v = 0; v < n; v++) {
            if (dist[v] < INF) h[v] += dist[v];
        }
        // 沿最短路增广
        int d = f;
        for (int v = t; v != s; v = prevv[v]) {
            d = min(d, graph[prevv[v]][preve[v]].cap);
        }
        f -= d;
        res += d * h[t]; // 实际费用即为新的势在汇点的值
        for (int v = t; v != s; v = prevv[v]) {
            Edge &e = graph[prevv[v]][preve[v]];
            e.cap -= d;
            graph[v][e.rev].cap += d;
        }
    }
    return res;
}

int main() {
    int n, m, k;
    cin >> n >> m >> k;
    vector<int> c(n+1), a(n+1);
    for (int i = 1; i <= n; i++) cin >> c[i];
    for (int i = 1; i <= n; i++) cin >> a[i];
    vector<tuple<int,int,int>> pipes;
    for (int i = 0; i < m; i++) {
        int u, v, w;
        cin >> u >> v >> w;
        pipes.push_back({u, v, w});
    }

    int S = 0; // 总资源量
    for (int i = 1; i <= n; i++) S += a[i];

    // 构建时间扩展网络
    // 节点编号：0: 源点 s, 1: 汇点 t
    // 对于每个资源站 i 和时间步 t (0..k)，有两个节点：in(i,t) 和 out(i,t)
    // 编号规则：in(i,t) = 2 + (i-1)*2*(k+1) + 2*t
    //          out(i,t)= 2 + (i-1)*2*(k+1) + 2*t+1
    int total_time_nodes = n * 2 * (k+1);
    int s = 0, t = 1;
    int N = total_time_nodes + 2;
    for (int i = 0; i < N; i++) graph[i].clear();

    // 记录管道边的信息，用于最后计算总传输量
    vector<tuple<int,int,int>> pipe_edges; // (from, edge_index, initial_cap)

    // 添加边
    // 1. 从源点 s 到 in(i,0)
    for (int i = 1; i <= n; i++) {
        int in_node = 2 + (i-1)*2*(k+1) + 0; // t=0 的 in 节点
        add_edge(s, in_node, a[i], 0);
    }

    // 2. 从 out(i,k) 到汇点 t：每条边容量1，费用为 M*(2j-1)
    for (int i = 1; i <= n; i++) {
        int out_node = 2 + (i-1)*2*(k+1) + 2*k + 1; // t=k 的 out 节点
        for (int j = 1; j <= c[i]; j++) {
            add_edge(out_node, t, 1, M * (2*j - 1));
        }
    }

    // 3. 对于每个 i,t：从 in(i,t) 到 out(i,t)
    for (int i = 1; i <= n; i++) {
        for (int tt = 0; tt <= k; tt++) {
            int in_node = 2 + (i-1)*2*(k+1) + 2*tt;
            int out_node = in_node + 1;
            add_edge(in_node, out_node, c[i], 0);
        }
    }

    // 4. 保留边：从 out(i,t) 到 in(i,t+1)
    for (int i = 1; i <= n; i++) {
        for (int tt = 0; tt < k; tt++) {
            int out_node = 2 + (i-1)*2*(k+1) + 2*tt + 1;
            int in_node_next = 2 + (i-1)*2*(k+1) + 2*(tt+1);
            add_edge(out_node, in_node_next, c[i], 0);
        }
    }

    // 5. 管道边：从 out(u,t) 到 in(v,t+1)
    for (auto &pipe : pipes) {
        int u = get<0>(pipe), v = get<1>(pipe), w = get<2>(pipe);
        for (int tt = 0; tt < k; tt++) {
            int out_node = 2 + (u-1)*2*(k+1) + 2*tt + 1;
            int in_node_next = 2 + (v-1)*2*(k+1) + 2*(tt+1);
            // 记录管道边
            int idx = graph[out_node].size();
            add_edge(out_node, in_node_next, w, -1);
            pipe_edges.push_back({out_node, idx, w});
        }
    }

    // 运行最小费用流，要求流量为 S
    ll total_cost = min_cost_flow(s, t, S, N);

    // 计算最终每个资源站的资源量 b_i 和总传输量 F
    vector<int> b(n+1, 0);
    ll sum_b2 = 0;
    for (int i = 1; i <= n; i++) {
        int out_node = 2 + (i-1)*2*(k+1) + 2*k + 1;
        for (Edge &e : graph[out_node]) {
            if (e.to == t) {
                // 初始容量为1，当前容量为 e.cap，所以流量为 1 - e.cap
                b[i] += (1 - e.cap);
            }
        }
        sum_b2 += (ll)b[i] * b[i];
    }

    // 计算总传输量 F：所有管道边上的流量之和
    ll F = 0;
    for (auto &pe : pipe_edges) {
        int from = get<0>(pe);
        int idx = get<1>(pe);
        int init_cap = get<2>(pe);
        int flow = init_cap - graph[from][idx].cap;
        F += flow;
    }

    // 计算不均衡度：n^2 倍方差 = n * sum(b_i^2) - S^2
    ll V = n * sum_b2 - (ll)S * S;
    cout << V << " " << F << endl;

    return 0;
}
```


```
