

(define (problem BW-rand-4)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 )
(:init
(handempty)
(ontable b1)
(ontable b2)
(on b3 b1)
(on b4 b3)
(clear b2)
(clear b4)
)
(:goal
(and
(on b1 b3)
(on b3 b4)
(on b4 b2))
)
)

