import prman


def draw_scene(ri: prman.Ri):
    # Base
    ri.TransformBegin()
    ri.Rotate(-90, 1, 0, 0)
    ri.Bxdf('PxrSurface',
            'bxdf',
            {
                'color diffuseColor': [0.84, 0.73, 0.65],
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
    ri.Hyperboloid([0.95, 0.0, -0.5], [0.5, 0.0, 0.15], 360)
    ri.TransformEnd()

    # Cap side
    ri.AttributeBegin()

    ri.Attribute('displacementbound', {'sphere': [0.14], "coordinatesystem": ["object"]})
    ri.Pattern('distort', 'distortTx', {})
    ri.Displace('PxrDisplace', 'capDisplace', {'float dispAmount': [0.05],
                                               'reference vector dispVector': 'distortTx:Cout'})

    ri.Bxdf('PxrSurface',
            'bxdf',
            {'color diffuseColor': [0.38, 0.18, 0.20],
             'float specularRoughness': 0.0
             })
    ri.TransformBegin()
    ri.Translate(0, 0, 2.25)
    ri.Cylinder(0.6, 0, 0.25, 360)
    ri.TransformEnd()

    ri.AttributeEnd()

    # Cap top
    ri.AttributeBegin()

    ri.Attribute('displacementbound', {'sphere': [0.14], "coordinatesystem": ["object"]})
    ri.Pattern('top_distort', 'topDistortTx', {})
    ri.Displace('PxrDisplace', 'capDisplace', {'float dispAmount': [0.05],
                                               'reference vector dispVector': 'topDistortTx:Cout'})

    ri.Bxdf('PxrSurface',
            'bxdf',
            {'color diffuseColor': [0.38, 0.18, 0.20]
             })
    ri.TransformBegin()
    ri.Translate(0, 0, 2.5)
    ri.Disk(0, 0.6, 360)
    ri.TransformEnd()
    ri.AttributeEnd()

    ri.TransformEnd()
