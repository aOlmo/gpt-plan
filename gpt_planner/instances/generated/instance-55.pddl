(define (problem BW-generalization-4)
(:domain blocksworld-4ops)(:objects e g i c k d)
(:init 
(handempty)
(ontable e)
(ontable g)
(ontable i)
(ontable c)
(ontable k)
(ontable d)
(clear e)
(clear g)
(clear i)
(clear c)
(clear k)
(clear d)
)
(:goal
(and
(on e g)
(on g i)
(on i c)
(on c k)
(on k d)
)))