(define (problem BW-generalization-4)
(:domain blocksworld-4ops)(:objects g d b k j f)
(:init 
(handempty)
(ontable g)
(ontable d)
(ontable b)
(ontable k)
(ontable j)
(ontable f)
(clear g)
(clear d)
(clear b)
(clear k)
(clear j)
(clear f)
)
(:goal
(and
(on g d)
(on d b)
(on b k)
(on k j)
(on j f)
)))