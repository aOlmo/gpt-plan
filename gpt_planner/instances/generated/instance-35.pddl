

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 )
(:init
(handempty)
(on b1 b2)
(ontable b2)
(on b3 b1)
(on b4 b5)
(ontable b5)
(clear b3)
(clear b4)
)
(:goal
(and
(on b1 b3)
(on b3 b5)
(on b4 b2)
(on b5 b4))
)
)


