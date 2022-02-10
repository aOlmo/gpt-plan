

(define (problem BW-rand-4)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 )
(:init
(handempty)
(on b1 b3)
(on b2 b1)
(ontable b3)
(ontable b4)
(clear b2)
(clear b4)
)
(:goal
(and
(on b1 b2)
(on b2 b4))
)
)


