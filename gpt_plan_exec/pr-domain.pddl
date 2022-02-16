(define
	(domain grounded-BLOCKS)
	(:requirements :strips :action-costs)
	(:predicates
		( HOLDING_F )
		( ON_F_F )
		( ON_F_C )
		( HOLDING_C )
		( CLEAR_E )
		( ONTABLE_C )
		( ON_F_E )
		( ON_C_F )
		( ON_C_C )
		( HOLDING_E )
		( CLEAR_J )
		( ONTABLE_E )
		( ON_E_E )
		( ON_E_F )
		( ON_E_C )
		( ON_F_J )
		( ON_C_J )
		( HOLDING_J )
		( CLEAR_B )
		( ONTABLE_J )
		( ON_J_J )
		( ON_J_E )
		( ON_J_F )
		( ON_J_C )
		( ON_E_B )
		( ON_F_B )
		( ON_C_B )
		( HOLDING_B )
		( CLEAR_G )
		( ONTABLE_B )
		( ON_B_B )
		( ON_B_J )
		( ON_B_E )
		( ON_B_F )
		( ON_B_C )
		( ON_J_G )
		( ON_E_G )
		( ON_F_G )
		( ON_C_G )
		( HOLDING_G )
		( CLEAR_H )
		( ONTABLE_G )
		( ON_G_G )
		( ON_G_B )
		( ON_G_J )
		( ON_G_E )
		( ON_G_F )
		( ON_G_C )
		( ON_B_H )
		( ON_J_H )
		( ON_E_H )
		( ON_F_H )
		( ON_C_H )
		( HOLDING_H )
		( CLEAR_A )
		( ONTABLE_H )
		( ON_H_H )
		( ON_H_G )
		( ON_H_B )
		( ON_H_J )
		( ON_H_E )
		( ON_H_F )
		( ON_H_C )
		( ON_G_A )
		( ON_B_A )
		( ON_J_A )
		( ON_E_A )
		( ON_F_A )
		( ON_C_A )
		( HOLDING_A )
		( CLEAR_D )
		( ONTABLE_A )
		( ON_A_A )
		( ON_A_H )
		( ON_A_G )
		( ON_A_B )
		( ON_A_J )
		( ON_A_E )
		( ON_A_F )
		( ON_A_C )
		( ON_H_D )
		( ON_G_D )
		( ON_B_D )
		( ON_J_D )
		( ON_E_D )
		( ON_F_D )
		( ON_C_D )
		( HOLDING_D )
		( CLEAR_I )
		( HOLDING_I )
		( ONTABLE_D )
		( ON_D_D )
		( ON_D_A )
		( ON_D_H )
		( ON_D_G )
		( ON_D_B )
		( ON_D_J )
		( ON_D_E )
		( ON_D_F )
		( ON_D_C )
		( ON_A_I )
		( ON_H_I )
		( ON_G_I )
		( ON_B_I )
		( ON_J_I )
		( ON_E_I )
		( ON_I_D )
		( ON_I_A )
		( ON_I_H )
		( ON_I_G )
		( ON_I_B )
		( ON_I_J )
		( ON_I_E )
		( ON_I_I )
		( ON_I_F )
		( ON_I_C )
		( ON_F_I )
		( ON_C_I )
		( HANDEMPTY )
		( CLEAR_C )
		( CLEAR_F )
		( ONTABLE_I )
		( ON_D_I )
		( ON_A_D )
		( ON_H_A )
		( ON_G_H )
		( ON_B_G )
		( ON_J_B )
		( ON_E_J )
		( ON_C_E )
		( ONTABLE_F )
	) 
	(:functions (total-cost))
	(:action PICK-UP_D
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( ONTABLE_D )
			( CLEAR_D )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_D )
			(not ( ONTABLE_D ))
			(not ( CLEAR_D ))
			(not ( HANDEMPTY ))
		)
	)
	(:action UNSTACK_C_I
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_C )
			( ON_C_I )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_C )
			( CLEAR_I )
			(not ( CLEAR_C ))
			(not ( HANDEMPTY ))
			(not ( ON_C_I ))
		)
	)
	(:action UNSTACK_F_I
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_F )
			( ON_F_I )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_F )
			( CLEAR_I )
			(not ( CLEAR_F ))
			(not ( HANDEMPTY ))
			(not ( ON_F_I ))
		)
	)
	(:action UNSTACK_I_C
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_I )
			( ON_I_C )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_I )
			( CLEAR_C )
			(not ( CLEAR_I ))
			(not ( HANDEMPTY ))
			(not ( ON_I_C ))
		)
	)
	(:action UNSTACK_I_F
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_I )
			( ON_I_F )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_I )
			( CLEAR_F )
			(not ( CLEAR_I ))
			(not ( HANDEMPTY ))
			(not ( ON_I_F ))
		)
	)
	(:action UNSTACK_I_I
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_I )
			( ON_I_I )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_I )
			(not ( HANDEMPTY ))
			(not ( ON_I_I ))
		)
	)
	(:action UNSTACK_I_E
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_I )
			( ON_I_E )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_I )
			( CLEAR_E )
			(not ( CLEAR_I ))
			(not ( HANDEMPTY ))
			(not ( ON_I_E ))
		)
	)
	(:action UNSTACK_I_J
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_I )
			( ON_I_J )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_I )
			( CLEAR_J )
			(not ( CLEAR_I ))
			(not ( HANDEMPTY ))
			(not ( ON_I_J ))
		)
	)
	(:action UNSTACK_I_B
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_I )
			( ON_I_B )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_I )
			( CLEAR_B )
			(not ( CLEAR_I ))
			(not ( HANDEMPTY ))
			(not ( ON_I_B ))
		)
	)
	(:action UNSTACK_I_G
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_I )
			( ON_I_G )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_I )
			( CLEAR_G )
			(not ( CLEAR_I ))
			(not ( HANDEMPTY ))
			(not ( ON_I_G ))
		)
	)
	(:action UNSTACK_I_H
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_I )
			( ON_I_H )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_I )
			( CLEAR_H )
			(not ( CLEAR_I ))
			(not ( HANDEMPTY ))
			(not ( ON_I_H ))
		)
	)
	(:action UNSTACK_I_A
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_I )
			( ON_I_A )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_I )
			( CLEAR_A )
			(not ( CLEAR_I ))
			(not ( HANDEMPTY ))
			(not ( ON_I_A ))
		)
	)
	(:action UNSTACK_I_D
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_I )
			( ON_I_D )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_I )
			( CLEAR_D )
			(not ( CLEAR_I ))
			(not ( HANDEMPTY ))
			(not ( ON_I_D ))
		)
	)
	(:action UNSTACK_E_I
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_E )
			( ON_E_I )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_E )
			( CLEAR_I )
			(not ( CLEAR_E ))
			(not ( HANDEMPTY ))
			(not ( ON_E_I ))
		)
	)
	(:action UNSTACK_J_I
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_J )
			( ON_J_I )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_J )
			( CLEAR_I )
			(not ( CLEAR_J ))
			(not ( HANDEMPTY ))
			(not ( ON_J_I ))
		)
	)
	(:action UNSTACK_B_I
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_B )
			( ON_B_I )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_B )
			( CLEAR_I )
			(not ( CLEAR_B ))
			(not ( HANDEMPTY ))
			(not ( ON_B_I ))
		)
	)
	(:action UNSTACK_G_I
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_G )
			( ON_G_I )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_G )
			( CLEAR_I )
			(not ( CLEAR_G ))
			(not ( HANDEMPTY ))
			(not ( ON_G_I ))
		)
	)
	(:action UNSTACK_H_I
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_H )
			( ON_H_I )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_H )
			( CLEAR_I )
			(not ( CLEAR_H ))
			(not ( HANDEMPTY ))
			(not ( ON_H_I ))
		)
	)
	(:action UNSTACK_A_I
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_A )
			( ON_A_I )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_A )
			( CLEAR_I )
			(not ( CLEAR_A ))
			(not ( HANDEMPTY ))
			(not ( ON_A_I ))
		)
	)
	(:action UNSTACK_D_C
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_D )
			( ON_D_C )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_D )
			( CLEAR_C )
			(not ( CLEAR_D ))
			(not ( HANDEMPTY ))
			(not ( ON_D_C ))
		)
	)
	(:action UNSTACK_D_F
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_D )
			( ON_D_F )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_D )
			( CLEAR_F )
			(not ( CLEAR_D ))
			(not ( HANDEMPTY ))
			(not ( ON_D_F ))
		)
	)
	(:action UNSTACK_D_E
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_D )
			( ON_D_E )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_D )
			( CLEAR_E )
			(not ( CLEAR_D ))
			(not ( HANDEMPTY ))
			(not ( ON_D_E ))
		)
	)
	(:action UNSTACK_D_J
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_D )
			( ON_D_J )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_D )
			( CLEAR_J )
			(not ( CLEAR_D ))
			(not ( HANDEMPTY ))
			(not ( ON_D_J ))
		)
	)
	(:action UNSTACK_D_B
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_D )
			( ON_D_B )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_D )
			( CLEAR_B )
			(not ( CLEAR_D ))
			(not ( HANDEMPTY ))
			(not ( ON_D_B ))
		)
	)
	(:action UNSTACK_D_G
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_D )
			( ON_D_G )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_D )
			( CLEAR_G )
			(not ( CLEAR_D ))
			(not ( HANDEMPTY ))
			(not ( ON_D_G ))
		)
	)
	(:action UNSTACK_D_H
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_D )
			( ON_D_H )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_D )
			( CLEAR_H )
			(not ( CLEAR_D ))
			(not ( HANDEMPTY ))
			(not ( ON_D_H ))
		)
	)
	(:action UNSTACK_D_A
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_D )
			( ON_D_A )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_D )
			( CLEAR_A )
			(not ( CLEAR_D ))
			(not ( HANDEMPTY ))
			(not ( ON_D_A ))
		)
	)
	(:action UNSTACK_D_D
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_D )
			( ON_D_D )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_D )
			(not ( HANDEMPTY ))
			(not ( ON_D_D ))
		)
	)
	(:action STACK_C_I
		:parameters ()
		:precondition
		(and
			( CLEAR_I )
			( HOLDING_C )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_C )
			( HANDEMPTY )
			( ON_C_I )
			(not ( HOLDING_C ))
			(not ( CLEAR_I ))
		)
	)
	(:action STACK_F_I
		:parameters ()
		:precondition
		(and
			( CLEAR_I )
			( HOLDING_F )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_F )
			( HANDEMPTY )
			( ON_F_I )
			(not ( HOLDING_F ))
			(not ( CLEAR_I ))
		)
	)
	(:action STACK_I_C
		:parameters ()
		:precondition
		(and
			( CLEAR_C )
			( HOLDING_I )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_I )
			( HANDEMPTY )
			( ON_I_C )
			(not ( HOLDING_I ))
			(not ( CLEAR_C ))
		)
	)
	(:action STACK_I_F
		:parameters ()
		:precondition
		(and
			( CLEAR_F )
			( HOLDING_I )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_I )
			( HANDEMPTY )
			( ON_I_F )
			(not ( HOLDING_I ))
			(not ( CLEAR_F ))
		)
	)
	(:action STACK_I_I
		:parameters ()
		:precondition
		(and
			( CLEAR_I )
			( HOLDING_I )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HANDEMPTY )
			( ON_I_I )
			(not ( HOLDING_I ))
		)
	)
	(:action STACK_I_E
		:parameters ()
		:precondition
		(and
			( CLEAR_E )
			( HOLDING_I )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_I )
			( HANDEMPTY )
			( ON_I_E )
			(not ( HOLDING_I ))
			(not ( CLEAR_E ))
		)
	)
	(:action STACK_I_J
		:parameters ()
		:precondition
		(and
			( CLEAR_J )
			( HOLDING_I )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_I )
			( HANDEMPTY )
			( ON_I_J )
			(not ( HOLDING_I ))
			(not ( CLEAR_J ))
		)
	)
	(:action STACK_I_B
		:parameters ()
		:precondition
		(and
			( CLEAR_B )
			( HOLDING_I )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_I )
			( HANDEMPTY )
			( ON_I_B )
			(not ( HOLDING_I ))
			(not ( CLEAR_B ))
		)
	)
	(:action STACK_I_G
		:parameters ()
		:precondition
		(and
			( CLEAR_G )
			( HOLDING_I )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_I )
			( HANDEMPTY )
			( ON_I_G )
			(not ( HOLDING_I ))
			(not ( CLEAR_G ))
		)
	)
	(:action STACK_I_H
		:parameters ()
		:precondition
		(and
			( CLEAR_H )
			( HOLDING_I )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_I )
			( HANDEMPTY )
			( ON_I_H )
			(not ( HOLDING_I ))
			(not ( CLEAR_H ))
		)
	)
	(:action STACK_I_A
		:parameters ()
		:precondition
		(and
			( CLEAR_A )
			( HOLDING_I )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_I )
			( HANDEMPTY )
			( ON_I_A )
			(not ( HOLDING_I ))
			(not ( CLEAR_A ))
		)
	)
	(:action STACK_I_D
		:parameters ()
		:precondition
		(and
			( CLEAR_D )
			( HOLDING_I )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_I )
			( HANDEMPTY )
			( ON_I_D )
			(not ( HOLDING_I ))
			(not ( CLEAR_D ))
		)
	)
	(:action STACK_E_I
		:parameters ()
		:precondition
		(and
			( CLEAR_I )
			( HOLDING_E )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_E )
			( HANDEMPTY )
			( ON_E_I )
			(not ( HOLDING_E ))
			(not ( CLEAR_I ))
		)
	)
	(:action STACK_J_I
		:parameters ()
		:precondition
		(and
			( CLEAR_I )
			( HOLDING_J )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_J )
			( HANDEMPTY )
			( ON_J_I )
			(not ( HOLDING_J ))
			(not ( CLEAR_I ))
		)
	)
	(:action STACK_B_I
		:parameters ()
		:precondition
		(and
			( CLEAR_I )
			( HOLDING_B )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_B )
			( HANDEMPTY )
			( ON_B_I )
			(not ( HOLDING_B ))
			(not ( CLEAR_I ))
		)
	)
	(:action STACK_G_I
		:parameters ()
		:precondition
		(and
			( CLEAR_I )
			( HOLDING_G )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_G )
			( HANDEMPTY )
			( ON_G_I )
			(not ( HOLDING_G ))
			(not ( CLEAR_I ))
		)
	)
	(:action STACK_H_I
		:parameters ()
		:precondition
		(and
			( CLEAR_I )
			( HOLDING_H )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_H )
			( HANDEMPTY )
			( ON_H_I )
			(not ( HOLDING_H ))
			(not ( CLEAR_I ))
		)
	)
	(:action STACK_A_I
		:parameters ()
		:precondition
		(and
			( CLEAR_I )
			( HOLDING_A )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_A )
			( HANDEMPTY )
			( ON_A_I )
			(not ( HOLDING_A ))
			(not ( CLEAR_I ))
		)
	)
	(:action STACK_D_C
		:parameters ()
		:precondition
		(and
			( CLEAR_C )
			( HOLDING_D )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_D )
			( HANDEMPTY )
			( ON_D_C )
			(not ( HOLDING_D ))
			(not ( CLEAR_C ))
		)
	)
	(:action STACK_D_F
		:parameters ()
		:precondition
		(and
			( CLEAR_F )
			( HOLDING_D )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_D )
			( HANDEMPTY )
			( ON_D_F )
			(not ( HOLDING_D ))
			(not ( CLEAR_F ))
		)
	)
	(:action STACK_D_I
		:parameters ()
		:precondition
		(and
			( CLEAR_I )
			( HOLDING_D )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_D )
			( HANDEMPTY )
			( ON_D_I )
			(not ( HOLDING_D ))
			(not ( CLEAR_I ))
		)
	)
	(:action STACK_D_E
		:parameters ()
		:precondition
		(and
			( CLEAR_E )
			( HOLDING_D )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_D )
			( HANDEMPTY )
			( ON_D_E )
			(not ( HOLDING_D ))
			(not ( CLEAR_E ))
		)
	)
	(:action STACK_D_J
		:parameters ()
		:precondition
		(and
			( CLEAR_J )
			( HOLDING_D )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_D )
			( HANDEMPTY )
			( ON_D_J )
			(not ( HOLDING_D ))
			(not ( CLEAR_J ))
		)
	)
	(:action STACK_D_B
		:parameters ()
		:precondition
		(and
			( CLEAR_B )
			( HOLDING_D )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_D )
			( HANDEMPTY )
			( ON_D_B )
			(not ( HOLDING_D ))
			(not ( CLEAR_B ))
		)
	)
	(:action STACK_D_G
		:parameters ()
		:precondition
		(and
			( CLEAR_G )
			( HOLDING_D )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_D )
			( HANDEMPTY )
			( ON_D_G )
			(not ( HOLDING_D ))
			(not ( CLEAR_G ))
		)
	)
	(:action STACK_D_H
		:parameters ()
		:precondition
		(and
			( CLEAR_H )
			( HOLDING_D )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_D )
			( HANDEMPTY )
			( ON_D_H )
			(not ( HOLDING_D ))
			(not ( CLEAR_H ))
		)
	)
	(:action STACK_D_A
		:parameters ()
		:precondition
		(and
			( CLEAR_A )
			( HOLDING_D )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_D )
			( HANDEMPTY )
			( ON_D_A )
			(not ( HOLDING_D ))
			(not ( CLEAR_A ))
		)
	)
	(:action STACK_D_D
		:parameters ()
		:precondition
		(and
			( CLEAR_D )
			( HOLDING_D )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HANDEMPTY )
			( ON_D_D )
			(not ( HOLDING_D ))
		)
	)
	(:action PUT-DOWN_I
		:parameters ()
		:precondition
		(and
			( HOLDING_I )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_I )
			( HANDEMPTY )
			( ONTABLE_I )
			(not ( HOLDING_I ))
		)
	)
	(:action PUT-DOWN_D
		:parameters ()
		:precondition
		(and
			( HOLDING_D )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_D )
			( HANDEMPTY )
			( ONTABLE_D )
			(not ( HOLDING_D ))
		)
	)
	(:action PICK-UP_I
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( ONTABLE_I )
			( CLEAR_I )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_I )
			(not ( ONTABLE_I ))
			(not ( CLEAR_I ))
			(not ( HANDEMPTY ))
		)
	)
	(:action PICK-UP_A
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( ONTABLE_A )
			( CLEAR_A )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_A )
			(not ( ONTABLE_A ))
			(not ( CLEAR_A ))
			(not ( HANDEMPTY ))
		)
	)
	(:action UNSTACK_C_D
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_C )
			( ON_C_D )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_C )
			( CLEAR_D )
			(not ( CLEAR_C ))
			(not ( HANDEMPTY ))
			(not ( ON_C_D ))
		)
	)
	(:action UNSTACK_F_D
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_F )
			( ON_F_D )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_F )
			( CLEAR_D )
			(not ( CLEAR_F ))
			(not ( HANDEMPTY ))
			(not ( ON_F_D ))
		)
	)
	(:action UNSTACK_E_D
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_E )
			( ON_E_D )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_E )
			( CLEAR_D )
			(not ( CLEAR_E ))
			(not ( HANDEMPTY ))
			(not ( ON_E_D ))
		)
	)
	(:action UNSTACK_J_D
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_J )
			( ON_J_D )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_J )
			( CLEAR_D )
			(not ( CLEAR_J ))
			(not ( HANDEMPTY ))
			(not ( ON_J_D ))
		)
	)
	(:action UNSTACK_B_D
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_B )
			( ON_B_D )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_B )
			( CLEAR_D )
			(not ( CLEAR_B ))
			(not ( HANDEMPTY ))
			(not ( ON_B_D ))
		)
	)
	(:action UNSTACK_G_D
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_G )
			( ON_G_D )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_G )
			( CLEAR_D )
			(not ( CLEAR_G ))
			(not ( HANDEMPTY ))
			(not ( ON_G_D ))
		)
	)
	(:action UNSTACK_H_D
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_H )
			( ON_H_D )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_H )
			( CLEAR_D )
			(not ( CLEAR_H ))
			(not ( HANDEMPTY ))
			(not ( ON_H_D ))
		)
	)
	(:action UNSTACK_A_C
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_A )
			( ON_A_C )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_A )
			( CLEAR_C )
			(not ( CLEAR_A ))
			(not ( HANDEMPTY ))
			(not ( ON_A_C ))
		)
	)
	(:action UNSTACK_A_F
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_A )
			( ON_A_F )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_A )
			( CLEAR_F )
			(not ( CLEAR_A ))
			(not ( HANDEMPTY ))
			(not ( ON_A_F ))
		)
	)
	(:action UNSTACK_A_E
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_A )
			( ON_A_E )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_A )
			( CLEAR_E )
			(not ( CLEAR_A ))
			(not ( HANDEMPTY ))
			(not ( ON_A_E ))
		)
	)
	(:action UNSTACK_A_J
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_A )
			( ON_A_J )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_A )
			( CLEAR_J )
			(not ( CLEAR_A ))
			(not ( HANDEMPTY ))
			(not ( ON_A_J ))
		)
	)
	(:action UNSTACK_A_B
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_A )
			( ON_A_B )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_A )
			( CLEAR_B )
			(not ( CLEAR_A ))
			(not ( HANDEMPTY ))
			(not ( ON_A_B ))
		)
	)
	(:action UNSTACK_A_G
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_A )
			( ON_A_G )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_A )
			( CLEAR_G )
			(not ( CLEAR_A ))
			(not ( HANDEMPTY ))
			(not ( ON_A_G ))
		)
	)
	(:action UNSTACK_A_H
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_A )
			( ON_A_H )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_A )
			( CLEAR_H )
			(not ( CLEAR_A ))
			(not ( HANDEMPTY ))
			(not ( ON_A_H ))
		)
	)
	(:action UNSTACK_A_A
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_A )
			( ON_A_A )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_A )
			(not ( HANDEMPTY ))
			(not ( ON_A_A ))
		)
	)
	(:action UNSTACK_D_I
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_D )
			( ON_D_I )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_D )
			( CLEAR_I )
			(not ( CLEAR_D ))
			(not ( HANDEMPTY ))
			(not ( ON_D_I ))
		)
	)
	(:action STACK_C_D
		:parameters ()
		:precondition
		(and
			( CLEAR_D )
			( HOLDING_C )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_C )
			( HANDEMPTY )
			( ON_C_D )
			(not ( HOLDING_C ))
			(not ( CLEAR_D ))
		)
	)
	(:action STACK_F_D
		:parameters ()
		:precondition
		(and
			( CLEAR_D )
			( HOLDING_F )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_F )
			( HANDEMPTY )
			( ON_F_D )
			(not ( HOLDING_F ))
			(not ( CLEAR_D ))
		)
	)
	(:action STACK_E_D
		:parameters ()
		:precondition
		(and
			( CLEAR_D )
			( HOLDING_E )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_E )
			( HANDEMPTY )
			( ON_E_D )
			(not ( HOLDING_E ))
			(not ( CLEAR_D ))
		)
	)
	(:action STACK_J_D
		:parameters ()
		:precondition
		(and
			( CLEAR_D )
			( HOLDING_J )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_J )
			( HANDEMPTY )
			( ON_J_D )
			(not ( HOLDING_J ))
			(not ( CLEAR_D ))
		)
	)
	(:action STACK_B_D
		:parameters ()
		:precondition
		(and
			( CLEAR_D )
			( HOLDING_B )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_B )
			( HANDEMPTY )
			( ON_B_D )
			(not ( HOLDING_B ))
			(not ( CLEAR_D ))
		)
	)
	(:action STACK_G_D
		:parameters ()
		:precondition
		(and
			( CLEAR_D )
			( HOLDING_G )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_G )
			( HANDEMPTY )
			( ON_G_D )
			(not ( HOLDING_G ))
			(not ( CLEAR_D ))
		)
	)
	(:action STACK_H_D
		:parameters ()
		:precondition
		(and
			( CLEAR_D )
			( HOLDING_H )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_H )
			( HANDEMPTY )
			( ON_H_D )
			(not ( HOLDING_H ))
			(not ( CLEAR_D ))
		)
	)
	(:action STACK_A_C
		:parameters ()
		:precondition
		(and
			( CLEAR_C )
			( HOLDING_A )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_A )
			( HANDEMPTY )
			( ON_A_C )
			(not ( HOLDING_A ))
			(not ( CLEAR_C ))
		)
	)
	(:action STACK_A_F
		:parameters ()
		:precondition
		(and
			( CLEAR_F )
			( HOLDING_A )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_A )
			( HANDEMPTY )
			( ON_A_F )
			(not ( HOLDING_A ))
			(not ( CLEAR_F ))
		)
	)
	(:action STACK_A_E
		:parameters ()
		:precondition
		(and
			( CLEAR_E )
			( HOLDING_A )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_A )
			( HANDEMPTY )
			( ON_A_E )
			(not ( HOLDING_A ))
			(not ( CLEAR_E ))
		)
	)
	(:action STACK_A_J
		:parameters ()
		:precondition
		(and
			( CLEAR_J )
			( HOLDING_A )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_A )
			( HANDEMPTY )
			( ON_A_J )
			(not ( HOLDING_A ))
			(not ( CLEAR_J ))
		)
	)
	(:action STACK_A_B
		:parameters ()
		:precondition
		(and
			( CLEAR_B )
			( HOLDING_A )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_A )
			( HANDEMPTY )
			( ON_A_B )
			(not ( HOLDING_A ))
			(not ( CLEAR_B ))
		)
	)
	(:action STACK_A_G
		:parameters ()
		:precondition
		(and
			( CLEAR_G )
			( HOLDING_A )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_A )
			( HANDEMPTY )
			( ON_A_G )
			(not ( HOLDING_A ))
			(not ( CLEAR_G ))
		)
	)
	(:action STACK_A_H
		:parameters ()
		:precondition
		(and
			( CLEAR_H )
			( HOLDING_A )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_A )
			( HANDEMPTY )
			( ON_A_H )
			(not ( HOLDING_A ))
			(not ( CLEAR_H ))
		)
	)
	(:action STACK_A_A
		:parameters ()
		:precondition
		(and
			( CLEAR_A )
			( HOLDING_A )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HANDEMPTY )
			( ON_A_A )
			(not ( HOLDING_A ))
		)
	)
	(:action STACK_A_D
		:parameters ()
		:precondition
		(and
			( CLEAR_D )
			( HOLDING_A )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_A )
			( HANDEMPTY )
			( ON_A_D )
			(not ( HOLDING_A ))
			(not ( CLEAR_D ))
		)
	)
	(:action PUT-DOWN_A
		:parameters ()
		:precondition
		(and
			( HOLDING_A )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_A )
			( HANDEMPTY )
			( ONTABLE_A )
			(not ( HOLDING_A ))
		)
	)
	(:action PICK-UP_H
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( ONTABLE_H )
			( CLEAR_H )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_H )
			(not ( ONTABLE_H ))
			(not ( CLEAR_H ))
			(not ( HANDEMPTY ))
		)
	)
	(:action UNSTACK_C_A
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_C )
			( ON_C_A )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_C )
			( CLEAR_A )
			(not ( CLEAR_C ))
			(not ( HANDEMPTY ))
			(not ( ON_C_A ))
		)
	)
	(:action UNSTACK_F_A
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_F )
			( ON_F_A )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_F )
			( CLEAR_A )
			(not ( CLEAR_F ))
			(not ( HANDEMPTY ))
			(not ( ON_F_A ))
		)
	)
	(:action UNSTACK_E_A
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_E )
			( ON_E_A )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_E )
			( CLEAR_A )
			(not ( CLEAR_E ))
			(not ( HANDEMPTY ))
			(not ( ON_E_A ))
		)
	)
	(:action UNSTACK_J_A
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_J )
			( ON_J_A )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_J )
			( CLEAR_A )
			(not ( CLEAR_J ))
			(not ( HANDEMPTY ))
			(not ( ON_J_A ))
		)
	)
	(:action UNSTACK_B_A
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_B )
			( ON_B_A )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_B )
			( CLEAR_A )
			(not ( CLEAR_B ))
			(not ( HANDEMPTY ))
			(not ( ON_B_A ))
		)
	)
	(:action UNSTACK_G_A
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_G )
			( ON_G_A )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_G )
			( CLEAR_A )
			(not ( CLEAR_G ))
			(not ( HANDEMPTY ))
			(not ( ON_G_A ))
		)
	)
	(:action UNSTACK_H_C
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_H )
			( ON_H_C )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_H )
			( CLEAR_C )
			(not ( CLEAR_H ))
			(not ( HANDEMPTY ))
			(not ( ON_H_C ))
		)
	)
	(:action UNSTACK_H_F
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_H )
			( ON_H_F )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_H )
			( CLEAR_F )
			(not ( CLEAR_H ))
			(not ( HANDEMPTY ))
			(not ( ON_H_F ))
		)
	)
	(:action UNSTACK_H_E
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_H )
			( ON_H_E )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_H )
			( CLEAR_E )
			(not ( CLEAR_H ))
			(not ( HANDEMPTY ))
			(not ( ON_H_E ))
		)
	)
	(:action UNSTACK_H_J
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_H )
			( ON_H_J )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_H )
			( CLEAR_J )
			(not ( CLEAR_H ))
			(not ( HANDEMPTY ))
			(not ( ON_H_J ))
		)
	)
	(:action UNSTACK_H_B
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_H )
			( ON_H_B )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_H )
			( CLEAR_B )
			(not ( CLEAR_H ))
			(not ( HANDEMPTY ))
			(not ( ON_H_B ))
		)
	)
	(:action UNSTACK_H_G
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_H )
			( ON_H_G )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_H )
			( CLEAR_G )
			(not ( CLEAR_H ))
			(not ( HANDEMPTY ))
			(not ( ON_H_G ))
		)
	)
	(:action UNSTACK_H_H
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_H )
			( ON_H_H )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_H )
			(not ( HANDEMPTY ))
			(not ( ON_H_H ))
		)
	)
	(:action UNSTACK_A_D
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_A )
			( ON_A_D )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_A )
			( CLEAR_D )
			(not ( CLEAR_A ))
			(not ( HANDEMPTY ))
			(not ( ON_A_D ))
		)
	)
	(:action STACK_C_A
		:parameters ()
		:precondition
		(and
			( CLEAR_A )
			( HOLDING_C )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_C )
			( HANDEMPTY )
			( ON_C_A )
			(not ( HOLDING_C ))
			(not ( CLEAR_A ))
		)
	)
	(:action STACK_F_A
		:parameters ()
		:precondition
		(and
			( CLEAR_A )
			( HOLDING_F )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_F )
			( HANDEMPTY )
			( ON_F_A )
			(not ( HOLDING_F ))
			(not ( CLEAR_A ))
		)
	)
	(:action STACK_E_A
		:parameters ()
		:precondition
		(and
			( CLEAR_A )
			( HOLDING_E )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_E )
			( HANDEMPTY )
			( ON_E_A )
			(not ( HOLDING_E ))
			(not ( CLEAR_A ))
		)
	)
	(:action STACK_J_A
		:parameters ()
		:precondition
		(and
			( CLEAR_A )
			( HOLDING_J )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_J )
			( HANDEMPTY )
			( ON_J_A )
			(not ( HOLDING_J ))
			(not ( CLEAR_A ))
		)
	)
	(:action STACK_B_A
		:parameters ()
		:precondition
		(and
			( CLEAR_A )
			( HOLDING_B )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_B )
			( HANDEMPTY )
			( ON_B_A )
			(not ( HOLDING_B ))
			(not ( CLEAR_A ))
		)
	)
	(:action STACK_G_A
		:parameters ()
		:precondition
		(and
			( CLEAR_A )
			( HOLDING_G )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_G )
			( HANDEMPTY )
			( ON_G_A )
			(not ( HOLDING_G ))
			(not ( CLEAR_A ))
		)
	)
	(:action STACK_H_C
		:parameters ()
		:precondition
		(and
			( CLEAR_C )
			( HOLDING_H )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_H )
			( HANDEMPTY )
			( ON_H_C )
			(not ( HOLDING_H ))
			(not ( CLEAR_C ))
		)
	)
	(:action STACK_H_F
		:parameters ()
		:precondition
		(and
			( CLEAR_F )
			( HOLDING_H )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_H )
			( HANDEMPTY )
			( ON_H_F )
			(not ( HOLDING_H ))
			(not ( CLEAR_F ))
		)
	)
	(:action STACK_H_E
		:parameters ()
		:precondition
		(and
			( CLEAR_E )
			( HOLDING_H )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_H )
			( HANDEMPTY )
			( ON_H_E )
			(not ( HOLDING_H ))
			(not ( CLEAR_E ))
		)
	)
	(:action STACK_H_J
		:parameters ()
		:precondition
		(and
			( CLEAR_J )
			( HOLDING_H )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_H )
			( HANDEMPTY )
			( ON_H_J )
			(not ( HOLDING_H ))
			(not ( CLEAR_J ))
		)
	)
	(:action STACK_H_B
		:parameters ()
		:precondition
		(and
			( CLEAR_B )
			( HOLDING_H )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_H )
			( HANDEMPTY )
			( ON_H_B )
			(not ( HOLDING_H ))
			(not ( CLEAR_B ))
		)
	)
	(:action STACK_H_G
		:parameters ()
		:precondition
		(and
			( CLEAR_G )
			( HOLDING_H )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_H )
			( HANDEMPTY )
			( ON_H_G )
			(not ( HOLDING_H ))
			(not ( CLEAR_G ))
		)
	)
	(:action STACK_H_H
		:parameters ()
		:precondition
		(and
			( CLEAR_H )
			( HOLDING_H )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HANDEMPTY )
			( ON_H_H )
			(not ( HOLDING_H ))
		)
	)
	(:action STACK_H_A
		:parameters ()
		:precondition
		(and
			( CLEAR_A )
			( HOLDING_H )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_H )
			( HANDEMPTY )
			( ON_H_A )
			(not ( HOLDING_H ))
			(not ( CLEAR_A ))
		)
	)
	(:action PUT-DOWN_H
		:parameters ()
		:precondition
		(and
			( HOLDING_H )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_H )
			( HANDEMPTY )
			( ONTABLE_H )
			(not ( HOLDING_H ))
		)
	)
	(:action PICK-UP_G
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( ONTABLE_G )
			( CLEAR_G )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_G )
			(not ( ONTABLE_G ))
			(not ( CLEAR_G ))
			(not ( HANDEMPTY ))
		)
	)
	(:action UNSTACK_C_H
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_C )
			( ON_C_H )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_C )
			( CLEAR_H )
			(not ( CLEAR_C ))
			(not ( HANDEMPTY ))
			(not ( ON_C_H ))
		)
	)
	(:action UNSTACK_F_H
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_F )
			( ON_F_H )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_F )
			( CLEAR_H )
			(not ( CLEAR_F ))
			(not ( HANDEMPTY ))
			(not ( ON_F_H ))
		)
	)
	(:action UNSTACK_E_H
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_E )
			( ON_E_H )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_E )
			( CLEAR_H )
			(not ( CLEAR_E ))
			(not ( HANDEMPTY ))
			(not ( ON_E_H ))
		)
	)
	(:action UNSTACK_J_H
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_J )
			( ON_J_H )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_J )
			( CLEAR_H )
			(not ( CLEAR_J ))
			(not ( HANDEMPTY ))
			(not ( ON_J_H ))
		)
	)
	(:action UNSTACK_B_H
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_B )
			( ON_B_H )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_B )
			( CLEAR_H )
			(not ( CLEAR_B ))
			(not ( HANDEMPTY ))
			(not ( ON_B_H ))
		)
	)
	(:action UNSTACK_G_C
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_G )
			( ON_G_C )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_G )
			( CLEAR_C )
			(not ( CLEAR_G ))
			(not ( HANDEMPTY ))
			(not ( ON_G_C ))
		)
	)
	(:action UNSTACK_G_F
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_G )
			( ON_G_F )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_G )
			( CLEAR_F )
			(not ( CLEAR_G ))
			(not ( HANDEMPTY ))
			(not ( ON_G_F ))
		)
	)
	(:action UNSTACK_G_E
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_G )
			( ON_G_E )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_G )
			( CLEAR_E )
			(not ( CLEAR_G ))
			(not ( HANDEMPTY ))
			(not ( ON_G_E ))
		)
	)
	(:action UNSTACK_G_J
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_G )
			( ON_G_J )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_G )
			( CLEAR_J )
			(not ( CLEAR_G ))
			(not ( HANDEMPTY ))
			(not ( ON_G_J ))
		)
	)
	(:action UNSTACK_G_B
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_G )
			( ON_G_B )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_G )
			( CLEAR_B )
			(not ( CLEAR_G ))
			(not ( HANDEMPTY ))
			(not ( ON_G_B ))
		)
	)
	(:action UNSTACK_G_G
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_G )
			( ON_G_G )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_G )
			(not ( HANDEMPTY ))
			(not ( ON_G_G ))
		)
	)
	(:action UNSTACK_H_A
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_H )
			( ON_H_A )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_H )
			( CLEAR_A )
			(not ( CLEAR_H ))
			(not ( HANDEMPTY ))
			(not ( ON_H_A ))
		)
	)
	(:action STACK_C_H
		:parameters ()
		:precondition
		(and
			( CLEAR_H )
			( HOLDING_C )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_C )
			( HANDEMPTY )
			( ON_C_H )
			(not ( HOLDING_C ))
			(not ( CLEAR_H ))
		)
	)
	(:action STACK_F_H
		:parameters ()
		:precondition
		(and
			( CLEAR_H )
			( HOLDING_F )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_F )
			( HANDEMPTY )
			( ON_F_H )
			(not ( HOLDING_F ))
			(not ( CLEAR_H ))
		)
	)
	(:action STACK_E_H
		:parameters ()
		:precondition
		(and
			( CLEAR_H )
			( HOLDING_E )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_E )
			( HANDEMPTY )
			( ON_E_H )
			(not ( HOLDING_E ))
			(not ( CLEAR_H ))
		)
	)
	(:action STACK_J_H
		:parameters ()
		:precondition
		(and
			( CLEAR_H )
			( HOLDING_J )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_J )
			( HANDEMPTY )
			( ON_J_H )
			(not ( HOLDING_J ))
			(not ( CLEAR_H ))
		)
	)
	(:action STACK_B_H
		:parameters ()
		:precondition
		(and
			( CLEAR_H )
			( HOLDING_B )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_B )
			( HANDEMPTY )
			( ON_B_H )
			(not ( HOLDING_B ))
			(not ( CLEAR_H ))
		)
	)
	(:action STACK_G_C
		:parameters ()
		:precondition
		(and
			( CLEAR_C )
			( HOLDING_G )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_G )
			( HANDEMPTY )
			( ON_G_C )
			(not ( HOLDING_G ))
			(not ( CLEAR_C ))
		)
	)
	(:action STACK_G_F
		:parameters ()
		:precondition
		(and
			( CLEAR_F )
			( HOLDING_G )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_G )
			( HANDEMPTY )
			( ON_G_F )
			(not ( HOLDING_G ))
			(not ( CLEAR_F ))
		)
	)
	(:action STACK_G_E
		:parameters ()
		:precondition
		(and
			( CLEAR_E )
			( HOLDING_G )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_G )
			( HANDEMPTY )
			( ON_G_E )
			(not ( HOLDING_G ))
			(not ( CLEAR_E ))
		)
	)
	(:action STACK_G_J
		:parameters ()
		:precondition
		(and
			( CLEAR_J )
			( HOLDING_G )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_G )
			( HANDEMPTY )
			( ON_G_J )
			(not ( HOLDING_G ))
			(not ( CLEAR_J ))
		)
	)
	(:action STACK_G_B
		:parameters ()
		:precondition
		(and
			( CLEAR_B )
			( HOLDING_G )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_G )
			( HANDEMPTY )
			( ON_G_B )
			(not ( HOLDING_G ))
			(not ( CLEAR_B ))
		)
	)
	(:action STACK_G_G
		:parameters ()
		:precondition
		(and
			( CLEAR_G )
			( HOLDING_G )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HANDEMPTY )
			( ON_G_G )
			(not ( HOLDING_G ))
		)
	)
	(:action STACK_G_H
		:parameters ()
		:precondition
		(and
			( CLEAR_H )
			( HOLDING_G )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_G )
			( HANDEMPTY )
			( ON_G_H )
			(not ( HOLDING_G ))
			(not ( CLEAR_H ))
		)
	)
	(:action PUT-DOWN_G
		:parameters ()
		:precondition
		(and
			( HOLDING_G )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_G )
			( HANDEMPTY )
			( ONTABLE_G )
			(not ( HOLDING_G ))
		)
	)
	(:action PICK-UP_B
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( ONTABLE_B )
			( CLEAR_B )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_B )
			(not ( ONTABLE_B ))
			(not ( CLEAR_B ))
			(not ( HANDEMPTY ))
		)
	)
	(:action UNSTACK_C_G
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_C )
			( ON_C_G )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_C )
			( CLEAR_G )
			(not ( CLEAR_C ))
			(not ( HANDEMPTY ))
			(not ( ON_C_G ))
		)
	)
	(:action UNSTACK_F_G
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_F )
			( ON_F_G )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_F )
			( CLEAR_G )
			(not ( CLEAR_F ))
			(not ( HANDEMPTY ))
			(not ( ON_F_G ))
		)
	)
	(:action UNSTACK_E_G
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_E )
			( ON_E_G )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_E )
			( CLEAR_G )
			(not ( CLEAR_E ))
			(not ( HANDEMPTY ))
			(not ( ON_E_G ))
		)
	)
	(:action UNSTACK_J_G
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_J )
			( ON_J_G )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_J )
			( CLEAR_G )
			(not ( CLEAR_J ))
			(not ( HANDEMPTY ))
			(not ( ON_J_G ))
		)
	)
	(:action UNSTACK_B_C
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_B )
			( ON_B_C )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_B )
			( CLEAR_C )
			(not ( CLEAR_B ))
			(not ( HANDEMPTY ))
			(not ( ON_B_C ))
		)
	)
	(:action UNSTACK_B_F
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_B )
			( ON_B_F )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_B )
			( CLEAR_F )
			(not ( CLEAR_B ))
			(not ( HANDEMPTY ))
			(not ( ON_B_F ))
		)
	)
	(:action UNSTACK_B_E
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_B )
			( ON_B_E )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_B )
			( CLEAR_E )
			(not ( CLEAR_B ))
			(not ( HANDEMPTY ))
			(not ( ON_B_E ))
		)
	)
	(:action UNSTACK_B_J
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_B )
			( ON_B_J )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_B )
			( CLEAR_J )
			(not ( CLEAR_B ))
			(not ( HANDEMPTY ))
			(not ( ON_B_J ))
		)
	)
	(:action UNSTACK_B_B
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_B )
			( ON_B_B )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_B )
			(not ( HANDEMPTY ))
			(not ( ON_B_B ))
		)
	)
	(:action UNSTACK_G_H
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_G )
			( ON_G_H )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_G )
			( CLEAR_H )
			(not ( CLEAR_G ))
			(not ( HANDEMPTY ))
			(not ( ON_G_H ))
		)
	)
	(:action STACK_C_G
		:parameters ()
		:precondition
		(and
			( CLEAR_G )
			( HOLDING_C )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_C )
			( HANDEMPTY )
			( ON_C_G )
			(not ( HOLDING_C ))
			(not ( CLEAR_G ))
		)
	)
	(:action STACK_F_G
		:parameters ()
		:precondition
		(and
			( CLEAR_G )
			( HOLDING_F )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_F )
			( HANDEMPTY )
			( ON_F_G )
			(not ( HOLDING_F ))
			(not ( CLEAR_G ))
		)
	)
	(:action STACK_E_G
		:parameters ()
		:precondition
		(and
			( CLEAR_G )
			( HOLDING_E )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_E )
			( HANDEMPTY )
			( ON_E_G )
			(not ( HOLDING_E ))
			(not ( CLEAR_G ))
		)
	)
	(:action STACK_J_G
		:parameters ()
		:precondition
		(and
			( CLEAR_G )
			( HOLDING_J )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_J )
			( HANDEMPTY )
			( ON_J_G )
			(not ( HOLDING_J ))
			(not ( CLEAR_G ))
		)
	)
	(:action STACK_B_C
		:parameters ()
		:precondition
		(and
			( CLEAR_C )
			( HOLDING_B )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_B )
			( HANDEMPTY )
			( ON_B_C )
			(not ( HOLDING_B ))
			(not ( CLEAR_C ))
		)
	)
	(:action STACK_B_F
		:parameters ()
		:precondition
		(and
			( CLEAR_F )
			( HOLDING_B )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_B )
			( HANDEMPTY )
			( ON_B_F )
			(not ( HOLDING_B ))
			(not ( CLEAR_F ))
		)
	)
	(:action STACK_B_E
		:parameters ()
		:precondition
		(and
			( CLEAR_E )
			( HOLDING_B )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_B )
			( HANDEMPTY )
			( ON_B_E )
			(not ( HOLDING_B ))
			(not ( CLEAR_E ))
		)
	)
	(:action STACK_B_J
		:parameters ()
		:precondition
		(and
			( CLEAR_J )
			( HOLDING_B )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_B )
			( HANDEMPTY )
			( ON_B_J )
			(not ( HOLDING_B ))
			(not ( CLEAR_J ))
		)
	)
	(:action STACK_B_B
		:parameters ()
		:precondition
		(and
			( CLEAR_B )
			( HOLDING_B )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HANDEMPTY )
			( ON_B_B )
			(not ( HOLDING_B ))
		)
	)
	(:action STACK_B_G
		:parameters ()
		:precondition
		(and
			( CLEAR_G )
			( HOLDING_B )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_B )
			( HANDEMPTY )
			( ON_B_G )
			(not ( HOLDING_B ))
			(not ( CLEAR_G ))
		)
	)
	(:action PUT-DOWN_B
		:parameters ()
		:precondition
		(and
			( HOLDING_B )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_B )
			( HANDEMPTY )
			( ONTABLE_B )
			(not ( HOLDING_B ))
		)
	)
	(:action PICK-UP_J
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( ONTABLE_J )
			( CLEAR_J )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_J )
			(not ( ONTABLE_J ))
			(not ( CLEAR_J ))
			(not ( HANDEMPTY ))
		)
	)
	(:action UNSTACK_C_B
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_C )
			( ON_C_B )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_C )
			( CLEAR_B )
			(not ( CLEAR_C ))
			(not ( HANDEMPTY ))
			(not ( ON_C_B ))
		)
	)
	(:action UNSTACK_F_B
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_F )
			( ON_F_B )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_F )
			( CLEAR_B )
			(not ( CLEAR_F ))
			(not ( HANDEMPTY ))
			(not ( ON_F_B ))
		)
	)
	(:action UNSTACK_E_B
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_E )
			( ON_E_B )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_E )
			( CLEAR_B )
			(not ( CLEAR_E ))
			(not ( HANDEMPTY ))
			(not ( ON_E_B ))
		)
	)
	(:action UNSTACK_J_C
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_J )
			( ON_J_C )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_J )
			( CLEAR_C )
			(not ( CLEAR_J ))
			(not ( HANDEMPTY ))
			(not ( ON_J_C ))
		)
	)
	(:action UNSTACK_J_F
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_J )
			( ON_J_F )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_J )
			( CLEAR_F )
			(not ( CLEAR_J ))
			(not ( HANDEMPTY ))
			(not ( ON_J_F ))
		)
	)
	(:action UNSTACK_J_E
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_J )
			( ON_J_E )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_J )
			( CLEAR_E )
			(not ( CLEAR_J ))
			(not ( HANDEMPTY ))
			(not ( ON_J_E ))
		)
	)
	(:action UNSTACK_J_J
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_J )
			( ON_J_J )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_J )
			(not ( HANDEMPTY ))
			(not ( ON_J_J ))
		)
	)
	(:action UNSTACK_B_G
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_B )
			( ON_B_G )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_B )
			( CLEAR_G )
			(not ( CLEAR_B ))
			(not ( HANDEMPTY ))
			(not ( ON_B_G ))
		)
	)
	(:action STACK_C_B
		:parameters ()
		:precondition
		(and
			( CLEAR_B )
			( HOLDING_C )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_C )
			( HANDEMPTY )
			( ON_C_B )
			(not ( HOLDING_C ))
			(not ( CLEAR_B ))
		)
	)
	(:action STACK_F_B
		:parameters ()
		:precondition
		(and
			( CLEAR_B )
			( HOLDING_F )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_F )
			( HANDEMPTY )
			( ON_F_B )
			(not ( HOLDING_F ))
			(not ( CLEAR_B ))
		)
	)
	(:action STACK_E_B
		:parameters ()
		:precondition
		(and
			( CLEAR_B )
			( HOLDING_E )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_E )
			( HANDEMPTY )
			( ON_E_B )
			(not ( HOLDING_E ))
			(not ( CLEAR_B ))
		)
	)
	(:action STACK_J_C
		:parameters ()
		:precondition
		(and
			( CLEAR_C )
			( HOLDING_J )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_J )
			( HANDEMPTY )
			( ON_J_C )
			(not ( HOLDING_J ))
			(not ( CLEAR_C ))
		)
	)
	(:action STACK_J_F
		:parameters ()
		:precondition
		(and
			( CLEAR_F )
			( HOLDING_J )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_J )
			( HANDEMPTY )
			( ON_J_F )
			(not ( HOLDING_J ))
			(not ( CLEAR_F ))
		)
	)
	(:action STACK_J_E
		:parameters ()
		:precondition
		(and
			( CLEAR_E )
			( HOLDING_J )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_J )
			( HANDEMPTY )
			( ON_J_E )
			(not ( HOLDING_J ))
			(not ( CLEAR_E ))
		)
	)
	(:action STACK_J_J
		:parameters ()
		:precondition
		(and
			( CLEAR_J )
			( HOLDING_J )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HANDEMPTY )
			( ON_J_J )
			(not ( HOLDING_J ))
		)
	)
	(:action STACK_J_B
		:parameters ()
		:precondition
		(and
			( CLEAR_B )
			( HOLDING_J )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_J )
			( HANDEMPTY )
			( ON_J_B )
			(not ( HOLDING_J ))
			(not ( CLEAR_B ))
		)
	)
	(:action PUT-DOWN_J
		:parameters ()
		:precondition
		(and
			( HOLDING_J )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_J )
			( HANDEMPTY )
			( ONTABLE_J )
			(not ( HOLDING_J ))
		)
	)
	(:action PICK-UP_E
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( ONTABLE_E )
			( CLEAR_E )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_E )
			(not ( ONTABLE_E ))
			(not ( CLEAR_E ))
			(not ( HANDEMPTY ))
		)
	)
	(:action UNSTACK_C_J
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_C )
			( ON_C_J )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_C )
			( CLEAR_J )
			(not ( CLEAR_C ))
			(not ( HANDEMPTY ))
			(not ( ON_C_J ))
		)
	)
	(:action UNSTACK_F_J
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_F )
			( ON_F_J )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_F )
			( CLEAR_J )
			(not ( CLEAR_F ))
			(not ( HANDEMPTY ))
			(not ( ON_F_J ))
		)
	)
	(:action UNSTACK_E_C
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_E )
			( ON_E_C )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_E )
			( CLEAR_C )
			(not ( CLEAR_E ))
			(not ( HANDEMPTY ))
			(not ( ON_E_C ))
		)
	)
	(:action UNSTACK_E_F
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_E )
			( ON_E_F )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_E )
			( CLEAR_F )
			(not ( CLEAR_E ))
			(not ( HANDEMPTY ))
			(not ( ON_E_F ))
		)
	)
	(:action UNSTACK_E_E
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_E )
			( ON_E_E )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_E )
			(not ( HANDEMPTY ))
			(not ( ON_E_E ))
		)
	)
	(:action UNSTACK_J_B
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_J )
			( ON_J_B )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_J )
			( CLEAR_B )
			(not ( CLEAR_J ))
			(not ( HANDEMPTY ))
			(not ( ON_J_B ))
		)
	)
	(:action STACK_C_J
		:parameters ()
		:precondition
		(and
			( CLEAR_J )
			( HOLDING_C )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_C )
			( HANDEMPTY )
			( ON_C_J )
			(not ( HOLDING_C ))
			(not ( CLEAR_J ))
		)
	)
	(:action STACK_F_J
		:parameters ()
		:precondition
		(and
			( CLEAR_J )
			( HOLDING_F )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_F )
			( HANDEMPTY )
			( ON_F_J )
			(not ( HOLDING_F ))
			(not ( CLEAR_J ))
		)
	)
	(:action STACK_E_C
		:parameters ()
		:precondition
		(and
			( CLEAR_C )
			( HOLDING_E )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_E )
			( HANDEMPTY )
			( ON_E_C )
			(not ( HOLDING_E ))
			(not ( CLEAR_C ))
		)
	)
	(:action STACK_E_F
		:parameters ()
		:precondition
		(and
			( CLEAR_F )
			( HOLDING_E )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_E )
			( HANDEMPTY )
			( ON_E_F )
			(not ( HOLDING_E ))
			(not ( CLEAR_F ))
		)
	)
	(:action STACK_E_E
		:parameters ()
		:precondition
		(and
			( CLEAR_E )
			( HOLDING_E )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HANDEMPTY )
			( ON_E_E )
			(not ( HOLDING_E ))
		)
	)
	(:action STACK_E_J
		:parameters ()
		:precondition
		(and
			( CLEAR_J )
			( HOLDING_E )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_E )
			( HANDEMPTY )
			( ON_E_J )
			(not ( HOLDING_E ))
			(not ( CLEAR_J ))
		)
	)
	(:action PUT-DOWN_E
		:parameters ()
		:precondition
		(and
			( HOLDING_E )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_E )
			( HANDEMPTY )
			( ONTABLE_E )
			(not ( HOLDING_E ))
		)
	)
	(:action PICK-UP_C
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( ONTABLE_C )
			( CLEAR_C )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_C )
			(not ( ONTABLE_C ))
			(not ( CLEAR_C ))
			(not ( HANDEMPTY ))
		)
	)
	(:action UNSTACK_C_C
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_C )
			( ON_C_C )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_C )
			(not ( HANDEMPTY ))
			(not ( ON_C_C ))
		)
	)
	(:action UNSTACK_C_F
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_C )
			( ON_C_F )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_C )
			( CLEAR_F )
			(not ( CLEAR_C ))
			(not ( HANDEMPTY ))
			(not ( ON_C_F ))
		)
	)
	(:action UNSTACK_F_E
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_F )
			( ON_F_E )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_F )
			( CLEAR_E )
			(not ( CLEAR_F ))
			(not ( HANDEMPTY ))
			(not ( ON_F_E ))
		)
	)
	(:action UNSTACK_E_J
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_E )
			( ON_E_J )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_E )
			( CLEAR_J )
			(not ( CLEAR_E ))
			(not ( HANDEMPTY ))
			(not ( ON_E_J ))
		)
	)
	(:action STACK_C_C
		:parameters ()
		:precondition
		(and
			( CLEAR_C )
			( HOLDING_C )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HANDEMPTY )
			( ON_C_C )
			(not ( HOLDING_C ))
		)
	)
	(:action STACK_C_F
		:parameters ()
		:precondition
		(and
			( CLEAR_F )
			( HOLDING_C )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_C )
			( HANDEMPTY )
			( ON_C_F )
			(not ( HOLDING_C ))
			(not ( CLEAR_F ))
		)
	)
	(:action STACK_C_E
		:parameters ()
		:precondition
		(and
			( CLEAR_E )
			( HOLDING_C )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_C )
			( HANDEMPTY )
			( ON_C_E )
			(not ( HOLDING_C ))
			(not ( CLEAR_E ))
		)
	)
	(:action STACK_F_E
		:parameters ()
		:precondition
		(and
			( CLEAR_E )
			( HOLDING_F )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_F )
			( HANDEMPTY )
			( ON_F_E )
			(not ( HOLDING_F ))
			(not ( CLEAR_E ))
		)
	)
	(:action PUT-DOWN_C
		:parameters ()
		:precondition
		(and
			( HOLDING_C )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_C )
			( HANDEMPTY )
			( ONTABLE_C )
			(not ( HOLDING_C ))
		)
	)
	(:action UNSTACK_C_E
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_C )
			( ON_C_E )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_C )
			( CLEAR_E )
			(not ( CLEAR_C ))
			(not ( HANDEMPTY ))
			(not ( ON_C_E ))
		)
	)
	(:action UNSTACK_F_C
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_F )
			( ON_F_C )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_F )
			( CLEAR_C )
			(not ( CLEAR_F ))
			(not ( HANDEMPTY ))
			(not ( ON_F_C ))
		)
	)
	(:action UNSTACK_F_F
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( CLEAR_F )
			( ON_F_F )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_F )
			(not ( HANDEMPTY ))
			(not ( ON_F_F ))
		)
	)
	(:action STACK_F_C
		:parameters ()
		:precondition
		(and
			( CLEAR_C )
			( HOLDING_F )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_F )
			( HANDEMPTY )
			( ON_F_C )
			(not ( HOLDING_F ))
			(not ( CLEAR_C ))
		)
	)
	(:action STACK_F_F
		:parameters ()
		:precondition
		(and
			( CLEAR_F )
			( HOLDING_F )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HANDEMPTY )
			( ON_F_F )
			(not ( HOLDING_F ))
		)
	)
	(:action PUT-DOWN_F
		:parameters ()
		:precondition
		(and
			( HOLDING_F )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( CLEAR_F )
			( HANDEMPTY )
			( ONTABLE_F )
			(not ( HOLDING_F ))
		)
	)
	(:action PICK-UP_F
		:parameters ()
		:precondition
		(and
			( HANDEMPTY )
			( ONTABLE_F )
			( CLEAR_F )
		)
		:effect
		(and
			(increase (total-cost) 1)
			( HOLDING_F )
			(not ( ONTABLE_F ))
			(not ( CLEAR_F ))
			(not ( HANDEMPTY ))
		)
	)

)
