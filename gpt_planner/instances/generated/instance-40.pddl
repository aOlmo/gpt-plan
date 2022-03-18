

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 )
(:init
(handempty)
(on b1 b4)
(ontable b2)
(on b3 b5)
(on b4 b3)
(ontable b5)
(clear b1)
(clear b2)
)
(:goal
(and
(on b1 b3)
(on b2 b4)
(on b3 b5)
(on b4 b1))
)
)


