(define (problem BW-generalization-4)
(:domain blocksworld-4ops)(:objects j g l)
(:init 
(handempty)
(ontable j)
(ontable g)
(ontable l)
(clear j)
(clear g)
(clear l)
)
(:goal
(and
(on j g)
(on g l)
)))