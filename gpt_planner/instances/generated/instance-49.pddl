(define (problem BW-generalization-4)
(:domain blocksworld-4ops)(:objects j i a)
(:init 
(handempty)
(ontable j)
(ontable i)
(ontable a)
(clear j)
(clear i)
(clear a)
)
(:goal
(and
(on j i)
(on i a)
)))