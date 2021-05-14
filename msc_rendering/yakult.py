import prman


def draw_scene(ri: prman.Ri):
    BOTTLE_DIFFUSE = [0.84, 0.73, 0.65]
    CAP_DIFFUSE = [0.38, 0.18, 0.20]
    CAP_SPECULAR_FACE = [0.8, 0.1, 0.1]
    CAP_SPECULAR_ROUGHNESS = [0.5]

    ri.TransformBegin()
    ri.Rotate(-90, 1, 0, 0)

    # Base logo
    ri.AttributeBegin()
    ri.TransformBegin()
    ri.Translate(0, 4, 0.3)
    ri.Rotate(90, 1, 0, 0)
    ri.Scale(2, 2.5, 2)
    # ri.Cone(0.5, 0.2, 360, {})
    ri.ScopedCoordinateSystem('base_logo_trs')
    ri.TransformEnd()

    # Base bxdf
    ri.Pattern('PxrProjector', 'base_projector', {'string coordsys': ['base_logo_trs']})
    ri.Pattern('PxrProjectionLayer', 'logo_prj', {'string filename': 'yakult_logo_circle.tx',
                                                  'reference struct manifold': 'base_projector:result'})
    ri.Pattern('PxrMix', 'base_mix', {'color color1': BOTTLE_DIFFUSE,
                                      'reference color color2': 'logo_prj:resultRGB',
                                      'reference float mix': 'logo_prj:resultA'})

    ri.Bxdf('PxrLayerSurface',
            'base_surface',
            {
                'reference color diffuseColor': 'base_mix:resultRGB',
                'color specularFaceColor': [0.3, 0.3, 0.3],
                'float specularRoughness': [0.6]
                # 'reference color diffuseColor': 'logo_txr:resultRGB',
                # 'reference color diffuseColor': 'base_prj_stack:resultRGB'
            })
    ri.Cylinder(1, -0.5, 0.7, 360)
    ri.AttributeEnd()

    # Mid
    ri.TransformBegin()
    ri.Bxdf('PxrLayerSurface',
            'base_surface',
            {
                'color diffuseColor': BOTTLE_DIFFUSE,
                'color specularFaceColor': [0.3, 0.3, 0.3],
                'float specularRoughness': [0.6]
                # 'reference color diffuseColor': 'logo_txr:resultRGB',
                # 'reference color diffuseColor': 'base_prj_stack:resultRGB'
            })
    ri.Translate(0, 0, 1)
    ri.Hyperboloid([1.0, 0, -0.3], [0.5, 0.8, 0.4], 360)
    ri.TransformEnd()

    # Upper ring
    ri.TransformBegin()
    # ri.Bxdf('PxrSurface',
    #         'bxdf',
    #         {'color diffuseColor': BOTTLE_DIFFUSE
    #          })
    ri.Translate(0, 0, 1.4)
    ri.Cylinder(0.95, 0, 0.35, 360)
    ri.TransformEnd()

    # Upper cone
    ri.TransformBegin()
    # ri.Bxdf('PxrSurface',
    #         'bxdf',
    #         {'color diffuseColor': BOTTLE_DIFFUSE
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
            {'color diffuseColor': CAP_DIFFUSE,
             'color specularFaceColor': CAP_SPECULAR_FACE,
             'float specularRoughness': CAP_SPECULAR_ROUGHNESS
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
            {'color diffuseColor': CAP_DIFFUSE,
             'color specularFaceColor': CAP_SPECULAR_FACE,
             'float specularRoughness': CAP_SPECULAR_ROUGHNESS
             })
    ri.TransformBegin()
    ri.Translate(0, 0, 2.5)
    ri.Disk(0, 0.6, 360)
    ri.TransformEnd()
    ri.AttributeEnd()

    ri.TransformEnd()
