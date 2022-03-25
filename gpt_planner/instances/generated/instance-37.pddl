(define (problem BW-generalization-4)
(:domain blocksworld-4ops)(:objects c e a l)
(:init 
(handempty)
(ontable c)
(ontable e)
(ontable a)
(ontable l)
(clear c)
(clear e)
(clear a)
(clear l)
)
(:goal
(and
(on c e)
(on e a)
(on a l)
)))