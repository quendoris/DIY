# Source notes · microscope discussion, 2026-10-20

**Provenance:** manually edited engineering record of the present project discussion. **Not a verbatim chat transcript**; full conversation export withheld because the repository currently has public visibility. Owner observations are kept separate from advertised specifications and proposals.

## Owner-supplied hardware and measurements

- LOMO Biolam S-11 / C11, marking 838612. Owner identifies mounted objectives as **8 0.20**, **40 0.65**, **MI 90 1.25**.
- External USB microscope camera labeled Digital Camera / High Speed Certified USB 2.0. USB ID **0ac8:3420**, Linux device name **MC50-B**, driver **uvcvideo**.
- Other equipment: Orange Pi Zero 3 with 4 GB RAM, Raspberry Pi 3 Model B v1.2, MCP4725, MP1584EN, WS2812 8-LED ring, white COB LEDs, TowerPro SG90 servos.
- Owner observed first visible COB emission near **7.36 V** and very bright light at **8 V**. **These are observations, not a 10-W current rating**.
- Turning the right focus knob to loosen it reduces movement resistance substantially. Load and backlash not measured.
- User wants dual-illumination heads with white and colored sources, high configurability from PC, separate transmitted/reflected modes, parked upper-light interlock.
- Upper head should move around object along azimuth arc, vertically along a smaller arc, and pitch independently. First prototype may be a fixed metal clamp/heatsink, then precision small actuators.
- Remove obsolete lower mirror/feed parts only after preserving/testing optical function of iris, field and auxiliary lenses.
- Motorize focus using externally coupled OpenSCAD gears/belt and replace stage with servo-driven X/Y and modern nonmetallic ESD-safe interchangeable fixtures.
- No ordinary manual controls; high motion precision, extremely quiet mechanics, one power supply; mandatory physical hardwired STOP and control software with motion audits.

## Owner's V4L2 output, not yet calibrated

- Video capture: /dev/video2; /dev/video3 exposes video metadata, not another camera.
- MJPEG 2592x1944 @15 FPS, 2048x1536 @15, 1920x1080 @15, 1024x768 @30, 640x480 @30 advertised.
- YUYV 2592x1944 @2 FPS, 1920x1080 @5, 1024x768 @10, 640x480 @30 advertised.
- Camera manual exposure menu mode 1, automatic mode 3; absolute exposure 3..10000 (inactive during auto). Automatic white balance and manual temperature menu; brightness, contrast, sharpness, gain and power-line controls.
- The current-format report showed 1920x1080 MJPEG @**30 FPS** despite format enumeration saying **15 FPS** at that resolution. Real capture must settle discrepancy.
- The manufacturer's 5-MP marketing claim is not yet an optical resolution test.

## Source references / limits

Biolam original series documentation: https://www.biolam.su/files/biolam.pdf
Biolam S-11 version mapping: https://www.zenit-npk.ru/fcatalog/info/49

Documented 230x140x360-mm maximum overall envelope does **not** determine fine geometry. Most current OpenSCAD dimensions are assumptions. No identified true sensor, LED operating current, safe workspace, gear dimensions, or actuator precision yet.
