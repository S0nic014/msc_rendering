import prman


def draw_scene(ri: prman.Ri):
    BOTTLE_DIFFUSE = [0.84, 0.73, 0.65]
    BOTTLE_DIFFUSE_ROUGHNESS = [0.0]
    BOTTLE_SPECULAR_EDGE = [1.0, 1.0, 1.0]
    BOTTLE_SPECULAR_EC = [0.9, 0.9, 0.9]
    BOTTLE_SPECULAR_ROUGHNESS = [0.4]

    CAP_DIFFUSE = [0.5, 0.18, 0.20]
    CAP_DIFFUSE_ROUGHNESS = [0.0]
    CAP_SPECULAR_EDGE = [1.0, 1.0, 1.0]
    CAP_SPECULAR_EC = [0.8, 0.8, 0.8]
    CAP_SPECULAR_ROUGHNESS = [0.3]

    # Under disk
    ri.AttributeBegin()
    ri.TransformBegin()
    ri.Rotate(90, 1, 0, 0)
    ri.Translate(0, 0, 0.5)
    ri.Disk(0, 1.0, 360)
    ri.TransformEnd()
    ri.AttributeEnd()

    ri.TransformBegin()

    ri.Rotate(-90, 1, 0, 0)
    # Base logo projection
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
    ri.Pattern('PxrLayeredBlend', 'base_layer_blend', {'reference color RGB_0': 'logo_prj:resultRGB',
                                                       'reference float A_0': 'logo_prj:resultA',
                                                       'int enable_0': [1],
                                                       'color backgroundRGB': BOTTLE_DIFFUSE})

    ri.Bxdf('PxrLayerSurface',
            'base_surface',
            {
                'reference color diffuseColor': 'base_layer_blend:resultRGB',
                'int specularFresnelMode': [1],
                'color specularEdgeColor': BOTTLE_SPECULAR_EDGE,
                'color specularExtinctionCoeff': BOTTLE_SPECULAR_EC,
                'float specularRoughness': BOTTLE_SPECULAR_ROUGHNESS
            })
    ri.Cylinder(1, -0.5, 0.7, 360)
    ri.AttributeEnd()

    # Mid
    ri.TransformBegin()
    ri.Translate(0, 0, 1)

    ri.Bxdf('PxrLayerSurface',
            'base_surface',
            {
                'color diffuseColor': BOTTLE_DIFFUSE,
                'float diffuseRoughness': BOTTLE_DIFFUSE_ROUGHNESS,
                'int specularFresnelMode': [1],
                'color specularEdgeColor': BOTTLE_SPECULAR_EDGE,
                'color specularExtinctionCoeff': BOTTLE_SPECULAR_EC,
                'float specularRoughness': BOTTLE_SPECULAR_ROUGHNESS
            })
    ri.Hyperboloid([1.0, 0, -0.3], [0.5, 0.8, 0.4], 360)
    ri.TransformEnd()

    # Upper ring
    ri.AttributeBegin()
    ri.TransformBegin()
    ri.Translate(0, 0, 1.4)
    # Upper ring logos
    ri.TransformBegin()
    ri.Rotate(90, 1, 0, 0)
    ri.Rotate(20, 0, 1, 0)
    ri.Translate(0, 0.2, -4)
    # ri.Cone(0.5, 0.2, 360, {})
    ri.Scale(2, 2.5, 2)
    ri.ScopedCoordinateSystem('ring_logo_trs')
    ri.TransformEnd()

    ri.TransformBegin()
    ri.Rotate(90, 1, 0, 0)
    ri.Rotate(-60, 0, 1, 0)
    ri.Translate(0, 0.2, -4)
    # ri.Cone(0.5, 0.2, 360, {})
    ri.Scale(2, 2, 2)
    ri.ScopedCoordinateSystem('ring_logo_trs2')
    ri.TransformEnd()

    # ring logo bxdf
    ri.Pattern('PxrProjector', 'ring_projector', {'string coordsys': ['ring_logo_trs']})
    ri.Pattern('PxrProjectionLayer', 'ring_logo_prj', {'string filename': 'yakult_logo_text.tx',
                                                       'reference struct manifold': 'ring_projector:result',
                                                       'int linearize': [1]})
    ri.Pattern('PxrProjector', 'ring_projector2', {'string coordsys': ['ring_logo_trs2']})
    ri.Pattern('PxrProjectionLayer', 'ring_logo_prj2', {'string filename': 'yakult_logo_text.tx',
                                                        'reference struct manifold': 'ring_projector2:result',
                                                        'int linearize': [1]})

    ri.Pattern('PxrLayeredBlend', 'base_layer_blend', {'reference color RGB_0': 'ring_logo_prj:resultRGB',
                                                       'reference float A_0': 'ring_logo_prj:resultA',
                                                       'int enable_0': [1],
                                                       'reference color RGB_1': 'ring_logo_prj2:resultRGB',
                                                       'reference float A_1': 'ring_logo_prj2:resultA',
                                                       'int enable_1': [1],
                                                       'color backgroundRGB': BOTTLE_DIFFUSE})

    ri.Bxdf('PxrLayerSurface',
            'base_surface',
            {
                'reference color diffuseColor': 'base_layer_blend:resultRGB',
                'float diffuseRoughness': BOTTLE_DIFFUSE_ROUGHNESS,
                'int specularFresnelMode': [1],
                'color specularEdgeColor': BOTTLE_SPECULAR_EDGE,
                'color specularExtinctionCoeff': BOTTLE_SPECULAR_EC,
                'float specularRoughness': BOTTLE_SPECULAR_ROUGHNESS
            })
    ri.Cylinder(0.95, 0, 0.35, 360)
    ri.TransformEnd()

    # Upper cone
    ri.TransformBegin()
    ri.Bxdf('PxrSurface',
            'bxdf',
            {
                'color diffuseColor': BOTTLE_DIFFUSE,
                'float diffuseRoughness': BOTTLE_DIFFUSE_ROUGHNESS,
                'int specularFresnelMode': [1],
                'color specularEdgeColor': BOTTLE_SPECULAR_EDGE,
                'color specularExtinctionCoeff': BOTTLE_SPECULAR_EC,
                'float specularRoughness': BOTTLE_SPECULAR_ROUGHNESS
            })
    ri.Translate(0, 0, 2.25)
    ri.Hyperboloid([0.95, 0.0, -0.5], [0.5, 0.0, 0.15], 360)
    ri.TransformEnd()
    ri.AttributeEnd()

    # Cap side
    ri.AttributeBegin()
    ri.Attribute('displacementbound', {'sphere': [0.14], "coordinatesystem": ["object"]})
    ri.Pattern('distort', 'distortTx', {})
    ri.Displace('PxrDisplace', 'capDisplace', {'float dispAmount': [0.05],
                                               'reference vector dispVector': 'distortTx:Cout'})

    ri.Bxdf('PxrSurface',
            'bxdf',
            {'color diffuseColor': CAP_DIFFUSE,
             'float diffuseRoughness': CAP_DIFFUSE_ROUGHNESS,
             'int specularFresnelMode': [1],
             'color specularEdgeColor': CAP_SPECULAR_EDGE,
             'color specularExtinctionCoeff': CAP_SPECULAR_EC,
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
             'float diffuseRoughness': CAP_DIFFUSE_ROUGHNESS,
             'int specularFresnelMode': [1],
             'color specularEdgeColor': CAP_SPECULAR_EDGE,
             'color specularExtinctionCoeff': CAP_SPECULAR_EC,
             'float specularRoughness': CAP_SPECULAR_ROUGHNESS
             })
    ri.TransformBegin()
    ri.Translate(0, 0, 2.5)
    ri.Disk(0, 0.6, 360)
    ri.TransformEnd()
    ri.AttributeEnd()

    ri.TransformEnd()
