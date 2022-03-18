

(define (problem BW-rand-4)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 )
(:init
(handempty)
(ontable b1)
(on b2 b3)
(on b3 b1)
(on b4 b2)
(clear b4)
)
(:goal
(and
(on b2 b4)
(on b3 b2))
)
)


