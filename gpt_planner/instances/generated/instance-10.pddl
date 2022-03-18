

(define (problem BW-rand-4)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 )
(:init
(handempty)
(on b1 b2)
(on b2 b3)
(ontable b3)
(ontable b4)
(clear b1)
(clear b4)
)
(:goal
(and
(on b1 b2)
(on b3 b1)
(on b4 b3))
)
)


