(define (problem BW-generalization-4)
(:domain blocksworld-4ops)(:objects i b h k d)
(:init 
(handempty)
(ontable i)
(ontable b)
(ontable h)
(ontable k)
(ontable d)
(clear i)
(clear b)
(clear h)
(clear k)
(clear d)
)
(:goal
(and
(on i b)
(on b h)
(on h k)
(on k d)
)))