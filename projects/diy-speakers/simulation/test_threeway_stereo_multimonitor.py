"""Stereo monitor placement: measured-owner facts vs test assumptions.

This is geometry validation, not a certified acoustic measurement or stand.
"""
import math
import unittest
from pathlib import Path
from threeway_baffle_geometry import DRIVERS
from threeway_stereo_multimonitor import (
 USER_HEAD_MARK_M, CURRENT_32_TOP_M, CURRENT_27_SIDE_TOP_M,
 Monitor,Satellite,unit,dot,source_centers,source_ray_to_screen,
 stereo_lateral_x,true_equilateral_3d_lateral_x,stereo_angle,horizontal_stereo_angle,down_tilt,
 monitor_scenario,evaluate,scenario_report,array_basis
)


class StereoMultiMonitorTests(unittest.TestCase):
    def setUp(self):
        self.x=stereo_lateral_x(.70)
        self.left=Satellite("L",-self.x,.90,.7,90)
        self.right=Satellite("R",self.x,.90,.7,-90)

    def test_user_supplied_measured_heights_kept_exact(self):
        self.assertEqual(USER_HEAD_MARK_M,.60)
        self.assertEqual(CURRENT_32_TOP_M,.70)
        self.assertEqual(CURRENT_27_SIDE_TOP_M,.60)
        self.assertAlmostEqual(.70-.60,.10,places=12)

    def test_horizontal_stereo_triangle_is_symmetric(self):
        self.assertAlmostEqual(self.x,.7/math.sqrt(3),places=10)
        self.assertAlmostEqual(horizontal_stereo_angle([self.left,self.right]),60,places=9)
        self.assertAlmostEqual(down_tilt(self.left),down_tilt(self.right),places=11)
        self.assertLess(stereo_angle([self.left,self.right]),60)
        self.assertGreater(stereo_angle([self.left,self.right]),50)

    def test_true_equilateral_height_adjusts_stereo_base_and_included_angle(self):
        h=.92
        d=.70
        x=true_equilateral_3d_lateral_x(d,h)
        self.assertAlmostEqual(x,math.sqrt((d*d+(.92-.60)**2)/3),places=12)
        self.assertGreater(x,stereo_lateral_x(d))
        stereo=[Satellite("L",-x,h,d,90),Satellite("R",x,h,d,-90)]
        self.assertAlmostEqual(stereo_angle(stereo),60,places=10)
        self.assertGreater(horizontal_stereo_angle(stereo),60)
        full_distance=math.sqrt(x*x+d*d+(h-USER_HEAD_MARK_M)**2)
        self.assertAlmostEqual(full_distance,2*x,places=10)
        self.assertAlmostEqual(2*x,.889,delta=.002)
        with self.assertRaises(ValueError):
            true_equilateral_3d_lateral_x(.7,-1)

    def test_true_3d_pair_preserves_local_baffle_distances(self):
        a=source_centers(self.left)
        b=source_centers(Satellite("L",self.left.center_x_m,.90,.7,0))
        def distance(p,q):return math.sqrt(sum((x-y)**2 for x,y in zip(p,q)))
        for pair in (("LOW","MID"),("MID","HIGH"),("LOW","HIGH")):
            i,j=pair
            self.assertAlmostEqual(distance(a[i],a[j]),distance(b[i],b[j]),places=9)

    def test_yaw_pitch_roll_orthonormal(self):
        for s in (self.left,self.right):
            u,v,n=array_basis(s)
            for x in (u,v,n):
                self.assertAlmostEqual(dot(x,x),1,places=10)
            self.assertAlmostEqual(dot(u,v),0,places=10)
            self.assertAlmostEqual(dot(u,n),0,places=10)
            self.assertAlmostEqual(dot(v,n),0,places=10)

    def test_midpoint_intersection_makes_80cm_axis_not_clear_70cm_screen(self):
        screen=Monitor("32",0,.35,1.2,.70)
        # Central speaker ray, screen at 1/2 of 70cm depth
        mid=source_ray_to_screen((0,.80,.70),(0,.60,0),screen,.06,0)
        self.assertAlmostEqual(mid["source_h_at_screen_m"],.70)
        self.assertTrue(mid["center_blocked"])
        self.assertFalse(mid["full_flange_conservatively_clear"])

    def test_clearance_more_demanding_than_center_ray(self):
        screen=Monitor("big",0,.35,1.2,.70)
        for axis in (.8,.86,.90):
            ray=source_ray_to_screen((0,axis,.7),(0,.6,0),screen,.084,.02)
            if axis>=.9:
                self.assertFalse(ray["center_blocked"])
            self.assertFalse(ray["full_flange_conservatively_clear"] if axis<.925 else False)
        ray=source_ray_to_screen((0,.94,.7),(0,.6,0),screen,.084,.02)
        self.assertTrue(ray["full_flange_conservatively_clear"])

    def test_screen_behind_front_speakers_is_not_in_line_of_sight(self):
        screen=Monitor("monitor",0,.35,1.2,.7)
        x=source_ray_to_screen((.1,.82,.25),(0,.60,0),screen,.084)
        self.assertFalse(x["screen_is_between"])
        self.assertTrue(x["full_flange_conservatively_clear"])

    def test_monitor_angular_size_as_scenario_not_actual_reading(self):
        current=monitor_scenario("MEASURED_TOPS_32_27")
        future=monitor_scenario("FUTURE_54_CENTER_42_SIDES")
        self.assertEqual(len(current),2)
        self.assertEqual(len(future),3)
        self.assertTrue(all(v.measured_top for v in current))
        self.assertTrue(all(not v.measured_top and v.future_scenario for v in future))
        self.assertEqual(future[0].width_m,1.196)
        self.assertEqual(current[0].top_m,.70)

    def test_all_six_bands_checked_across_full_27point_ear_grid(self):
        r=evaluate([self.left,self.right],monitor_scenario("MEASURED_TOPS_32_27"))
        self.assertEqual(r["positions_checked"],27)
        self.assertLessEqual(r["two_speaker_all_six_faceplates_clear_count"],27)
        self.assertFalse(r["all_hardwares_physically_measured"])

    def test_moving_speaker_forward_of_displays_clears_ray_in_model(self):
        monitors=monitor_scenario("FUTURE_54_CENTER_42_SIDES")
        x=stereo_lateral_x(.10)
        speakers=[Satellite("L",-x,.85,.10,90),Satellite("R",x,.85,.10,-90)]
        result=evaluate(speakers,monitors)
        self.assertEqual(result["two_speaker_all_six_faceplates_clear_count"],27)
        # At 10cm listener depth the full cabinet may collide with head/arms,
        # obscure the monitor's image and fail stand stability. Ray clear
        # does NOT certify a practical or safe position.

    def test_explicit_missing_ear_height_and_future_tops_in_report(self):
        result=scenario_report()
        self.assertFalse(result["user_measured"]["ear_height_confirmed"])
        self.assertEqual(result["user_measured"]["head_reference_above_table_m"],.60)
        self.assertEqual(result["user_measured"]["central_32_monitor_top_above_table_m"],.70)
        self.assertEqual(result["unmeasured_assumptions"]["future_54_top_height_m"],.80)
        self.assertEqual(result["unmeasured_assumptions"]["future_42_sides_top_height_m"],.73)
        self.assertEqual(len(result["scenarios"]),300)
        sample=next(v for v in result["scenarios"]
          if v["monitor_configuration"]=="MEASURED_TOPS_32_27"
          and v["triangle_strategy"]=="TRUE_3D_EQUILATERAL"
          and v["speaker_depth_m"]==.70
          and v["nominal_acoustic_axis_height_m"]==.92
          and v["roll_deg"]==90)
        self.assertAlmostEqual(sample["base_to_ear_distance_ratio"],1.,places=6)
        self.assertAlmostEqual(sample["true_3d_stereo_included_angle_deg"],60.,places=5)

        self.assertTrue(all(
          r["visibility"]["complete_acoustic_diffraction_and_directionality"] is False
          for r in result["scenarios"]))

    def test_stereo_openscad_preview_is_labelled_nonproduction(self):
        scad=Path(__file__).with_name("threeway_stereo_multimonitor_scene.scad").read_text()
        self.assertIn("head_reference_height=.60",scad)
        self.assertIn("source_axis_height=.92",scad)
        self.assertIn('scenario="future"',scad)
        self.assertIn("speaker_roll_deg=90",scad)
        self.assertIn("show_supports=false",scad)
        self.assertIn('triangle_strategy="true_3d_equilateral"',scad)
        self.assertIn("function speaker_half_base()",scad)
        self.assertIn("displayed_screen(0,.35,1.196,.80)",scad)
        self.assertIn("displayed_screen(0,.35,.708,.70)",scad)
        self.assertIn("NOT a cut-ready baffle",scad)

    def test_invalid_monitor_and_bad_reference_fail(self):
        with self.assertRaises(ValueError):
            Monitor("bad",0,.35,-1,.7).validate()
        with self.assertRaises(ValueError):
            stereo_lateral_x(0)
        with self.assertRaises(ValueError):
            evaluate([self.left,self.left],monitor_scenario("MEASURED_TOPS_32_27"))
        with self.assertRaises(ValueError):
            evaluate([self.left,self.right],[],ear_height_m=-1)


if __name__=="__main__":
    unittest.main()
