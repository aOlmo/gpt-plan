

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 )
(:init
(handempty)
(ontable b1)
(ontable b2)
(on b3 b2)
(ontable b4)
(on b5 b1)
(clear b3)
(clear b4)
(clear b5)
)
(:goal
(and
(on b2 b5)
(on b3 b4)
(on b4 b2)
(on b5 b1))
)
)


