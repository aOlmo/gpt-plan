

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 )
(:init
(handempty)
(on b1 b4)
(ontable b2)
(on b3 b5)
(ontable b4)
(on b5 b1)
(clear b2)
(clear b3)
)
(:goal
(and
(on b3 b4))
)
)


