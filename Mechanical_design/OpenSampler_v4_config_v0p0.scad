in=25.4;
xs=20;

Lx=440; //was 590 in Opensampler V2,was 480 in Opensampler V3.03
Ly=285;	//was 380 in OpenSampler V2,was 315 in OpenSampler V3.03
Lz=240; // was 220 in Opensampler V2, was 200 in Opensampler V3.03
La=135; //length of moving part on z-axis, was 140 in Opensampler V3.03
LyPlate=169; // length of y-plate that z-axis moves on. was 169 in V3.10

nema17holespac=31;
nema17diagholespac=43.84;

xyarm=28;
zyarm=Lz+xs+6;

platethick=3.175;
backpanelthick=6.35;
frontpanelthick=6;
bottomthick=12.7;
belt_end_thick=4.8;

wheeloffset=12;
plateoffset=wheeloffset-10;

//distance from extrusion surface to bottom plate=2.2mm
// plates are about 2.8mm making plate surface 5mm of extrusion
//hole spacing for wheels: 40.64,60.64,80.64,100.64
// BETTER hole spacing for wheels: 40.0,60.0,80.0,100.0
// hole diam for fixed wheel:5mm, for eccentric: 7.14mm
// spacer block and acme block are 12mm thick.
// 125ml (100ml) bottle size: h=95mm, diam=52mm

// 60mm clearancy for needle and spings etc.
// so height between bottom frame and bottom z-axis:
// trayplate thickness + bottle h + 60
// 13 + 108 + 60 = 188mm

// tallest bottle: 155, smallest bottle: 105
// minimum clearance: 10, spring action: 40
// vertical movement: 155-105+10+30=90


// FOR OpenSampler V4 
// more z-height, 155mm 16mm diam vials expected
// ordered vials of KIMAX 16*150mm, which are 155mm high with cap
// change y cart to have 6 mini wheels for Z-axis
// fit 3 trays of 5*8 (103*160mm, 19mm spacing, 4mm edge)
