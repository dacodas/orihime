import bleach

class Cleaner(bleach.sanitizer.Cleaner):

    def __init__(self, *args, **kwargs):

        attributes = {
            **bleach.sanitizer.ALLOWED_ATTRIBUTES,
            **{
                'div': ['class', 'id'],
                'span': ['class', 'id']
            }
        }

        new_kwargs = {
            **kwargs,
            **{
                'tags': bleach.sanitizer.ALLOWED_TAGS + ['p', 'div', 'span', 'br', 'ruby', 'rt'],
                'attributes': attributes
            }
        }

        super(Cleaner, self).__init__(*args, **new_kwargs)

