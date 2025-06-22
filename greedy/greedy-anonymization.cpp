#include <iostream>
#include <fstream>
#include <vector>
#include <set>
#include <unordered_set>
#include <algorithm>
#include <deque>
#include <unordered_map>
#include <bitset>
#include <stack>
#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/vf2_sub_graph_iso.hpp>
#include "gspan.h"
#include <sstream>

using namespace std;
using namespace GSPAN;

ifstream in("graph_input.in");

class AnonGraph {
public:
    int n;
    int m;
    unordered_map<int, vector<int>> v;
    unordered_set<int> node_indexes;
};

AnonGraph g;
int k;
vector<AnonGraph> neighborhood;
bool anonymized[1000001] = {false};
vector<vector<AnonGraph>> components;
vector<vector<string>> component_dfs_codes;
vector<string> dfs_code;
deque<int> unanonymizedVertices;
int edgesAdded = 0;

// Stub out mexprint to avoid linking mexgspan.cpp
namespace GSPAN {
    void Graph::mexprint() {}
}

AnonGraph read_input() {
    AnonGraph g;
    int n, m, a, b;
    in >> n >> m >> k;
    g.n = n;
    g.m = 0;
    // Read edges, filter out duplicates and self-loops
    set<pair<int,int>> seen;
    for (int i = 0; i < m; i++) {
        in >> a >> b;
        if (a == b) continue;  // skip self-loops
        int u = a, v = b;
        if (u > v) swap(u, v);
        if (seen.insert({u, v}).second) {
            g.v[u].push_back(v);
            g.v[v].push_back(u);
            g.m++;
        }
    }
    for (int i = 0; i < n; i++)
        g.node_indexes.insert(i);
    return g;
}

bool neighborhood_cmp(int &a, int &b) {
    if (neighborhood[a].n != neighborhood[b].n)
        return neighborhood[a].n > neighborhood[b].n;
    return neighborhood[a].m > neighborhood[b].m;
}

bool component_cmp(const AnonGraph &a, const AnonGraph &b) {
    return a.n > b.n;
}
bool cost_cmp(const pair<int,int> &a, const pair<int,int> &b) {
    return a.second < b.second;
}

void compute_neighborhoods() {
    for (int i = 0; i < g.n; i++) {
        AnonGraph neigh;
        neigh.n = g.v[i].size();
        neigh.m = 0;
        for (int j : g.v[i])
            neigh.node_indexes.insert(j);
        for (int j : g.v[i]) {
            for (int k : g.v[j]) {
                if (neigh.node_indexes.count(k)) {
                    neigh.v[j].push_back(k);
                    neigh.m++;
                }
            }
        }
        neigh.m /= 2;
        neighborhood.push_back(neigh);
    }
}

int compute_similarity(const AnonGraph &x, const AnonGraph &y) {
    return abs(x.n - y.n) + abs(x.m - y.m);
}

typedef boost::adjacency_list<boost::vecS, boost::vecS, boost::undirectedS> BoostGraph;

template <typename Graph1, typename Graph2>
struct vf2_callback {
    vf2_callback(const Graph1 &g1, const Graph2 &g2,
                 unordered_map<int,int> &map12)
        : graph1(g1), graph2(g2), mapping(map12) {}

    template <typename CorrespondenceMap1To2, typename CorrespondenceMap2To1>
    bool operator()(CorrespondenceMap1To2 f, CorrespondenceMap2To1) const {
        BGL_FORALL_VERTICES_T(v, graph1, Graph1) {
            int tgt = get(f, v);
            mapping[v] = tgt;
        }
        return true;
    }
    const Graph1 &graph1;
    const Graph2 &graph2;
    unordered_map<int,int> &mapping;
};

void anonymize_neighborhoods(int u, int v) {
    bitset<10000> matched_u, matched_v;
    // Perfect DFS-code matches
    for (int i = 0; i < (int)components[u].size(); i++) {
        for (int j = 0; j < (int)components[v].size(); j++) {
            if (component_dfs_codes[u][i] == component_dfs_codes[v][j]) {
                matched_u[i] = matched_v[j] = 1;
                break;
            }
        }
    }
    // Compute similarity list
    vector<vector<pair<int,int>>> sims(components[u].size());
    for (int i = 0; i < (int)components[u].size(); i++) {
        if (matched_u[i]) continue;
        for (int j = 0; j < (int)components[v].size(); j++) {
            if (matched_v[j]) continue;
            sims[i].push_back({j, compute_similarity(components[u][i], components[v][j])});
        }
        sort(sims[i].begin(), sims[i].end(), cost_cmp);
    }
    // Greedy match remaining by similarity
    vector<pair<int,int>> matched_pairs;
    for (int i = 0; i < (int)sims.size(); i++) {
        if (matched_u[i]) continue;
        for (auto &p : sims[i]) {
            int j = p.first;
            if (!matched_v[j]) {
                matched_u[i] = matched_v[j] = 1;
                matched_pairs.emplace_back(i,j);
                break;
            }
        }
    }
    // Iso-map and edge-copy for matched components
    for (auto &pr : matched_pairs) {
        int ci = pr.first, cj = pr.second;
        const auto &compU = components[u][ci], &compV = components[v][cj];
        BoostGraph BG1(compU.node_indexes.size()), BG2(compV.node_indexes.size());
        unordered_map<int,int> toIdxU, toIdxV;
        vector<int> fromU, fromV;
        int idx = 0;
        for (int x : compU.node_indexes) { toIdxU[x] = idx++; fromU.push_back(x); }
        idx = 0;
        for (int x : compV.node_indexes) { toIdxV[x] = idx++; fromV.push_back(x); }
        for (auto &kv : compU.v) {
            int x = kv.first;
            for (int y : kv.second) {
                if (toIdxU.count(y)) add_edge(toIdxU[x], toIdxU[y], BG1);
            }
        }
        for (auto &kv : compV.v) {
            int x = kv.first;
            for (int y : kv.second) {
                if (toIdxV.count(y)) add_edge(toIdxV[x], toIdxV[y], BG2);
            }
        }
        unordered_map<int,int> iso_map;
        vf2_callback<BoostGraph,BoostGraph> callback(BG1, BG2, iso_map);
        boost::vf2_subgraph_iso(BG1, BG2, callback);
        // Copy missing edges
        for (auto &m1 : iso_map) {
            for (auto &m2 : iso_map) {
                int u1 = fromU[m1.first], v1 = fromU[m2.first];
                int u2 = fromV[m1.second], v2 = fromV[m2.second];
                bool inV = (find(g.v[u2].begin(), g.v[u2].end(), v2) != g.v[u2].end());
                bool inU = (find(g.v[u1].begin(), g.v[u1].end(), v1) != g.v[u1].end());
                if (inV && !inU) { g.v[u1].push_back(v1); g.v[v1].push_back(u1); edgesAdded++; }
                if (inU && !inV) { g.v[u2].push_back(v2); g.v[v2].push_back(u2); edgesAdded++; }
            }
        }
    }
    // If component counts differ, add whole unmatched comps
    if (components[u].size() > components[v].size()) {
        for (int i = 0; i < (int)components[u].size(); ++i) {
            if (!matched_u[i]) {
                for (int x : components[u][i].node_indexes) {
                    if (find(g.v[v].begin(), g.v[v].end(), x) == g.v[v].end()) {
                        g.v[v].push_back(x);
                        g.v[x].push_back(v);
                        edgesAdded++;
                    }
                }
            }
        }
    } else if (components[u].size() < components[v].size()) {
        for (int j = 0; j < (int)components[v].size(); ++j) {
            if (!matched_v[j]) {
                for (int x : components[v][j].node_indexes) {
                    if (find(g.v[u].begin(), g.v[u].end(), x) == g.v[u].end()) {
                        g.v[u].push_back(x);
                        g.v[x].push_back(u);
                        edgesAdded++;
                    }
                }
            }
        }
    }
    anonymized[u] = anonymized[v] = true;
}

void find_neighborhood_components() {
    components.resize(neighborhood.size());
    for (int i = 0; i < (int)neighborhood.size(); i++) {
        AnonGraph &ng = neighborhood[i];
        bitset<1000001> vis;
        for (int v : ng.node_indexes) {
            if (!vis[v]) {
                AnonGraph comp;
                stack<int> st;
                st.push(v);
                while (!st.empty()) {
                    int x = st.top(); st.pop();
                    if (vis[x]) continue;
                    vis[x] = 1;
                    comp.node_indexes.insert(x);
                    comp.n++;
                    for (int y : ng.v[x]) {
                        comp.v[x].push_back(y);
                        comp.m++;
                        if (!vis[y]) st.push(y);
                    }
                }
                comp.m /= 2;
                components[i].push_back(comp);
            }
        }
        sort(components[i].begin(), components[i].end(), component_cmp);
    }
}

string get_min_dfs_code(const GSPAN::Graph &g) {
    GSPAN::DFSCode dfs_code;
    dfs_code.fromGraph(const_cast<GSPAN::Graph &>(g));
    GSPAN::gSpan gspan;
    gspan.GRAPH_IS_MIN = g;
    gspan.DFS_CODE_IS_MIN.clear();
    gspan.DFS_CODE_IS_MIN = dfs_code;
    if (!gspan.is_min());
    ostringstream oss;
    gspan.DFS_CODE_IS_MIN.write(oss);
    return oss.str();
}

void compute_component_dfs_code(int node, int cidx) {
    AnonGraph &comp = components[node][cidx];
    GSPAN::Graph gs(false);
    unordered_map<int,int> old2new;
    int idx = 0;
    for (int x : comp.node_indexes) old2new[x] = idx++;
    gs.resize(comp.node_indexes.size());
    for (auto &kv : comp.v) {
        int x = old2new[kv.first];
        gs[x].label = 0;
        for (int y : kv.second) gs[x].push(x, old2new[y], 0);
    }
    gs.buildEdge();
    component_dfs_codes[node][cidx] = get_min_dfs_code(gs);
}

void merge_dfs_codes(int idx) {
    vector<string> codes = component_dfs_codes[idx];
    sort(codes.begin(), codes.end());
    dfs_code[idx].clear();
    for (auto &c : codes) dfs_code[idx] += c + "|";
}

int main() {
    g = read_input();
    compute_neighborhoods();
    find_neighborhood_components();
    component_dfs_codes.assign(neighborhood.size(), vector<string>());
    for (int i = 0; i < (int)neighborhood.size(); i++) {
        component_dfs_codes[i].resize(components[i].size());
        for (int j = 0; j < (int)components[i].size(); j++)
            compute_component_dfs_code(i, j);
    }
    dfs_code.resize(neighborhood.size());
    for (int i = 0; i < (int)neighborhood.size(); i++)
        merge_dfs_codes(i);

    for (int i = 0; i < g.n; i++) unanonymizedVertices.push_back(i);
    sort(unanonymizedVertices.begin(), unanonymizedVertices.end(), neighborhood_cmp);

    while (!unanonymizedVertices.empty()) {
        int u = unanonymizedVertices.front();
        unanonymizedVertices.pop_front();
        if (anonymized[u]) continue;
        vector<pair<int,int>> cand;
        for (int vtx : unanonymizedVertices) {
            if (vtx == u || anonymized[vtx]) continue;
            int lb = abs(neighborhood[u].m - neighborhood[vtx].m);
            cand.emplace_back(vtx, lb);
        }
        sort(cand.begin(), cand.end(), cost_cmp);
        if (cand.size() >= (size_t)2*k-1) cand.resize(k-1);
        for (auto &p : cand)
            anonymize_neighborhoods(u, p.first);
    }
    set<pair<int,int>> outEdges;
    for (auto &kv : g.v) {
        int u = kv.first;
        for (int w : kv.second) {
            if (u < w) outEdges.emplace(u,w);
        }
    }
    cout << "Final edges:\n";
    for (auto &e : outEdges)
        cout << e.first << " " << e.second << "\n";
    cout << "Edges added: " << edgesAdded << "\n";
    return 0;
}
