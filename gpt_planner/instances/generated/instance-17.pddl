(define (problem BW-generalization-4)
(:domain blocksworld-4ops)(:objects d l i c g e k f h)
(:init 
(handempty)
(ontable d)
(ontable l)
(ontable i)
(ontable c)
(ontable g)
(ontable e)
(ontable k)
(ontable f)
(ontable h)
(clear d)
(clear l)
(clear i)
(clear c)
(clear g)
(clear e)
(clear k)
(clear f)
(clear h)
)
(:goal
(and
(on d l)
(on l i)
(on i c)
(on c g)
(on g e)
(on e k)
(on k f)
(on f h)
)))