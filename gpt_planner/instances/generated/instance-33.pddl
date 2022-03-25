(define (problem BW-generalization-4)
(:domain blocksworld-4ops)(:objects k i e)
(:init 
(handempty)
(ontable k)
(ontable i)
(ontable e)
(clear k)
(clear i)
(clear e)
)
(:goal
(and
(on k i)
(on i e)
)))