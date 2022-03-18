

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 )
(:init
(handempty)
(ontable b1)
(on b2 b4)
(on b3 b5)
(ontable b4)
(ontable b5)
(clear b1)
(clear b2)
(clear b3)
)
(:goal
(and
(on b2 b5)
(on b4 b3))
)
)


