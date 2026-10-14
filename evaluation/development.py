"""Deterministic synthetic development families; not a sealed holdout."""
from copy import deepcopy


def label(eid, content, x, y, width, height, size, **extra):
    return dict(id=eid, type='text', content=content, x=x, y=y, width=width,
                height=height, font_size=size, font_family='Solstice Sans',
                color='rgba(255,255,255,1)', z_index=5, **extra)


def button(eid, content, x, y, width=260, height=64, rotation=0):
    return [dict(id=eid+'-shape', type='shape', x=x, y=y, width=width, height=height,
                 shape_type='rectangle', fill_color='rgba(232,106,58,1)', z_index=3,
                 group_id=eid, rotation=rotation, corner_radius=16),
            label(eid+'-label', content, x+8, y+12, width-16, height-24, 20,
                  group_id=eid, rotation=rotation, text_align='center')]


def families():
    background = dict(id='canvas-art', type='image', x=0, y=0, width=900, height=900,
                      asset_id='solstice_bg_gradient.png', fit='cover', z_index=0)
    editorial = [label('t0', 'Ideas worth sharing', 70, 80, 760, 110, 52, font_weight='bold'),
        label('t1', 'Stories from our community, collected for the season ahead.', 70, 230, 760, 180, 30),
        label('t2', 'Meet the makers. Explore their work. Find a new perspective.', 70, 470, 760, 140, 26),
        label('t3', 'Free admission. Doors open at noon.', 70, 710, 760, 80, 18)]
    catalog = [dict(id='visual-a', type='image', x=80, y=80, width=300, height=300,
                    asset_id='solstice_bottle.png', fit='contain', z_index=2),
               dict(id='visual-b', type='image', x=520, y=80, width=300, height=300,
                    asset_id='solstice_bottle.png', fit='contain', z_index=2),
               label('t0', 'Two ways to enjoy the afternoon', 60, 430, 780, 130, 42),
               label('t1', 'Botanical flavor, made to share with friends.', 60, 580, 780, 100, 24),
               *button('g0', 'Explore the collection', 100, 740),
               *button('g1', 'Find a local stockist', 500, 740)]
    event = [dict(id='mark', type='image', x=300, y=30, width=300, height=100,
                  asset_id='solstice_logo_lockup.png', fit='contain', z_index=2),
             label('t0', 'An evening under the stars', 50, 210, 800, 160, 48),
             label('t1', 'Live music and botanical refreshments.\nBring a friend and stay awhile.', 70, 420, 760, 170, 26),
             *button('g0', 'Reserve your place', 80, 700, rotation=-10),
             *button('g1', 'Friday at sunset', 530, 700)]
    dense = [label('t0', 'A guide to the summer collection', 60, 60, 780, 130, 38),
             label('t1', 'Discover carefully blended botanical flavors, seasonal ingredients, and new favorites for gatherings big and small.', 60, 230, 780, 180, 24),
             *button('g0', 'Made with botanicals', 30, 470),
             *button('g1', 'Bright citrus notes', 320, 470),
             *button('g2', 'Ready to share', 610, 470),
             *button('g3', 'Explore our story', 160, 630),
             *button('g4', 'See the collection', 500, 630),
             label('t2', 'Availability varies by location. Visit your stockist for details.', 60, 790, 780, 60, 14)]
    for name, elements in [('editorial', editorial), ('catalog', catalog), ('event', event), ('dense-labels', dense)]:
        yield name, {'canvas': {'width': 900, 'height': 900}, 'elements': [deepcopy(background), *elements]}


def tasks():
    for family, source in families():
        for target_name, (width, height) in [('banner', (1200, 240)), ('story', (360, 780)), ('compact', (640, 100))]:
            yield {'case': family+'-'+target_name, 'family': family, 'source': deepcopy(source),
                   'target_canvas': {'width': width, 'height': height}}
