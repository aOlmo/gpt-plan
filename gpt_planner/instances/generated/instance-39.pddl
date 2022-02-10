

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 )
(:init
(handempty)
(on b1 b2)
(on b2 b3)
(on b3 b5)
(ontable b4)
(on b5 b4)
(clear b1)
)
(:goal
(and
(on b2 b3)
(on b3 b5)
(on b5 b1))
)
)


