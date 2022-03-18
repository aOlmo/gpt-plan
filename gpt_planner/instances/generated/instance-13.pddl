

(define (problem BW-rand-4)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 )
(:init
(handempty)
(ontable b1)
(ontable b2)
(on b3 b2)
(on b4 b1)
(clear b3)
(clear b4)
)
(:goal
(and
(on b1 b3)
(on b4 b2))
)
)


