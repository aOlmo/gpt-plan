(define (problem BW-generalization-4)
(:domain blocksworld-4ops)(:objects i c f a)
(:init 
(handempty)
(ontable i)
(ontable c)
(ontable f)
(ontable a)
(clear i)
(clear c)
(clear f)
(clear a)
)
(:goal
(and
(on i c)
(on c f)
(on f a)
)))