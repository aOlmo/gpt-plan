(define (problem BW-generalization-4)
(:domain blocksworld-4ops)(:objects d c f g l j a k e b h)
(:init 
(handempty)
(ontable d)
(ontable c)
(ontable f)
(ontable g)
(ontable l)
(ontable j)
(ontable a)
(ontable k)
(ontable e)
(ontable b)
(ontable h)
(clear d)
(clear c)
(clear f)
(clear g)
(clear l)
(clear j)
(clear a)
(clear k)
(clear e)
(clear b)
(clear h)
)
(:goal
(and
(on d c)
(on c f)
(on f g)
(on g l)
(on l j)
(on j a)
(on a k)
(on k e)
(on e b)
(on b h)
)))