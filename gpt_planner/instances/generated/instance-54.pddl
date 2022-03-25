(define (problem BW-generalization-4)
(:domain blocksworld-4ops)(:objects h f a)
(:init 
(handempty)
(ontable h)
(ontable f)
(ontable a)
(clear h)
(clear f)
(clear a)
)
(:goal
(and
(on h f)
(on f a)
)))