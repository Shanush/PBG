import numpy

filepath = 'C:/Users/Shanush/OneDrive - UNSW/Masters Thesis/Vissers Design'  # for Windows
# filepath = '/Users/mykhailo/Documents/UNSW/PBG'  #for Mac

# Parameters ##  ALL UNITS IN MICRONS

chip_length = 32000
chip_width = 26777.27

R_inner_low = 700 / 2  # radius for Round
R_inner_high = 900 / 2
R = 55  # radius for arc, const for low and high TL
d_angle = numpy.pi / 354  # arc builder step

gap = 1.5  # 0.5 for 50nm #1.5 for 20nm # gap between the Zlow and the ground plane   #30
w_gnd = 300  # width of the single ground plane for CPW structure

l_Zhigh = 720
l_Zhigh_edge = l_Zhigh
t_Zhigh = 1.5  # 0.5 for 50nm #1.5 for 20nm

l_Zlow = 64
l_Zlow_short = 34
t_Zlow = 5.5 # 2.5 for 50nm #5.5 for 20nm

number = 2339  # number of Zlow-Zhigh cascades from each side of the resonator in case of transimission line

w_c = 4  # C finger width
h_c = 100  # C finger height
w_sep = 4  # C finger separation
h_sep = 2  # C finger vertical distance from ground plane fingers to resonator
delta_x = 0  # offset for starting point of C fingers

c_gap = 0  # coupling capacitor separation
c_length = 0  # length of the polygon that has coupling capacitor

spec = {'layer': 1, 'datatype': 1, 'number_of_points': 0.9}  # finese of arc

spec_path = {'layer': 1, 'datatype': 1}  # standard specifications for Path polygon
spec_res = {'layer': 0, 'datatype': 1}  # standard specifications for Rectangular polygon used for Resonator creation
step_polygon = 0.125  # check stepper for polygon builder

edge_offset = 0  # free space left from the top of the chip before starting resonator
resonator_y_offset = 1200  # distance between the resonator and the start of meander in vertical direction
min_side_offset = 1000  # distance from the long side of the chip
angle_error = 2 * d_angle
last_meander_side_offset = chip_width / 2  # last meander side offset excluding radius of the bend

gap_final = 187.5
t_final = 300   #275  # the additional CPW for 50 Ohms match to PCB CPW-grounded
l_taper = 3500  # length of the tapered element  #
l_final = 1200  # length of the polygon after it was tapered, will be parametrised according to the chip length

filename = 'layout_20nm_inner_poster.gds' # 'layout_20nm_inner.gds'

# comment it out if not creating gnd plane
# l_Zhigh = l_Zhigh
# l_Zhigh_edge = l_Zhigh + gap  # only need gap on one side
# t_Zhigh = t_Zhigh + 2*gap
#
# l_Zlow = l_Zlow + 2*gap
# l_Zlow_short = l_Zlow_short + 2*gap
# t_Zlow = t_Zlow + 2*gap
#
# t_final = t_final + gap_final
#
# filename = 'layout_20nm_outer_poster.gds'

