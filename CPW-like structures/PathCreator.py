"""
@author: Mykhailo Savytskyi
"""
import gdspy
import Position
import numpy
from Parameters import *

print('Using gdspy module version ' + gdspy.__version__)


# fuction that writes the created structure to gds file
def write():
    gdspy.write_gds(filepath + "/" + filename, unit=1.0e-6, precision=1.0e-9)
    print('gds file saved to "' + filepath + "/" + filename + '"')
    print('PathCreator Finished!')


def initPath(width):
    path = gdspy.Path(width, (position.x, position.y))
    return path


def createPoly(width, length, direction='+x', final_width=None, spec_path=spec_path):
    path = initPath(width)
    path.segment(length, direction, final_width=final_width, **spec_path)
    cell.add(path)
    if (direction == '+x'):
        position.move_x(length)
    elif (direction == '-x'):
        position.move_x(-length)
    elif (direction == '+y'):
        position.move_y(length)
    elif (direction == '-y'):
        position.move_y((-length))


def createArc(width, radius, angle1, angle2):
    path = initPath(width)
    path.arc(radius, angle1, angle2, **spec)
    cell.add(path)
    cx = position.x - radius * numpy.cos(angle1)
    cy = position.y - radius * numpy.sin(angle1)
    position.x = cx + radius * numpy.cos(angle2)
    position.y = cy + radius * numpy.sin(angle2)


def poly_minus_x_draw(total_length, width, step, side_offset=min_side_offset):
    if (position.x > side_offset + R) and (position.length < total_length):
        length_to_edge_of_chip = position.x - (side_offset + R + step)
        remaining_length = total_length - position.length
        length_to_draw = length_to_edge_of_chip if (length_to_edge_of_chip < remaining_length) else remaining_length
        createPoly(width, length_to_draw, direction=position.direction)
        position.length += length_to_draw

    while (position.x > side_offset + R) and (position.length < total_length):
        createPoly(width, step, direction=position.direction)
        position.length += step


def poly_plus_x_draw(total_length, width, step, side_offset=min_side_offset):
    if (position.x < chip_width - side_offset - R) and (position.length < total_length):
        length_to_edge_of_chip = (chip_width - side_offset - R - step) - position.x
        remaining_length = total_length - position.length
        length_to_draw = length_to_edge_of_chip if (length_to_edge_of_chip < remaining_length) else remaining_length
        createPoly(width, length_to_draw, direction=position.direction)
        position.length += length_to_draw

    while (position.x < chip_width - side_offset - R) and (position.length < total_length):
        createPoly(width, step, direction=position.direction)
        position.length += step


def arc_minus_x_draw(d_angle, total_length, width):
    # length_to_do = (total_length - position.length)
    # if length_to_do > numpy.pi * R and position.angle == numpy.pi/2:
    #     createArc(width, R, position.angle, 3 * numpy.pi / 2)
    #     position.angle = 3 * numpy.pi / 2
    #     position.length += numpy.pi * R
    # else:
    #     final_angle = length_to_do / R + position.angle
    #     if final_angle > 3 * numpy.pi / 2:
    #         final_angle = 3 * numpy.pi / 2
    #         length_to_do = (final_angle - position.angle)*R
    #     createArc(width, R, position.angle, final_angle)
    #     position.angle = final_angle
    #     position.length += length_to_do

    for n in range(int(round(numpy.pi / d_angle))):
        if (position.length < total_length) and (position.angle <= 3 * numpy.pi / 2):
            end_angle = position.angle + d_angle
            if end_angle > 3 * numpy.pi / 2:  # round it to nearest pi/2
                end_angle = 3 * numpy.pi / 2
            createArc(width, R, position.angle, end_angle)
            position.length += abs(end_angle - position.angle) * R
            position.add_angle(end_angle - position.angle)
        else:
            break

    if (position.angle >= 3 * numpy.pi / 2):
        position.change_direction()
        position.arcContinue = False
        position.angle = -numpy.pi / 2
    else:
        position.arcContinue = True


def arc_half_minus_x_draw(d_angle, total_length, width):
    for n in range(int(round((numpy.pi / 2) / d_angle))):
        if (position.length < total_length) and (position.angle <= numpy.pi):
            createArc(width, R, position.angle, position.angle + d_angle)
            position.length += d_angle * R
            position.add_angle(d_angle)
        else:
            break

    if (position.angle >= numpy.pi):
        position.change_direction()
        position.arcContinue = False
        position.angle = -numpy.pi / 2
    else:
        position.arcContinue = True


def arc_plus_x_draw(d_angle, total_length, width):
    # length_to_do = (total_length - position.length)
    # if length_to_do > numpy.pi * R and position.angle == -numpy.pi / 2:
    #     createArc(width, -R, position.angle, -3 * numpy.pi / 2)
    #     position.angle = -3 * numpy.pi / 2
    #     position.length += numpy.pi * R
    # else:
    #     final_angle = position.angle - length_to_do / R
    #     if final_angle <  -3 * numpy.pi / 2:
    #         final_angle = -3 * numpy.pi / 2
    #         length_to_do = (position.angle - final_angle)*R
    #     createArc(width, -R, position.angle, final_angle)
    #     position.angle = final_angle
    #     position.length += length_to_do

    for n in range(int(round(numpy.pi / d_angle))):
        if (position.length < total_length) and (position.angle >= -3 * numpy.pi / 2):
            end_angle = position.angle - d_angle
            if end_angle < -3 * numpy.pi / 2:  # round it to nearest pi/2
                end_angle = -3 * numpy.pi / 2
            createArc(width, -R, position.angle, end_angle)
            position.length += abs(end_angle - position.angle) * R
            position.add_angle(end_angle - position.angle)
        else:
            break

    if (position.angle <= -3 * numpy.pi / 2):
        position.change_direction()
        position.arcContinue = False
        position.angle = numpy.pi / 2
    else:
        position.arcContinue = True


def arc_half_plus_x_draw(d_angle, total_length, width):
    for n in range(int(round((numpy.pi / 2) / d_angle))):
        if (position.length < total_length) and (position.angle >= -3 * numpy.pi / 2):
            createArc(width, -R, position.angle, position.angle - d_angle)
            position.length += d_angle * R
            position.add_angle(-d_angle)
        else:
            break

    if (position.angle <= -3 * numpy.pi / 2):
        position.change_direction()
        position.arcContinue = False
        position.angle = numpy.pi / 2
    else:
        position.arcContinue = True


# The main function that creates meanders
def meander_draw(total_length, width, step):
    if position.arcContinue == False:

        if position.direction == '-x':
            poly_minus_x_draw(total_length, width, step)
            if position.length < total_length:
                arc_minus_x_draw(d_angle, total_length, width)
            if position.length < total_length:
                meander_draw(total_length, width, step)

        if position.direction == '+x':
            poly_plus_x_draw(total_length, width, step)
            if position.length < total_length:
                arc_plus_x_draw(d_angle, total_length, width)
            if position.length < total_length:
                meander_draw(total_length, width, step)

    else:
        if position.angle < 0:
            arc_plus_x_draw(d_angle, total_length, width)
        else:
            arc_minus_x_draw(d_angle, total_length, width)
        if position.length < total_length:
            meander_draw(total_length, width, step)

    # print(str(position.length) + '/')


# Overwritten meander_draw function to meet requirements for the last meander
def last_meander_draw(width, step):
    if position.arcContinue == False:

        if position.direction == '-x':
            if position.x < last_meander_side_offset:
                # Turn around to the middle
                length_to_draw = numpy.pi * R + (last_meander_side_offset - position.x + step) + numpy.pi * R / 2
                arc_minus_x_draw(d_angle, length_to_draw, width)
                poly_plus_x_draw(length_to_draw, width, step, side_offset=last_meander_side_offset)

                arc_half_plus_x_draw(d_angle, length_to_draw, width)

            else:
                length_to_draw = (position.x - last_meander_side_offset) + numpy.pi * R / 2
                poly_minus_x_draw(length_to_draw, width, step, side_offset=last_meander_side_offset)
                arc_half_minus_x_draw(d_angle, length_to_draw, width)

        elif position.direction == '+x':
            if position.x > last_meander_side_offset:
                # Turn around to the middle
                length_to_draw = numpy.pi * R + (position.x - last_meander_side_offset + step) + numpy.pi * R / 2
                arc_plus_x_draw(d_angle, length_to_draw, width)
                poly_minus_x_draw(length_to_draw, width, step, side_offset=last_meander_side_offset)

                arc_half_minus_x_draw(d_angle, length_to_draw, width)

            else:
                length_to_draw = (last_meander_side_offset - position.x) + numpy.pi * R / 2
                poly_plus_x_draw(length_to_draw, width, step, side_offset=last_meander_side_offset)
                arc_half_plus_x_draw(d_angle, length_to_draw, width)

    else:
        if position.angle < 0:
            arc_half_plus_x_draw(d_angle, numpy.pi / 2 * R, width)
        else:
            arc_half_minus_x_draw(d_angle, numpy.pi / 2 * R, width)

    final_length = 0
    position.direction = '-y'
    while (final_length < (step * 10)):
        createPoly(width, step, direction=position.direction)
        final_length += step

    position.length += final_length

    # print(str(position.length) + '/')


# Overwritten meander_draw function to meet requirements for the first meander
def first_meander_draw(total_length, width, step, direction):
    length = 0
    if direction == '+x':
        while position.x < chip_width - min_side_offset - R:
            createPoly(width, step, direction=direction)
            length += step
        if length < total_length:
            createArc(t_Zhigh, R, numpy.pi / 2.0, 0)
            length += numpy.pi * R / 2
        if length < total_length:
            while position.y > chip_length / 2 - edge_offset - resonator_y_offset:
                createPoly(width, step, direction='-y')
                length += step
        if length < total_length:
            createArc(t_Zhigh, R, 0 * numpy.pi / 2.0, -numpy.pi / 2)
            length += numpy.pi * R / 2
        if length < total_length:
            createPoly(t_Zhigh, total_length - length, direction='-x')


def taper(initial_width, final_width, length, direction, step=step_polygon):

    # Fake exponential Taper - terrible design
    # a = (1 / float(length)) * numpy.log(final_width / float(initial_width))
    #
    # previous_width = initial_width
    # for i in range(step, length, step):
    #     width = initial_width * numpy.exp(a * float(i))
    #     if (i == length-step):  # for the last iteration
    #         width = final_width
    #
    #     # print("Taper - i is %f \n\t a is %f \n\t exp is %f \n\t width is %f" % (i, a, numpy.exp(a * i), width))
    #     createPoly(width=previous_width, length=step, direction=direction, final_width=width)
    #     previous_width = width

    createPoly(width=initial_width, length = length, direction=direction, final_width=final_width)


# END of FUNCTION definitions
###################################################################################
# Constracting the actual design by using function defined above


cell = gdspy.Cell('PathCreator')
# #define chip
# position=Position.Position()
# createPoly(chip_length,chip_width)

# # #draw a structure
position = Position.Position(x=chip_width / 2, y=chip_length / 2 - edge_offset, angle=-numpy.pi / 2)

createPoly(width=t_final, length=l_final, direction='-y')
taper(initial_width=t_final, final_width=t_Zhigh, length=l_taper, direction='-y', step=step_polygon)  # tapering

createArc(t_Zhigh, R, -numpy.pi, -numpy.pi / 2)
createPoly(width=t_Zhigh, length=(chip_width - min_side_offset - R - position.x), direction='+x')

position.length = 0
position.direction = '+x'
meander_draw(total_length=l_Zhigh_edge - (l_Zlow/2) - (l_Zlow_short/2), width=t_Zhigh, step=step_polygon)

for i in range(number):  # number of repetitions
    print("Iteration %d" % (i + 1))
    position.length = 0  # before building new TL, the initial length should be set to zero
    meander_draw(total_length=l_Zlow, width=t_Zlow, step=step_polygon)
    position.length = 0
    meander_draw(total_length=l_Zhigh - l_Zlow, width=t_Zhigh, step=step_polygon)
    position.length = 0  # before building new TL, the initial length should be set to zero
    meander_draw(total_length=l_Zlow, width=t_Zlow, step=step_polygon)
    position.length = 0
    meander_draw(total_length=l_Zhigh - (l_Zlow/2) - (l_Zlow_short/2), width=t_Zhigh, step=step_polygon)
    position.length = 0
    meander_draw(total_length=l_Zlow_short, width=t_Zlow, step=step_polygon)
    position.length = 0
    meander_draw(total_length=l_Zhigh - (l_Zlow/2) - (l_Zlow_short/2), width=t_Zhigh, step=step_polygon)
    position.length = 0

# meander_draw(total_length=l_Zlow, width=t_Zlow, step=step_polygon)
last_meander_draw(t_Zhigh, step_polygon)

taper(initial_width=t_Zhigh, final_width=t_final, length=l_taper, direction='-y', step=step_polygon)  # tapering

l_final = chip_length / 2 - abs(position.y)
createPoly(width=t_final, length=l_final, direction='-y')

write()  # writing the final structure to gds file
