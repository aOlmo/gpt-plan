(define (problem BW-generalization-4)
(:domain blocksworld-4ops)(:objects d h j)
(:init 
(handempty)
(ontable d)
(ontable h)
(ontable j)
(clear d)
(clear h)
(clear j)
)
(:goal
(and
(on d h)
(on h j)
)))