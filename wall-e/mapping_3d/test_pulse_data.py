from unittest import TestCase
from mapping_3d.pulse_data import *

valid_xyz_coord_list_int = [1, 2, 3]
valid_xyz_coord_list_decimal = [1.0102, 2.24231, 3.12894123]
valid_xyz_coord_tuple_int = tuple(valid_xyz_coord_list_int)
valid_xyz_coord_tuple_decimal = tuple(valid_xyz_coord_list_decimal)

invalid_xyz_coord_int = 8
invalid_xyz_coord_string = "hey there"
invalid_xyz_coord_list_len = [2, 3, 4, 5]
invalid_xyz_coord_idx_0_not_number = ["hey", 1, 3]
invalid_xyz_coord_idx_1_not_number = [2, "yo", 3]
invalid_xyz_coord_idx_2_not_number = [2, 4, "aye"]
invalid_xyz_coord_all_3_not_number = ["hey", "yo", "aye"]
invalid_xyz_coord_zcoord_less_than_zero = [1, 2, -2]
invalid_xyz_coord_zcoord_is_zero = [1, 2, 0]

valid_radius_int = 3
valid_radius_decimal = 3.129302
invalid_radius_zero = 0
invalid_radius_string = "3.234"
invalid_radius_negative = -12.2

valid_brightness_zero = 0
valid_brightness_one = 1
valid_brightness_decimal = 0.23
invalid_brightness_string = "3.234"
invalid_brightness_less_than_zero = -12.2
invalid_brightness_greater_than_one = 1.23

# Example frame pulse data
# fpd = FramePulseData()
# for i in range(0, 12):
#     fpd.add_pulse_to_frame(i, PulseData([0, 0, 5], 0.2, 1), PulseData([2, 3, 10], 0.2, 1))
# for i in range(12, 23):
#     fpd.add_pulse_to_frame(i, PulseData([0, 0, 5], 0.2, 1), PulseData([2, 2, 3], 0.8, 1), PulseData([3, 3, 4], 0.1, 1))
# for i in range(23, 35):
#     fpd.add_pulse_to_frame(i, PulseData([2, 2, 3], 0.8, 1), PulseData([3, 3, 4], 0.2, 1))
# write_pulse_data_to_file(fpd)

# Example of frame pulse data from dark to bright
# if __name__ == '__main__':
#     fpd = FramePulseData()
#     for i in range(0, 100):
#         fpd.add_pulse_to_frame(i, PulseData([0, 0, 5], 0.2, i / 100.0))
#     write_frame_pulse_data_to_file(fpd)


class TestPulseData(TestCase):
    # xyz_coord tests

    def test_valid_xyz_coord_list_int(self):
        verify_xyz_coord_type(valid_xyz_coord_list_int)

    def test_valid_xyz_coord_list_decimal(self):
        verify_xyz_coord_type(valid_xyz_coord_list_decimal)

    def test_valid_xyz_coord_tuple_int(self):
        verify_xyz_coord_type(valid_xyz_coord_tuple_int)

    def test_valid_xyz_coord_tuple_decimal(self):
        verify_xyz_coord_type(valid_xyz_coord_tuple_decimal)

    def test_invalid_xyz_coord_int(self):
        self.assertRaises(TypeError, verify_xyz_coord_type, invalid_xyz_coord_int)

    def test_invalid_xyz_coord_string(self):
        self.assertRaises(TypeError, verify_xyz_coord_type, invalid_xyz_coord_string)

    def test_invalid_xyz_coord_list_len(self):
        self.assertRaises(ValueError, verify_xyz_coord_type, invalid_xyz_coord_list_len)

    def test_invalid_xyz_coord_idx_0_not_number(self):
        self.assertRaises(TypeError, verify_xyz_coord_type, invalid_xyz_coord_idx_0_not_number)

    def test_invalid_xyz_coord_idx_1_not_number(self):
        self.assertRaises(TypeError, verify_xyz_coord_type, invalid_xyz_coord_idx_1_not_number)

    def test_invalid_xyz_coord_idx_2_not_number(self):
        self.assertRaises(TypeError, verify_xyz_coord_type, invalid_xyz_coord_idx_2_not_number)

    def test_invalid_xyz_coord_all_3_not_number(self):
        self.assertRaises(TypeError, verify_xyz_coord_type, invalid_xyz_coord_all_3_not_number)

    def test_invalid_xyz_coord_zcoord_less_than_zero(self):
        self.assertRaises(ValueError, verify_xyz_coord_type, invalid_xyz_coord_zcoord_less_than_zero)

    def test_invalid_xyz_coord_zcoord_is_zeroo(self):
        self.assertRaises(ValueError, verify_xyz_coord_type, invalid_xyz_coord_zcoord_is_zero)

    # radius tests

    def test_valid_radius_int(self):
        verify_radius_value(valid_radius_int)

    def test_valid_radius_decimal(self):
        verify_radius_value(valid_radius_decimal)

    def test_invalid_radius_zero(self):
        self.assertRaises(ValueError, verify_radius_value, invalid_radius_zero)

    def test_invalid_radius_string(self):
        self.assertRaises(TypeError, verify_radius_value, invalid_radius_string)

    def test_invalid_radius_negative(self):
        self.assertRaises(ValueError, verify_radius_value, invalid_radius_negative)

    # brightness tests

    def test_valid_brightness_zero(self):
        verify_brightness_value(valid_brightness_zero)

    def test_valid_brightness_one(self):
        verify_brightness_value(valid_brightness_one)

    def test_valid_brightness_decimal(self):
        verify_brightness_value(valid_brightness_decimal)

    def test_invalid_brightness_string(self):
        self.assertRaises(TypeError, verify_brightness_value, invalid_brightness_string)

    def test_invalid_brightness_less_than_zero(self):
        self.assertRaises(ValueError, verify_brightness_value, invalid_brightness_less_than_zero)

    def test_invalid_brightness_greater_than_one(self):
        self.assertRaises(ValueError, verify_brightness_value, invalid_brightness_greater_than_one)

    # PulseData tests

    def test_valid_args_pulse_data(self):
        pd = PulseData(valid_xyz_coord_list_decimal, valid_radius_int, valid_brightness_decimal)
        self.assertEquals(pd.pulse_data[XYZ_COORD_LABEL], valid_xyz_coord_list_decimal)
        self.assertEquals(pd.pulse_data[RADIUS_LABEL], valid_radius_int)
        self.assertEquals(pd.pulse_data[BRIGHTNESS_LABEL], valid_brightness_decimal)

    def test_valid_args_pulse_data_converts_tuple_to_list(self):
        pd = PulseData(valid_xyz_coord_tuple_decimal, valid_radius_int, valid_brightness_decimal)
        self.assertEquals(pd.pulse_data[XYZ_COORD_LABEL], valid_xyz_coord_list_decimal)
        self.assertEquals(pd.pulse_data[RADIUS_LABEL], valid_radius_int)
        self.assertEquals(pd.pulse_data[BRIGHTNESS_LABEL], valid_brightness_decimal)

    # FramePulseData tests

    def test_fpd_str_is_correct(self):
        fpd = FramePulseData()
        fpd.add_pulse_to_frame(3,
                               PulseData(xyz_coord=[0, 0, 5], radius=0.2, brightness=1),
                               PulseData(xyz_coord=[2, 3, 10], radius=0.2, brightness=1))
        self.assertEquals(str(fpd.frame_pulse_data), "{3: [{'c': [0, 0, 5], 'r': 0.2, 'b': 1}, "
                                                     "{'c': [2, 3, 10], 'r': 0.2, 'b': 1}]}")

    def test_fpd_add_pulse_and_none_is_correct(self):
        fpd = FramePulseData()
        fpd.add_pulse_to_frame(3,
                               None,
                               PulseData(xyz_coord=[2, 3, 10], radius=0.2, brightness=1))
        self.assertEquals(str(fpd.frame_pulse_data), "{3: [{'c': [2, 3, 10], 'r': 0.2, 'b': 1}]}")

    def test_fpd_add_none_pulse_is_correct(self):
        fpd = FramePulseData()
        fpd.add_pulse_to_frame(3,
                               None,
                               None)
        self.assertEquals(str(fpd.frame_pulse_data), "{}")
