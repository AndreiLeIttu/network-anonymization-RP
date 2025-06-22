include "alldifferent.mzn";

int: n;  % number of nodes
int: m;  % number of edges
int: k;  % k-anonymity

array[1..m] of tuple(int,int): initial_edges;
array[1..n*n] of var bool: edges;

% Index = ((x-1)*n + (y-1))*n + i, ranges 1..n^3
array[1..n*n*n] of var 1..n: phi;

array[1..n] of var set of int: neighborhood =
  [ { i | i in 1..n where edges[(j-1)*n + i] \/ edges[(i-1)*n + j] }
    | j in 1..n ];

array[1..n] of var int: neighborhood_size =
  [ card(neighborhood[j]) | j in 1..n ];

array[1..n*n] of var bool: isomorphic;


%–– Helper to flatten phi[x,y,i] → phi_flat(x,y,i) ––
function var int: phi_flat(int: x, int: y, int: i) =
  phi[((x - 1) * n * n) + ((y - 1) * n) + i];

constraint
  forall(x, y in 1..n where x != y) (
    isomorphic[(x-1)*n+y] <-> (
      neighborhood_size[x] = neighborhood_size[y]
      /\
      forall(i in neighborhood[x]) (
        phi_flat(x,y,i) in neighborhood[y]
      )
      /\
      all_different([ phi_flat(x,y,i) | i in neighborhood[x] ])
      /\
      forall(i, j in neighborhood[x] where i < j) (
        edges[(i-1)*n + j]
        =
        edges[
          (phi_flat(x,y,i) - 1) * n
          + phi_flat(x,y,j)
        ]
      )
    )
  );

constraint
  forall(i in 1..n) (
    sum(j in 1..n where i != j)(bool2int(isomorphic[(i-1)*n+j]))
    >= k - 1
  );

constraint
  forall(e in initial_edges) (
    edges[(e.1 - 1)*n + e.2] = true /\
    edges[(e.2 - 1)*n + e.1] = true
  );

constraint
  forall(i, j in 1..n where i < j)(
    edges[(i-1)*n + j] = edges[(j-1)*n + i]
  );
constraint
  forall(i in 1..n)(
    edges[(i-1)*n + i] = false
  );

solve 
  minimize sum([ bool2int(edges[(i-1)*n + j]) | i, j in 1..n ]);


output [
  "%---------------%\n",
  "objective = ",
    show(sum([ bool2int(edges[(i-1)*n + j]) | i, j in 1..n where i < j ])),
]
++
[
  "\nEdges (i,j):\n",
  concat([
    if fix(edges[(i-1)*n + j]) then
      show(i) ++ " " ++ show(j) ++ "\n"
    else
      ""
    endif
    | i, j in 1..n where i < j
  ])
];
