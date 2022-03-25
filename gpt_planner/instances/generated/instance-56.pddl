(define (problem BW-generalization-4)
(:domain blocksworld-4ops)(:objects l g f)
(:init 
(handempty)
(ontable l)
(ontable g)
(ontable f)
(clear l)
(clear g)
(clear f)
)
(:goal
(and
(on l g)
(on g f)
)))