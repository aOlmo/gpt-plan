(define (problem BW-generalization-4)
(:domain blocksworld-4ops)(:objects j a k)
(:init 
(handempty)
(ontable j)
(ontable a)
(ontable k)
(clear j)
(clear a)
(clear k)
)
(:goal
(and
(on j a)
(on a k)
)))