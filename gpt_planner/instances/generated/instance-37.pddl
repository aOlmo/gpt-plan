

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 )
(:init
(handempty)
(ontable b1)
(on b2 b5)
(ontable b3)
(on b4 b3)
(ontable b5)
(clear b1)
(clear b2)
(clear b4)
)
(:goal
(and
(on b1 b4)
(on b4 b3)
(on b5 b1))
)
)


