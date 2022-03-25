(define (problem BW-generalization-4)
(:domain blocksworld-4ops)(:objects f j i)
(:init 
(handempty)
(ontable f)
(ontable j)
(ontable i)
(clear f)
(clear j)
(clear i)
)
(:goal
(and
(on f j)
(on j i)
)))