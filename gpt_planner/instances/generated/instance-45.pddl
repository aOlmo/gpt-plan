(define (problem BW-generalization-4)
(:domain blocksworld-4ops)(:objects i l k e a b)
(:init 
(handempty)
(ontable i)
(ontable l)
(ontable k)
(ontable e)
(ontable a)
(ontable b)
(clear i)
(clear l)
(clear k)
(clear e)
(clear a)
(clear b)
)
(:goal
(and
(on i l)
(on l k)
(on k e)
(on e a)
(on a b)
)))