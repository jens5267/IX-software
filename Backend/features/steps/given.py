from behave import Given
from somos.models import Port

@Given('a {object}')
def impl_step(context, object):
    objects = {
        "Port": Port.objects.create(name="Port")
    }
    context.object = objects[object]
    assert context.object is not None, "Implementation failed"
