

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 )
(:init
(handempty)
(on b1 b2)
(on b2 b3)
(ontable b3)
(on b4 b1)
(ontable b5)
(clear b4)
(clear b5)
)
(:goal
(and
(on b3 b1)
(on b4 b3)
(on b5 b2))
)
)


