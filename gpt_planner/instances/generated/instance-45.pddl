

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 )
(:init
(handempty)
(ontable b1)
(on b2 b4)
(on b3 b5)
(ontable b4)
(on b5 b2)
(clear b1)
(clear b3)
)
(:goal
(and
(on b1 b2)
(on b3 b5))
)
)


