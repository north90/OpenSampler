display=1;

Lx=480; //was 590 in Opensampler V2
Ly=315;	//was 380 in OpenSampler V2
Lz=200; // was 220 in Opensampler V2
La=140; //length of moving part on z-axis

in=25.4;
xs=20;

nema17holespac=31;
nema17diagholespac=43.84;

xyarm=28;
zyarm=Lz+xs+6;

backpanelthick=6.35;
frontpanelthick=6;
bottomthick=12.7;

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

// tallest bottle: 108, smallest bottle: 50
// minimum clearance: 10, spring action: 40
// vertical movement: 108-50+10+40=108

// FOR OpenSampler V3 try to get movement of 160*350mm (3 gc trays)
// no Cutout out the X-cart, even spacing off the wheels
// less z-height, smaller vials expected
// ordered vials of sigma 20ml supelco (23*75mm)
// also available are 27ml vials (30*60)



module E1x1(len){
	translate([0,0,0])
	difference(){
		translate([-xs/2,-xs/2,0])
		cube([xs,xs,len]);
		for ( i = [0 : 3] ){
			rotate([0,0,i*90])
			translate([-xs/2-1,-xs/8,-1])
			cube([xs/4,xs/4,len+2]);
		}
		translate([0,0,-1])
		cylinder(r=2.5,h=len+2);
	}	
}

module E1x2(len){
	translate([0,-xs*1/2,0]){
		E1x1(len);
		translate([0,xs,0])
		E1x1(len);
	}
}

module E1x3(len){
	translate([0,-xs*1,0]){
		E1x1(len);
		translate([0,xs,0])
		E1x1(len);
		translate([0,xs*2,0])
		E1x1(len);
	}
}

module wheel(){
	difference(){
		cylinder(r=12,h=11,center=true,$fn=25);
		cylinder(r=2.5,h=12,center=true);
	}
}

module mini_wheel(){
	difference(){
		cylinder(r=7.65,h=10,center=true);
		cylinder(r=2.5,h=12,center=true);
	}
}

// stepper nema 17, with some extra space around
module stepper(){ 
	difference(){
		union(){
			translate([-21,-21,-40])	
				cube([42,42,40],center=false);
			cylinder(r=2.5,h=30,center=false);
			cylinder(r=12,h=4,center=true);
			translate([-15.5,-15.5,0])
				cylinder(r=1.5,h=10,center=false);
			translate([15.5,-15.5,0])
				cylinder(r=1.5,h=10,center=false);
			translate([15.5,15.5,0])
				cylinder(r=1.5,h=10,center=false);
			translate([-15.5,15.5,0])
				cylinder(r=1.5,h=10,center=false);

			translate([0,0,10])
				cylinder(r=8,h=15,center=false);				
		}
	}
}

// stepper nema 17, with TR8-2 rod
module z_stepper(len){ 
	difference(){
		union(){
			translate([-22,-22,-40])	
				cube([44,44,40],center=false);
			cylinder(r=2.5,h=30,center=false);
			cylinder(r=12,h=4,center=true);
			translate([-15.5,-15.5,0])
				cylinder(r=1.5,h=10,center=false);
			translate([15.5,-15.5,0])
				cylinder(r=1.5,h=10,center=false);
			translate([15.5,15.5,0])
				cylinder(r=1.5,h=10,center=false);
			translate([-15.5,15.5,0])
				cylinder(r=1.5,h=10,center=false);
			translate([0,0,0])
				cylinder(r=4,h=len,center=false);					
		}
	}
}


module stepper_holes(){ 
	difference(){
		union(){
			translate([-21.5,-21.5,-49])	
				cube([43,43,49],center=false);
			cylinder(r=2.5,h=70,center=true);
			cylinder(r=14,h=10,center=false);
			cylinder(r=6,h=35,center=false);
			translate([-15.5,-15.5,0])
				cylinder(r=2,h=80,center=true);
			translate([15.5,-15.5,0])
				cylinder(r=2,h=80,center=true);
			translate([15.5,15.5,0])
				cylinder(r=2,h=80,center=true);
			translate([-15.5,15.5,0])
				cylinder(r=2,h=80,center=true);
		
		}
	}
}

module x_plate_top(){
	difference(){
		union(){
			translate([-5,-37,0])
			cube([115,76,4.8]);

			translate([(104+51.5)/2-21,35-24,0])
			cube([42,42,4.8]);						

			translate([2,-30,-12])
			wheel();
			translate([54,-30,-12])
			wheel();
			translate([104,-30,-12])
			wheel();

			translate([2,30,-12])
			wheel();
			translate([49,30,-12])
			wheel();
			translate([104,30,-12])
			wheel();
		}
		translate([2,-30,-1])
		cylinder(r=3.57,h=10);
		translate([54,-30,-1])
		cylinder(r=3.57,h=10);
		translate([104,-30,-1])
		cylinder(r=3.57,h=10);

		translate([2,30,-1])
		cylinder(r=2.5,h=10);
		translate([49,30,-1])
		cylinder(r=2.5,h=10);
		translate([104,30,-1])
		cylinder(r=2.5,h=10);


		translate([xyarm,0,-1]){
			translate([0,30,0])
			cylinder(r=2.5,h=10);
			translate([0,0,0])
			cylinder(r=2.5,h=10);
			translate([0,-25,0])
			cylinder(r=2.5,h=10);
		}

		translate([2,-3,0.5]){
			translate([0,-4.75,0])
			cylinder(r=1.5,h=10);
			translate([0,4.75,0])
			cylinder(r=1.5,h=10);
		}
	}	
}



module y_plate_top(){
	difference(){
		union(){
			translate([-36,-32,0])
			cube([36+113,64,3]);
			translate([-30,-20,-12])
			wheel();
			translate([30,-26,-12])
			wheel();
			translate([-30,26,-12])
			wheel();
			translate([30,26,-12])
			wheel();

			translate([-25,-25,0])
			cube([50,50,3]);
			translate([19,25.7,15])
			mini_wheel();
			translate([19,-25.7,15])
			mini_wheel();
			translate([-11,25.7,15])
			mini_wheel();
			translate([-11,-25.7,15])
			mini_wheel();
		}
		translate([60,0,-1])
		cylinder(r=2.5,h=10);

		translate([30,26,-1])
		cylinder(r=2.5,h=10);
		translate([30,-26,-1])
		cylinder(r=2.5,h=10);

		translate([-30,26,-1])
		cylinder(r=3.57,h=10);
		translate([-30,-20,-1])
		cylinder(r=3.57,h=10);


		translate([19,25.7,-1])
		cylinder(r=3.57,h=10);
		translate([19,-25.7,-1])
		cylinder(r=2.5,h=10);
		translate([-11,25.7,-1])
		cylinder(r=3.57,h=10);
		translate([-11,-25.7,-1])
		cylinder(r=2.5,h=10);

		translate([La-37,-30,-1]){
			translate([-4.75,0,0])
			cylinder(r=1.5,h=10);
			translate([4.75,0,0])
			cylinder(r=1.5,h=10);
		}


	}	


}
module y_plate_bottom(){
	difference(){
		union(){
			translate([35,0,0])
			cylinder(r=32,h=3);
			translate([35,-32,0])
			cube([32,32,3]);

		}

		translate([+30,-26,-1])
		cylinder(r=2,h=10);
		translate([+30,26,-1])
		cylinder(r=2,h=10);

		translate([+60,0,-1])
		cylinder(r=2,h=10);

		translate([0,-32,-1])
		cube([15,64,10]);

	}	
}



module z_motorplate(){
	difference(){
		union(){
			cylinder(r=32,h=3);
			translate([-32,-18.4,0])
			cube([64,18.4,3]);

			translate([-32,-18.4,-25])
			cube([64,3.2,25]);

		}
		translate([0,0,-1])
		cylinder(r=7,h=10);
		translate([0,0,1.5])
		cylinder(r=8.025,h=10);

		translate([nema17diagholespac/2,0,-1])
		cylinder(r=1.8,h=10);
		translate([-nema17diagholespac/2,0,-1])
		cylinder(r=1.8,h=10);
		translate([0,nema17diagholespac/2,-1])
		cylinder(r=1.8,h=10);

		translate([-10,-17-10,-1])
		cylinder(r=2.5,h=10);
		translate([10,-17-10,-1])
		cylinder(r=2.5,h=10);

		translate([-50,-118.4,-5])
		cube([100,100,10]);

	}
}

module gc_tray(){
	cube([120,188,20]);
}

module backpanel(){
	difference(){
		cube([Lx,backpanelthick,Lz-xs]);
		translate([xs+20,-1,xs+20+bottomthick])
		rotate([-90,0,0])
		cylinder(r=15,h=backpanelthick+2);

		translate([xs/2,-1,Lz-xs-20])
		rotate([-90,0,0])
		cylinder(r=2.55,h=backpanelthick+2);
		translate([xs/2,-1,xs+20])
		rotate([-90,0,0])
		cylinder(r=2.55,h=backpanelthick+2);

		translate([Lx-xs/2,-1,Lz-xs-20])
		rotate([-90,0,0])
		cylinder(r=2.55,h=backpanelthick+2);
		translate([Lx-xs/2,-1,xs+20])
		rotate([-90,0,0])
		cylinder(r=2.55,h=backpanelthick+2);

		translate([Lx/2,-1,xs/2])
		rotate([-90,0,0])
		cylinder(r=2.55,h=backpanelthick+2);
		
	}
}

module xcablecarrier(){
	translate([200,-xs,Lz-xs-76])
	cube([Lx-xs-200-2,xs+1, 6]);

}

module frontpanel(){
	difference(){
		translate([0,-xs*3-frontpanelthick,xs+bottomthick-2])
		cube([Lx,backpanelthick,Lz-xs*2-bottomthick+2]);

		translate([xs/2,-xs*3-frontpanelthick-1,xs+40])
		rotate([-90,0,0])
		cylinder(r=2.55,h=backpanelthick+2);
		translate([xs/2,-xs*3-frontpanelthick-1,Lz-xs-20])
		rotate([-90,0,0])
		cylinder(r=2.55,h=backpanelthick+2);

		translate([Lx-xs/2,-xs*3-frontpanelthick-1,xs+40])
		rotate([-90,0,0])
		cylinder(r=2.55,h=backpanelthick+2);
		translate([Lx-xs/2,-xs*3-frontpanelthick-1,Lz-xs-20])
		rotate([-90,0,0])
		cylinder(r=2.55,h=backpanelthick+2);
	}
}

module bottomplate(){
	difference(){
		translate([0,-Ly,xs])
		cube([Lx,Ly,bottomthick]);
		
		translate([-1,-xs*3,xs-1])
		cube([xs+1,3*xs+2,xs+2]);
		translate([Lx-xs,-xs*3,xs-1])
		cube([xs+1,3*xs+2,xs+2]);

		translate([xs/2,-Ly+xs*1.5,xs-1])
		cylinder(r=2.55,h=20);
		translate([Lx-xs/2,-Ly+xs*1.5,xs-1])
		cylinder(r=2.55,h=20);
		translate([Lx/2,-Ly+xs/2,xs-1])
		cylinder(r=2.55,h=20);

		translate([xs/2,-Ly/3,xs-1])
		cylinder(r=2.55,h=20);
		translate([Lx-xs/2,-Ly/3,xs-1])
		cylinder(r=2.55,h=20);

		translate([Lx/2,-xs/2,xs-1])
		cylinder(r=2.55,h=20);


		translate([-1,-xs*3-6.25,xs+bottomthick-2])
		cube([Lx+2,6.35,Lz]);

		translate([250,-xs*3-3.125,0]){
			translate([0,0,0])
			cylinder(r=2.55,h=100);
			translate([35,0,0])
			cylinder(r=2.55,h=100);
			translate([70,0,0])
			cylinder(r=2.55,h=100);
			translate([105,0,0])
			cylinder(r=2.55,h=100);
			translate([140,0,0])
			cylinder(r=2.55,h=100);
			translate([175,0,0])
			cylinder(r=2.55,h=100);
		}
	}
}

module arduino_mega_holes(){
	union(){
		cube([101,53,2]);
		
		translate([0.55*in,0.1*in,-50])
		cylinder(r=1.5,h=60);
		translate([0.6*in,2*in,-50])
		cylinder(r=1.5,h=60);

		translate([2.6*in,0.3*in,-50])
		cylinder(r=1.5,h=60);
		translate([2.6*in,1.4*in,-50])
		cylinder(r=1.5,h=60);

		translate([3.8*in,0.1*in,-50])
		cylinder(r=1.5,h=60);
		translate([3.55*in,2.0*in,-50])
		cylinder(r=1.5,h=60);
	}
}

module powersupply(){
	cube([130,32,50]);
}

module ramps(){
	union(){
		translate([-15,-8,0])
		cube([115,61,40]);
	}
}


if (display>0){
	//________________BASE____________________________
	
	translate([0,-xs/2,xs/2])
	rotate([0,90,0])
	E1x1(Lx);
	translate([0,xs/2-Ly,xs/2])
	rotate([0,90,0])
	E1x1(Lx);
	
	translate([0+xs/2,-xs,xs/2])
	rotate([90,0,0])
	E1x1(Ly-2*xs);
	translate([Lx-xs/2,-xs,xs/2])
	rotate([90,0,0])
	E1x1(Ly-2*xs);
	
	translate([xs/2,-1.5*xs,xs])
	E1x3(Lz-xs*2);
	translate([Lx-xs/2,-1.5*xs,xs])
	E1x3(Lz-xs*2);
	
	translate([0,-2*xs,-xs/2+Lz])
	rotate([0,90,0])
	E1x2(Lx);

	difference(){
		backpanel();
		translate([-1,10,0])
		xcablecarrier();
		translate([+1,10,0])
		xcablecarrier();

		translate([xs+20,-5,xs+bottomthick+60])
		rotate([90,0,0])
		translate([100,53,0])
		rotate([0,0,180])
		arduino_mega_holes();
	}


		
		
	xcablecarrier();
	
	translate([xs+60,-32-2,xs+bottomthick+3])
	powersupply();
		
	translate([0,-1,0])
	bottomplate();

	color([0.3,0.3,0.3,0.3])
	frontpanel();

	translate([85,-Ly+30,xs+12.5])
	gc_tray();
	
	translate([85+124,-Ly+30,xs+12.5])
	gc_tray();

	translate([85+248,-Ly+30,xs+12.5])
	gc_tray();

	translate([100,-Ly+2*xs+40,xs+12.5])
	cylinder(r=8,h=105);

	translate([100,-Ly+2*xs+90,xs+12.5])
	cylinder(r=11.5,h=75);

	translate([100,-Ly+2*xs+120,xs+12.5])
	cylinder(r=15,h=60);



	translate([0+355-350,0,0]){	
		//_________________X-AXIS_____________________________
		translate([xyarm,0,zyarm])
		rotate([90,0,0])
		//rotate([0,0,90])
		E1x2(Ly);
		
		translate([0,-xs*2,0]){
			difference(){
				translate([0,0,Lz+2])
				x_plate_top();
				translate([(104+51.5)/2,32,Lz+3+2+1.8])
				rotate([0,180,0])
				stepper_holes();
			}
	
			translate([(104+51.5)/2,32,Lz+3+2+1.8])
			rotate([0,180,0])
			stepper();
		}
		
		translate([0,-110-160+160,0]){
			// ________________Y_AXIS________________________________

			
			translate([xyarm+xs/2+2,0,zyarm])
			rotate([0,0,180])
			rotate([0,-90,0])
			y_plate_top();
			
			difference(){
				translate([xyarm-xs/2-2,0,zyarm])
				rotate([0,-90,0])
				y_plate_bottom();

				translate([xyarm-xs/2-9,0,zyarm+35+1])
				rotate([0,90,0])
				//rotate([0,0,45])
				stepper_holes();
			}

			translate([xyarm-xs/2-5,0,zyarm+35])
			rotate([0,90,0])
			//rotate([0,0,45])
			stepper();

			translate([xyarm+27,0,zyarm+116+0])
			rotate([0,180,45])
			z_stepper(120);


			translate([xyarm+27,0,zyarm+113])
			rotate([0,0,-90])
			z_motorplate();



			translate([0,0,-90]){
				//_____________Z_AXIS_______________________________

			translate([xyarm+xs+5+2,0,zyarm-20])
			E1x2(La);

			}	
		}
	}
}

//________________________________________________________________________________
// --------------------individual parts----------------------------------------
//
//$fn=40;
//projection(cut = true)
//translate([0,0,-1])

//y_plate_top();


// _________backpanel__________________
//translate([0,180,0])
//rotate([90,0,0])
//difference(){
//	backpanel();
//	translate([-1,10,0])
//	xcablecarrier();
//	translate([+1,10,0])
//	xcablecarrier();
//
//	translate([xs+20,-5,xs+bottomthick+60])
//	rotate([90,0,0])
//	translate([100,53,0])
//	rotate([0,0,180])
//	arduino_mega_holes();
//}



//_________________Bottomplate____________________
//translate([0,Ly,-xs])
//bottomplate();


//_____________frontpanel______________________
//translate([0,Lz-xs*2-bottomthick+2,0])
//rotate([90,0,0])
//translate([0,3*xs+6,-xs-bottomthick+2])
//frontpanel();


//
//translate([-241,132,16])
//rotate([0,90,0])
//			difference(){
//				translate([xyarm-xs/2-2,-100,zyarm])
//				rotate([0,-90,0])
//				y_plate_bottom();
//
//				translate([xyarm-xs/2-9,-100,zyarm+35+1])
//				rotate([0,90,0])
//				//rotate([0,0,45])
//				stepper_holes();
//			}



	//motorplate_on_top();

//				//translate([36,32,-1])
//				rotate([0,0,0])
//				difference(){
//				y_plate_top();
//
//				translate([45,0,-1])
//				rotate([0,0,45])
//				stepper_holes();
//			}

//
//translate([5,37,0])
//	difference(){
//		x_plate_top();
//		translate([(104+51.5)/2,32,3+2])
//		rotate([0,180,0])
//		stepper_holes();
//	}

