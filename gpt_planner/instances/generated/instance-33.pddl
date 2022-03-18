

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 )
(:init
(handempty)
(ontable b1)
(on b2 b1)
(on b3 b5)
(ontable b4)
(ontable b5)
(clear b2)
(clear b3)
(clear b4)
)
(:goal
(and
(on b1 b5)
(on b3 b1)
(on b4 b3)
(on b5 b2))
)
)


