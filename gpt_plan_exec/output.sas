begin_version
3
end_version
begin_metric
1
end_metric
11
begin_variable
var0
-1
2
Atom clear_a()
NegatedAtom clear_a()
end_variable
begin_variable
var1
-1
2
Atom clear_b()
NegatedAtom clear_b()
end_variable
begin_variable
var2
-1
2
Atom clear_c()
NegatedAtom clear_c()
end_variable
begin_variable
var3
-1
2
Atom clear_d()
NegatedAtom clear_d()
end_variable
begin_variable
var4
-1
2
Atom clear_e()
NegatedAtom clear_e()
end_variable
begin_variable
var5
-1
2
Atom handempty()
NegatedAtom handempty()
end_variable
begin_variable
var6
-1
6
Atom holding_a()
Atom on_a_b()
Atom on_a_c()
Atom on_a_d()
Atom on_a_e()
Atom ontable_a()
end_variable
begin_variable
var7
-1
6
Atom holding_b()
Atom on_b_a()
Atom on_b_c()
Atom on_b_d()
Atom on_b_e()
Atom ontable_b()
end_variable
begin_variable
var8
-1
6
Atom holding_c()
Atom on_c_a()
Atom on_c_b()
Atom on_c_d()
Atom on_c_e()
Atom ontable_c()
end_variable
begin_variable
var9
-1
6
Atom holding_d()
Atom on_d_a()
Atom on_d_b()
Atom on_d_c()
Atom on_d_e()
Atom ontable_d()
end_variable
begin_variable
var10
-1
6
Atom holding_e()
Atom on_e_a()
Atom on_e_b()
Atom on_e_c()
Atom on_e_d()
Atom ontable_e()
end_variable
11
begin_mutex_group
6
0 0
6 0
7 1
8 1
9 1
10 1
end_mutex_group
begin_mutex_group
6
1 0
6 1
7 0
8 2
9 2
10 2
end_mutex_group
begin_mutex_group
6
2 0
6 2
7 2
8 0
9 3
10 3
end_mutex_group
begin_mutex_group
6
3 0
6 3
7 3
8 3
9 0
10 4
end_mutex_group
begin_mutex_group
6
4 0
6 4
7 4
8 4
9 4
10 0
end_mutex_group
begin_mutex_group
6
5 0
6 0
7 0
8 0
9 0
10 0
end_mutex_group
begin_mutex_group
6
6 0
6 1
6 2
6 3
6 4
6 5
end_mutex_group
begin_mutex_group
6
7 0
7 1
7 2
7 3
7 4
7 5
end_mutex_group
begin_mutex_group
6
8 0
8 1
8 2
8 3
8 4
8 5
end_mutex_group
begin_mutex_group
6
9 0
9 1
9 2
9 3
9 4
9 5
end_mutex_group
begin_mutex_group
6
10 0
10 1
10 2
10 3
10 4
10 5
end_mutex_group
begin_state
1
1
0
0
1
0
5
1
4
5
2
end_state
begin_goal
4
6 4
7 3
9 3
10 2
end_goal
50
begin_operator
pick-up_a 
0
3
0 0 0 1
0 5 0 1
0 6 5 0
1
end_operator
begin_operator
pick-up_b 
0
3
0 1 0 1
0 5 0 1
0 7 5 0
1
end_operator
begin_operator
pick-up_c 
0
3
0 2 0 1
0 5 0 1
0 8 5 0
1
end_operator
begin_operator
pick-up_d 
0
3
0 3 0 1
0 5 0 1
0 9 5 0
1
end_operator
begin_operator
pick-up_e 
0
3
0 4 0 1
0 5 0 1
0 10 5 0
1
end_operator
begin_operator
put-down_a 
0
3
0 0 -1 0
0 5 -1 0
0 6 0 5
1
end_operator
begin_operator
put-down_b 
0
3
0 1 -1 0
0 5 -1 0
0 7 0 5
1
end_operator
begin_operator
put-down_c 
0
3
0 2 -1 0
0 5 -1 0
0 8 0 5
1
end_operator
begin_operator
put-down_d 
0
3
0 3 -1 0
0 5 -1 0
0 9 0 5
1
end_operator
begin_operator
put-down_e 
0
3
0 4 -1 0
0 5 -1 0
0 10 0 5
1
end_operator
begin_operator
stack_a_b 
0
4
0 0 -1 0
0 1 0 1
0 5 -1 0
0 6 0 1
1
end_operator
begin_operator
stack_a_c 
0
4
0 0 -1 0
0 2 0 1
0 5 -1 0
0 6 0 2
1
end_operator
begin_operator
stack_a_d 
0
4
0 0 -1 0
0 3 0 1
0 5 -1 0
0 6 0 3
1
end_operator
begin_operator
stack_a_e 
0
4
0 0 -1 0
0 4 0 1
0 5 -1 0
0 6 0 4
1
end_operator
begin_operator
stack_b_a 
0
4
0 0 0 1
0 1 -1 0
0 5 -1 0
0 7 0 1
1
end_operator
begin_operator
stack_b_c 
0
4
0 1 -1 0
0 2 0 1
0 5 -1 0
0 7 0 2
1
end_operator
begin_operator
stack_b_d 
0
4
0 1 -1 0
0 3 0 1
0 5 -1 0
0 7 0 3
1
end_operator
begin_operator
stack_b_e 
0
4
0 1 -1 0
0 4 0 1
0 5 -1 0
0 7 0 4
1
end_operator
begin_operator
stack_c_a 
0
4
0 0 0 1
0 2 -1 0
0 5 -1 0
0 8 0 1
1
end_operator
begin_operator
stack_c_b 
0
4
0 1 0 1
0 2 -1 0
0 5 -1 0
0 8 0 2
1
end_operator
begin_operator
stack_c_d 
0
4
0 2 -1 0
0 3 0 1
0 5 -1 0
0 8 0 3
1
end_operator
begin_operator
stack_c_e 
0
4
0 2 -1 0
0 4 0 1
0 5 -1 0
0 8 0 4
1
end_operator
begin_operator
stack_d_a 
0
4
0 0 0 1
0 3 -1 0
0 5 -1 0
0 9 0 1
1
end_operator
begin_operator
stack_d_b 
0
4
0 1 0 1
0 3 -1 0
0 5 -1 0
0 9 0 2
1
end_operator
begin_operator
stack_d_c 
0
4
0 2 0 1
0 3 -1 0
0 5 -1 0
0 9 0 3
1
end_operator
begin_operator
stack_d_e 
0
4
0 3 -1 0
0 4 0 1
0 5 -1 0
0 9 0 4
1
end_operator
begin_operator
stack_e_a 
0
4
0 0 0 1
0 4 -1 0
0 5 -1 0
0 10 0 1
1
end_operator
begin_operator
stack_e_b 
0
4
0 1 0 1
0 4 -1 0
0 5 -1 0
0 10 0 2
1
end_operator
begin_operator
stack_e_c 
0
4
0 2 0 1
0 4 -1 0
0 5 -1 0
0 10 0 3
1
end_operator
begin_operator
stack_e_d 
0
4
0 3 0 1
0 4 -1 0
0 5 -1 0
0 10 0 4
1
end_operator
begin_operator
unstack_a_b 
0
4
0 0 0 1
0 1 -1 0
0 5 0 1
0 6 1 0
1
end_operator
begin_operator
unstack_a_c 
0
4
0 0 0 1
0 2 -1 0
0 5 0 1
0 6 2 0
1
end_operator
begin_operator
unstack_a_d 
0
4
0 0 0 1
0 3 -1 0
0 5 0 1
0 6 3 0
1
end_operator
begin_operator
unstack_a_e 
0
4
0 0 0 1
0 4 -1 0
0 5 0 1
0 6 4 0
1
end_operator
begin_operator
unstack_b_a 
0
4
0 0 -1 0
0 1 0 1
0 5 0 1
0 7 1 0
1
end_operator
begin_operator
unstack_b_c 
0
4
0 1 0 1
0 2 -1 0
0 5 0 1
0 7 2 0
1
end_operator
begin_operator
unstack_b_d 
0
4
0 1 0 1
0 3 -1 0
0 5 0 1
0 7 3 0
1
end_operator
begin_operator
unstack_b_e 
0
4
0 1 0 1
0 4 -1 0
0 5 0 1
0 7 4 0
1
end_operator
begin_operator
unstack_c_a 
0
4
0 0 -1 0
0 2 0 1
0 5 0 1
0 8 1 0
1
end_operator
begin_operator
unstack_c_b 
0
4
0 1 -1 0
0 2 0 1
0 5 0 1
0 8 2 0
1
end_operator
begin_operator
unstack_c_d 
0
4
0 2 0 1
0 3 -1 0
0 5 0 1
0 8 3 0
1
end_operator
begin_operator
unstack_c_e 
0
4
0 2 0 1
0 4 -1 0
0 5 0 1
0 8 4 0
1
end_operator
begin_operator
unstack_d_a 
0
4
0 0 -1 0
0 3 0 1
0 5 0 1
0 9 1 0
1
end_operator
begin_operator
unstack_d_b 
0
4
0 1 -1 0
0 3 0 1
0 5 0 1
0 9 2 0
1
end_operator
begin_operator
unstack_d_c 
0
4
0 2 -1 0
0 3 0 1
0 5 0 1
0 9 3 0
1
end_operator
begin_operator
unstack_d_e 
0
4
0 3 0 1
0 4 -1 0
0 5 0 1
0 9 4 0
1
end_operator
begin_operator
unstack_e_a 
0
4
0 0 -1 0
0 4 0 1
0 5 0 1
0 10 1 0
1
end_operator
begin_operator
unstack_e_b 
0
4
0 1 -1 0
0 4 0 1
0 5 0 1
0 10 2 0
1
end_operator
begin_operator
unstack_e_c 
0
4
0 2 -1 0
0 4 0 1
0 5 0 1
0 10 3 0
1
end_operator
begin_operator
unstack_e_d 
0
4
0 3 -1 0
0 4 0 1
0 5 0 1
0 10 4 0
1
end_operator
0
