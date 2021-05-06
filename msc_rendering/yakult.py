import prman


def draw_scene(ri: prman.Ri):
    # ri.Pattern('liquid', 'liquidShader', {"color baseColor": [0.4, 0.0, 0],
    #                                       "float fillLevel": 0.5})
    # ri.Bxdf('PxrSurface',
    #         'bxdf',
    #         {
    #             'reference color diffuseColor': ['liquidShader:Cout'],
    #             'reference float presence': ["liquidShader:Aout"]
    #         })

    ri.TransformBegin()
    # Base
    ri.Rotate(-90, 1, 0, 0)
    ri.Bxdf('PxrSurface',
            'bxdf',
            {
            })
    ri.Cylinder(1, -0.5, 0.7, 360)

    # Mid
    ri.TransformBegin()
    # ri.Bxdf('PxrSurface',
    #         'bxdf',
    #         {'color diffuseColor': [1, 0, 0]
    #          })
    ri.Translate(0, 0, 1)
    ri.Hyperboloid([1.0, 0, -0.3], [0.5, 0.8, 0.4], 360)
    ri.TransformEnd()

    # Upper ring
    ri.TransformBegin()
    # ri.Bxdf('PxrSurface',
    #         'bxdf',
    #         {'color diffuseColor': [0, 0, 1]
    #          })
    ri.Translate(0, 0, 1.4)
    ri.Cylinder(0.95, 0, 0.35, 360)
    ri.TransformEnd()

    # Upper cone
    ri.TransformBegin()
    # ri.Bxdf('PxrSurface',
    #         'bxdf',
    #         {'color diffuseColor': [0, 1, 0]
    #          })
    ri.Translate(0, 0, 2.25)
    ri.Hyperboloid([0.95, 0.0, -0.5], [0.5, 0.0, 0.2], 360)
    ri.TransformEnd()

    ri.TransformEnd()
