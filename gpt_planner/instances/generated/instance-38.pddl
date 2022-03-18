

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 )
(:init
(handempty)
(on b1 b4)
(ontable b2)
(on b3 b2)
(on b4 b5)
(on b5 b3)
(clear b1)
)
(:goal
(and
(on b2 b1)
(on b4 b5))
)
)


