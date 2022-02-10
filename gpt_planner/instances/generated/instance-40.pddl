

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 )
(:init
(handempty)
(on b1 b2)
(on b2 b4)
(ontable b3)
(ontable b4)
(on b5 b3)
(clear b1)
(clear b5)
)
(:goal
(and
(on b1 b4)
(on b2 b1)
(on b3 b2)
(on b4 b5))
)
)


