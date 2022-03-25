(define (problem BW-generalization-4)
(:domain blocksworld-4ops)(:objects c i d b)
(:init 
(handempty)
(ontable c)
(ontable i)
(ontable d)
(ontable b)
(clear c)
(clear i)
(clear d)
(clear b)
)
(:goal
(and
(on c i)
(on i d)
(on d b)
)))