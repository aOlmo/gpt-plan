(define (problem BW-generalization-4)
(:domain blocksworld-4ops)(:objects g h j d a f b i e c l k)
(:init 
(handempty)
(ontable g)
(ontable h)
(ontable j)
(ontable d)
(ontable a)
(ontable f)
(ontable b)
(ontable i)
(ontable e)
(ontable c)
(ontable l)
(ontable k)
(clear g)
(clear h)
(clear j)
(clear d)
(clear a)
(clear f)
(clear b)
(clear i)
(clear e)
(clear c)
(clear l)
(clear k)
)
(:goal
(and
(on g h)
(on h j)
(on j d)
(on d a)
(on a f)
(on f b)
(on b i)
(on i e)
(on e c)
(on c l)
(on l k)
)))