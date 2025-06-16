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
        unordered_set<int> node_indexes; //nodes that are part of this graph
};

AnonGraph g;
int k; //anonymization factor

vector<AnonGraph> neighborhood;
//only used for lookups as deque lookups are linear in time complexity
bool anonymized[1000001];

vector<vector<AnonGraph>> components;
vector<vector<string>> component_dfs_codes; //first index is the node corresponding to the neighborhood, second one is the component index
vector<string> dfs_code;

AnonGraph read_input() {
    AnonGraph g;
    int n, m, a, b;
    in>>n>>m>>k;
    g.n = n;
    g.m = m;
    for (int i=1;i<=g.m;i++) {
        in>>a>>b;
        g.v[a].push_back(b);
        g.v[b].push_back(a);
    }

    for (int i=0;i<g.n;i++)
        g.node_indexes.insert(i);
    return g;
}

//comparison function returning the node which has the biggest neighborhood
//first, in terms of number of nodes, second, in terms of number of edges.
bool neighborhood_cmp(int &a, int &b) {
    if (neighborhood[a].n != neighborhood[b].n) 
        return neighborhood[a].n > neighborhood[b].n;
    return neighborhood[a].m > neighborhood[b].m;
}

bool cost_cmp(pair<int,int> &a, pair<int, int> &b) {
    return a.second < b.second;
}

void compute_neighborhoods() {
    for (int i=0;i<g.n;i++) {
        AnonGraph neigh;

        neigh.n = 1 + g.v[i].size(); //number of nodes in neighborhood = current node + degree of the node
        neigh.m = 0;
        neigh.node_indexes.insert(i);
        for (int j : g.v[i]) {
            neigh.node_indexes.insert(j);
            neigh.v[i].push_back(j);
            neigh.m++;
        }
        for (int j : g.v[i]) {
            for (int k : g.v[j]) 
                if (neigh.node_indexes.find(k) != neigh.node_indexes.end()) 
                    neigh.v[j].push_back(k), neigh.m++;

        }
        neigh.m/=2; //we counted all edges twice
        neighborhood.push_back(neigh);
    }
}

//anonymizes the neighborhoods of nodes u and v to be isomorphic
void anonymize_neighborhoods(int u, int v) {
    //mark the two nodes as part of the same equivalence class in the end, also mark both of them as anonymized, updating vertexList
    //if this alters neighborhood of node u, also alter exactly the same way all of the neighborhoods of nodes that are in the same equivalence class as u, and mark all of them as unanonymized
}

//for our graph g and the neighborhoods of all of its nodes, finds the respective maximally connected subgraphs, 
//representing the connected components of each neighborhood
void find_neighborhood_components() {
    for (int i=0;i<neighborhood.size();i++) {
        AnonGraph g = neighborhood[i];
        bitset<1000001> visited; 
        for (int v: g.node_indexes) 
            if (!visited[v])
            {
                AnonGraph component;
                component.n = 0;
                component.m = 0;
                stack<int> st;
                st.push(v);
                while(!st.empty()) {
                    int front = st.top();
                    st.pop();
                    component.node_indexes.insert(front);
                    component.n++;
                    visited[front] = 1;
                    for (int u : g.v[front]) {
                        if (!visited[u])
                            st.push(u);
                        component.m++;
                        component.v[front].push_back(u);
                    }
                }
                component.m/=2; //we counted each edge twice
                components[i].push_back(component);
            }

    }
}

//call the gspan library on an instance of a graph to get its minimum dfs code
string get_min_dfs_code(const GSPAN::Graph& g) {
    DFSCode dfs_code;
    dfs_code.fromGraph(const_cast<GSPAN::Graph&>(g));

    // Create a gSpan instance only to check if this code is minimal
    gSpan gspan;
    gspan.GRAPH_IS_MIN = g;
    gspan.DFS_CODE_IS_MIN.clear();
    gspan.DFS_CODE_IS_MIN = dfs_code;

    if (!gspan.is_min()) {
        // If it's not minimal, is_min() modifies DFS_CODE_IS_MIN to be the minimal one
    }

    std::ostringstream oss;
    gspan.DFS_CODE_IS_MIN.write(oss);
    return oss.str();
}

//computes the minimum dfs code of a given component by converting the graph to a GSPAN::Graph instance and calling the above function
void compute_component_dfs_code(int node, int component_idx) {
    AnonGraph component = components[node][component_idx];
    GSPAN::Graph gspan_graph(false); // false = undirected

    std::unordered_map<int, int> old_to_new;
    int idx = 0;
    for (int u : component.node_indexes)
        old_to_new[u] = idx++;

    gspan_graph.resize(component.node_indexes.size());

    for (auto& [u, neighbors] : component.v) {
        int new_u = old_to_new[u];
        gspan_graph[new_u].label = 0;
        for (int v : neighbors) {
            int new_v = old_to_new[v];
            gspan_graph[new_u].push(new_u, new_v, 0);
        }
    }

    gspan_graph.buildEdge();
    string code = get_min_dfs_code(gspan_graph);
    component_dfs_codes[node][component_idx] = code;
}

void merge_dfs_codes(int neigh_idx) {
    vector<string> codes;
    for (int i=0;i<components[neigh_idx].size();i++) 
        codes.push_back(component_dfs_codes[neigh_idx][i]);
    sort(codes.begin(), codes.end());

    string merged_code;
    for (string code: codes) {
        merged_code += code + "|";
    }
    dfs_code[neigh_idx] = merged_code;
}

int main() {
    g = read_input();
    compute_neighborhoods();
    find_neighborhood_components();
    for (int i=0;i<neighborhood.size();i++) {
        for (int j=0;j<components[i].size();j++)
            compute_component_dfs_code(i, j);
        merge_dfs_codes(i);
    }
    //might need to be declared globally as anonymization functions may update which nodes are/not anonymized
    deque<int> vertexList(g.n);
    for (int i=0;i<g.n;i++)
        vertexList.push_back(i);
    sort(vertexList.begin(), vertexList.end(), neighborhood_cmp);
    while(!vertexList.empty()) {
        int seedVertex = vertexList.front();
        vertexList.pop_front();
        
        vector<pair<int,int>> candidateSet;
        for (int v: vertexList) {
            //use lower bound for the anonymization nodes between current node and all others, in order to compute the list of candidates for equivalence classes
            if (v != seedVertex) {
                int cost_lb = abs(neighborhood[seedVertex].m - neighborhood[v].m);
                candidateSet.push_back({v, cost_lb});
            }
        }

        sort(candidateSet.begin(), candidateSet.end(), cost_cmp);

        if (vertexList.size() >= 2*k - 1)
            while(candidateSet.size() > k - 1) 
                candidateSet.pop_back();
        //anonymize all 
        for (int i=0;i<candidateSet.size();i++) {
            anonymize_neighborhoods(seedVertex, candidateSet[i].first);
        }
    }
    //somehow print out the resulting graph/equivalence classes

    return 0;
}