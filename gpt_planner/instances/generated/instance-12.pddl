

(define (problem BW-rand-4)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 )
(:init
(handempty)
(on b1 b2)
(ontable b2)
(on b3 b4)
(on b4 b1)
(clear b3)
)
(:goal
(and
(on b1 b4)
(on b3 b1)
(on b4 b2))
)
)


