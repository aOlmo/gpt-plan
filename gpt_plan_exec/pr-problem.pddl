(define
	(problem grounded-BLOCKS-5-0)
	(:domain grounded-BLOCKS)
	(:init
		(= (total-cost) 0)
		( HANDEMPTY )
		( ON_B_A )
		( ON_E_B )
		( ON_C_E )
		( ONTABLE_A )
		( ONTABLE_D )
		( CLEAR_C )
		( CLEAR_D )
	)
	(:goal
		(and 
		( ON_D_C )
		( ON_B_D )
		( ON_E_B )
		( ON_A_E )
		)
	)
	(:metric minimize (total-cost))

)
