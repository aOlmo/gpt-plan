(define (problem BW-generalization-4)
(:domain blocksworld-4ops)(:objects f e c)
(:init 
(handempty)
(ontable f)
(ontable e)
(ontable c)
(clear f)
(clear e)
(clear c)
)
(:goal
(and
(on f e)
(on e c)
)))