(define (problem BW-generalization-4)
(:domain blocksworld-4ops)(:objects a c i g)
(:init 
(handempty)
(ontable a)
(ontable c)
(ontable i)
(ontable g)
(clear a)
(clear c)
(clear i)
(clear g)
)
(:goal
(and
(on a c)
(on c i)
(on i g)
)))