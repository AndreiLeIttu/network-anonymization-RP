include "alldifferent.mzn";

int: n; %number of nodes
int: m; %number of edges
int: k; %k-anonymity 

array[1..m] of tuple(int,int): initial_edges;
array[1..n, 1..n] of var bool: edges;

int: unused = n+1;
array[1..n, 1..n] of var 1..unused: phi; %node assignments for the purpose of isomorphism tests

array[1..n] of var set of int: neighborhood= 
  [ {i | i in 1..n where i = j \/ edges[j, i] \/ edges[i, j]} | j in 1..n ];
array[1..n] of var int: neighborhood_size = 
  [card(neighborhood[j]) | j in 1..n];


predicate isomorphic(int: x, int: y) =
    neighborhood_size[x] = neighborhood_size[y] /\
    forall(i in neighborhood[x]) (
      phi[x, i] in neighborhood[y]
    ) /\
    forall(i in neighborhood[x], j in neighborhood[x] where i != j) (
      (edges[i, j] -> edges[phi[x, i], phi[x, j]]) /\
      (edges[phi[x, i], phi[x, j]] -> edges[i, j])
    );


%constraints 

%all node assignments for a neighborhood are different
constraint forall(i in 1..n) (
  all_different([
    phi[i, j] | j in neighborhood[i]
  ])
);

constraint forall(i, j in 1..n where i != j /\ not edges[i, j] /\ not edges[j, i]) (
  phi[i, j] = n+1
);

%all initial edges are in the final graph
constraint forall(e in initial_edges) (
  edges[e.1, e.2] = true /\ 
  edges[e.2, e.1] = true
); 

%ensure symmetry for all edges in the final graph
constraint forall(i, j in 1..n where i<j) (edges[i,j] = edges[j,i]);
constraint forall(i in 1..n) (edges[i,i] = 0);

%for each node, there must be at least k-1 nodes for which the two are equivalent
constraint forall(i in 1..n) (
  sum(j in 1..n where i != j)(bool2int(isomorphic(i, j))) >= k-1
);

solve minimize sum([bool2int(edges[i,j]) | i, j in 1..n]);