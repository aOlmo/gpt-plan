

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 )
(:init
(handempty)
(on b1 b3)
(ontable b2)
(ontable b3)
(on b4 b1)
(ontable b5)
(clear b2)
(clear b4)
(clear b5)
)
(:goal
(and
(on b2 b1)
(on b4 b2)
(on b5 b3))
)
)


