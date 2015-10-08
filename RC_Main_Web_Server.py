from RPi.GPIO import setup, OUT, PWM, output, LOW, HIGH, cleanup, setmode, BCM
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response

__author__ = 'root'

setmode(BCM)

setup(17, OUT)
setup(20, OUT)
setup(22, OUT)
setup(5, OUT)
setup(6, OUT)
setup(13, OUT)

isForward = None
isBackward = None

def default_response():
    return Response('<font size=400><center>'
                    '<a href=/move/f>forward</a><br><br>'
                    '<a href=/move/l>left</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
                    '<a href=/move/s>stop</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
                    '<a href=/move/r>right</a><br><br>'
                    '<a href=/move/b>backward</a></center></font>')

def right(duty=100):
    output(5, HIGH)
    output(6, LOW)
    p2.ChangeDutyCycle(float(duty))


def left(duty=100):
    output(5, LOW)
    output(6, HIGH)
    p2.ChangeDutyCycle(float(duty))
    return default_response()


def straight(duty=100):
    output(5, LOW)
    output(6, LOW)


def backward(duty=50):
    global isForward
    global isBackward
    isForward = False
    if isBackward:
        duty = 75
    straight()
    output(20, HIGH)
    output(22, LOW)
    p.ChangeDutyCycle(float(duty))
    isBackward = True


def forward(duty=50):
    global isForward
    global isBackward
    isBackward = False
    if isForward:
        duty = 75
    straight()
    output(20, LOW)
    output(22, HIGH)
    p.ChangeDutyCycle(float(duty))
    isForward = True


def stop(duty=0):
    straight()
    output(20, LOW)
    output(22, LOW)
    return default_response()


def default(duty=0):
    print "Command not found"

stop(0)
straight(0)

p = PWM(17, 90)
p2 = PWM(13, 90)
p.start(50)
p2.start(100)

commands_dict = {"b": backward,
                 "f": forward,
                 "s": stop,
                 "r": right,
                 "l": left,
                 "st": straight}


def move(request):
    commands_dict.get(request.matchdict['direction'], default)()
    return default_response()

fspeed = 0
rspeed = 0

if __name__ == '__main__':
    config = Configurator()
    config.add_route('move', '/move/{direction}')
    config.add_view(move, route_name='move')
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8081, app)
    server.serve_forever()

p.stop()

cleanup(17)
cleanup(20)
cleanup(22)
cleanup(5)
cleanup(6)
cleanup(13)
