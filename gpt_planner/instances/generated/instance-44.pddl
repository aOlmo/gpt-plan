

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 )
(:init
(handempty)
(on b1 b2)
(on b2 b5)
(on b3 b1)
(ontable b4)
(ontable b5)
(clear b3)
(clear b4)
)
(:goal
(and
(on b3 b1)
(on b4 b5)
(on b5 b3))
)
)


