(define (problem BW-generalization-4)
(:domain blocksworld-4ops)(:objects b a k h)
(:init 
(handempty)
(ontable b)
(ontable a)
(ontable k)
(ontable h)
(clear b)
(clear a)
(clear k)
(clear h)
)
(:goal
(and
(on b a)
(on a k)
(on k h)
)))