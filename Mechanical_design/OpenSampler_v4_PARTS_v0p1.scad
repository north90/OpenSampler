include <OpenSampler_v4_config_v0p0.scad>;
$fn=32;


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

// Main plate for x-axis movement 4.8mm aluminum (3/16")
module x_plate_top(){
	difference(){
		union(){
			translate([-5,-37,0])
			cube([115,76,4.8]);

			translate([(104+51.5)/2-21,35-24,0])
			cube([42,42,4.8]);				
            
            // wheels are just for display
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
        // holes for adjustable wheels
		translate([2,-30,-1])
		cylinder(r=3.57,h=10);
		translate([54,-30,-1])
		cylinder(r=3.57,h=10);
		translate([104,-30,-1])
		cylinder(r=3.57,h=10);

        // holes for M5 thread for wheels
		translate([2,30,-1])
		cylinder(r=2.1,h=10);
		translate([49,30,-1])
		cylinder(r=2.1,h=10);
		translate([104,30,-1])
		cylinder(r=2.1,h=10);

        // holes for attachment y-arm
		translate([xyarm,0,-1]){
			translate([0,30,0])
			cylinder(r=2.5,h=10);
			translate([0,0,0])
			cylinder(r=2.5,h=10);
			translate([0,-25,0])
			cylinder(r=2.5,h=10);
		}
        // pocket for secure attachment of y-arm
		translate([xyarm,0,0])        
        translate([-10,-50,3.2])
        cube([20,100,10]);

        // holes for 20mm endstop switch
		translate([2,-3,-1]){
			translate([0,-4.75,0])
			cylinder(r=1.2,h=10);
			translate([0,4.75,0])
			cylinder(r=1.2,h=10);
		}
        // holes for stepper motor
        translate([(104+51.5)/2,32,4.8+0.1])
        rotate([0,180,0])
        stepper_holes();

	}
	
}



module y_plate_top(){
	difference(){
		union(){
			translate([-36,-32,0])
			cube([LyPlate,64,platethick]);
			translate([-30,-20,-12])
			wheel();
			translate([30,-26,-12])
			wheel();
			translate([-30,26,-12])
			wheel();
			translate([30,26,-12])
			wheel();

			translate([50,25.7,15])
			mini_wheel();
			translate([50,-25.7,15])
			mini_wheel();
			translate([-25,-25,0])
			cube([50,50,3]);
			translate([17,25.7,15])
			mini_wheel();
			translate([17,-25.7,15])
			mini_wheel();
			translate([-16,25.7,15])
			mini_wheel();
			translate([-16,-25.7,15])
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


		translate([50,25.7,-1])
		cylinder(r=3.57,h=10);
		translate([50,-25.7,-1])
		cylinder(r=2.5,h=10);
		translate([17,25.7,-1])
		cylinder(r=3.57,h=10);
		translate([17,-25.7,-1])
		cylinder(r=2.5,h=10);
		translate([-16,25.7,-1])
		cylinder(r=3.57,h=10);
		translate([-16,-25.7,-1])
		cylinder(r=2.5,h=10);

		translate([LyPlate-36-10,-30,-1]){
			translate([-4.75,0,0])
			cylinder(r=1.2,h=10);
			translate([4.75,0,0])
			cylinder(r=1.2,h=10);
		}
 		translate([LyPlate-36,0,-1]){ 
 			translate([-15,-15,0])
			cylinder(r=2.1,h=10);
			translate([-15,15,0])
			cylinder(r=2.1,h=10);     
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
        // holes for M5 thread to attach to y_plate_top
		translate([+30,-26,-1])
		cylinder(r=2.1,h=10);
		translate([+30,26,-1])
		cylinder(r=2.1,h=10);

		translate([60,0,-1])
		cylinder(r=2.1,h=10);

        // cut not needed part off
		translate([0,-32,-1])
		cube([15,64,10]);

        //holes for stepper motor
        translate([36,0,-1])
        stepper_holes();
        
        // hole for cable carrier
        translate([59,-26,-1])
        cylinder(r=2.1,h=100);
	}	
}



module z_motorplate(){
	difference(){
		union(){
            translate([0,-5,0])
			cylinder(r=32,h=platethick);
			translate([-32,-(xs/2+plateoffset+platethick*2),0])
			cube([64,(xs/2+plateoffset+platethick*2)-5,platethick]);

			translate([-32,-18.4,-25])
			cube([64,platethick,25]);
		}
        translate([-35,21,-1])
        cube([70,50,platethick+2]);
        
        // for acme T8 stepper
 		translate([0,0,-1])
		cylinder(r=12,h=10);       

        //holes for 0 deg stepper
 		translate([nema17holespac/2,nema17holespac/2,-1])
		cylinder(r=1.8,h=10);
		translate([-nema17holespac/2,nema17holespac/2,-1])
		cylinder(r=1.8,h=10);       

		translate([-10,-17-10,-1])
		cylinder(r=2.5,h=10);
		translate([10,-17-10,-1])
		cylinder(r=2.5,h=10);

		translate([-50,-118.4,-5])
		cube([100,100,10]);
        
      //holes for connecting to y_plate
        translate([-15,-20,-15])
        rotate([-90,0,0])
        cylinder(r=2.5,h=100);
        translate([15,-20,-15])
        rotate([-90,0,0])
        cylinder(r=2.5,h=100);

	}

}

module belt_end_plate(){
    difference(){
            translate([-20,-10,0])
            cube([40,20,belt_end_thick]);
            //deep under belt
            translate([-10,0,-1])
            cylinder(r=2.55,h=10);
            translate([-10,0,1.3])
            cylinder(r=4.55,h=10);
            // normal
            translate([10,0,-1])
            cylinder(r=2.55,h=10);           
            translate([10,0,3.3])
            cylinder(r=4.55,h=10);   
            // belt clamp screws
            translate([0,5,-1])
            cylinder(r=2,h=10);           
            translate([0,5,3])
            cylinder(r=4.55,h=10);
            translate([0,-5,-1])
            cylinder(r=2,h=10);           
            translate([0,-5,3])
            cylinder(r=4.55,h=10);  
        
            //belt holes
            translate([-16.5,2,-1])
            cylinder(r=1.5,h=10);           
            translate([-16.5,-2,-1])
            cylinder(r=1.5,h=10);      
            translate([3.5,2,-1])
            cylinder(r=1.5,h=10);           
            translate([3.5,-2,-1])
            cylinder(r=1.5,h=10); 
            translate([-18,-2,-1])
            cube([3,4,10]);
            translate([2,-2,-1])
            cube([3,4,10]);
            
            translate([-16.5,-3.5,2.8])
            cube([20,7,10]);
        
    }
}

module belt_end_plate_x(){
    difference(){
            union(){
                translate([-20,-10,0])
                cube([40,20,belt_end_thick]);
                translate([0,10,0])
                cylinder(r=19.99,h=belt_end_thick);
            }
                 
            //deep under belt
            translate([-10,0,-1])
            cylinder(r=2.55,h=10);
            translate([-10,0,1.3])
            cylinder(r=4.55,h=10);
            // normal
            translate([10,0,-1])
            cylinder(r=2.55,h=10);           
            translate([10,0,3.3])
            cylinder(r=4.55,h=10);   
            // belt clamp screws
            translate([0,5,-1])
            cylinder(r=2,h=10);           
            translate([0,5,3])
            cylinder(r=4.55,h=10);
            translate([0,-5,-1])
            cylinder(r=2,h=10);           
            translate([0,-5,3])
            cylinder(r=4.55,h=10);  
        
            //belt holes
            translate([-16.5,2,-1])
            cylinder(r=1.5,h=10);           
            translate([-16.5,-2,-1])
            cylinder(r=1.5,h=10);      
            translate([3.5,2,-1])
            cylinder(r=1.5,h=10);           
            translate([3.5,-2,-1])
            cylinder(r=1.5,h=10); 
            translate([-18,-2,-1])
            cube([3,4,10]);
            translate([2,-2,-1])
            cube([3,4,10]);
            
            translate([-16.5,-3.5,2.8])
            cube([20,7,10]);
        
    }
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
	translate([200,-xs,Lz-xs-80])
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

module needle_mount_bottom(){
	difference(){
		union(){
			translate([-20,0,0])
			cube([40,32,9.5]);
	
		}
		translate([-21,18,5])
		cube([42,30,9.5]);	
	
		translate([-9,9,-1])
		cylinder(r=2.1,h=100);
		translate([9,9,-1])
		cylinder(r=2.1,h=100);
	
		translate([-10,24,-1])
		cylinder(r=2.55,h=100);
		translate([10,24,-1])
		cylinder(r=2.55,h=100);
		translate([-10,24,3.2])
		cylinder(r=4.75,h=100);
		translate([10,24,3.2])
		cylinder(r=4.75,h=100);
	
	
		translate([0,-1,10])
		rotate([-90,0,0])
		cylinder(r=3.5,h=3.5);
		
		
		translate([0,2.45,10])
		rotate([-90,0,0])
		cylinder(r=6.4,h=9.3+2.55,$fn=6);
	
		translate([0,14,10])
		rotate([-90,0,0])
		cylinder(r=4,h=3);
	
		translate([0,16,10])
		rotate([-90,0,0])
		cylinder(r=7,h=100);	



		translate([-15,-1,9.7])
		rotate([-90,0,0])
		cylinder(r=3.4,h=100);	
		translate([15,-1,9.7])
		rotate([-90,0,0])
		cylinder(r=3.4,h=100);
	}
}

module needle_mount_top(){
	difference(){
		union(){
			translate([-20,0,0])
			cube([40,18,9.5]);
	
		}
	
		translate([-9,9,-1])
		cylinder(r=2.5,h=100);
		translate([9,9,-1])
		cylinder(r=2.5,h=100);
	
		translate([-10,24,-1])
		cylinder(r=2.55,h=100);
		translate([10,24,-1])
		cylinder(r=2.55,h=100);
		translate([-10,24,3.2])
		cylinder(r=4.75,h=100);
		translate([10,24,3.2])
		cylinder(r=4.75,h=100);
	
	
		translate([0,-1,10])
		rotate([-90,0,0])
		cylinder(r=3.5,h=3.5);
		
		
		translate([0,2.45,10])
		rotate([-90,0,0])
		cylinder(r=6.4,h=9.3+2.55,$fn=6);
	
		translate([0,14,10])
		rotate([-90,0,0])
		cylinder(r=4,h=3);
	
		translate([0,16,10])
		rotate([-90,0,0])
		cylinder(r=7,h=100);	

		translate([-15,-1,9.7])
		rotate([-90,0,0])
		cylinder(r=3.4,h=100);	
		translate([15,-1,9.7])
		rotate([-90,0,0])
		cylinder(r=3.4,h=100);
	}
}

module spring_support_plate(){
    difference(){
        linear_extrude(height=12.7, convexity = 10)
        polygon(points=[[-20,-10],[20,-10],[20,-5],[16,-1],[16,1],[20,5],[20,20],
        [18,24],[12,24],[8,10],[-8,10],[-12,24],[-18,24],[-20,20],[-20,10],
        [-20,5],[-16,1],[-16,-1],[-20,-5]]);
       
        // slight oversized holes for 4mm brass vertical rod of spring plate
        translate([-15,20,-1])
        cylinder(r=2.05,h=100); 
        translate([15,20,-1])
        cylinder(r=2.05,h=100); 
        
        // M5 screw holes and countersinks
        translate([-10,0,-1])
        cylinder(r=2.5,h=100); 
        translate([10,0,-1])
        cylinder(r=2.5,h=100); 
        translate([-10,0,-1])
        cylinder(r=4.75,h=3); 
        translate([10,0,-1])
        cylinder(r=4.75,h=3); 
        
        translate([-21,-11,6.35])
        cube([42,21.01,100]);
       
        // optional center hole for too long trapezium rod on z-stepper motor
        //translate([0,0,-1])
        //cylinder(r=4.5,h=100);
    }   
}

module spring_support_plate_top(){
    difference(){
        translate([-20,-16,0])
        cube([40,16,12.7]);
        
        //center cut-out for sample tubing
        translate([-4,-17,-1])
        cube([8,8,100]);
        translate([0,-17+8,-1])
        cylinder(r=4,h=100); 
       
        // slight oversized holes for 4mm brass vertical rod of spring plate
        translate([-15,-10,-1])
        cylinder(r=2.05,h=100); 
        translate([15,-10,-1])
        cylinder(r=2.05,h=100); 
        
        // M5 screw holes and countersink
        translate([-10,-50,6.35])
        rotate([-90,0,0])
        cylinder(r=2.5,h=100); 
        translate([10,-50,6.35])
        rotate([-90,0,0])
        cylinder(r=2.5,h=100); 
        translate([-10,-17,6.35])
        rotate([-90,0,0])
        cylinder(r=4.75,h=3); 
        translate([10,-17,6.35])
        rotate([-90,0,0])
        cylinder(r=4.75,h=3); 
        
        

    }   
}
module spring_plate(){
    difference(){
        union(){
            cylinder(r=7,h=12.7);
            translate([0,0,6.35])
            scale([1,0.5,1])
            cylinder(r=20,h=6.35);
        }
        translate([0,0,-1])
        cylinder(r1=1.6,r2=6,h=14.7); 
        
        translate([-15,0,-1])
        cylinder(r=1.7,h=100); 
        translate([15,0,-1])
        cylinder(r=1.7,h=100);
    }        
    
}

module end_stop_holder(){
    difference(){
        translate([0,-7,0])
        cube([32,14,5]);
        
        translate([4.5,0,-1])
        cylinder(r=2.55,h=10);
        translate([4.5,-2.55,-1])
        cube([4,5.1,10]);
        translate([8.5,0,-1])
        cylinder(r=2.55,h=10);       
    
        translate([23-4.75,0,-1])
        cylinder(r=1.7,h=10);    
        translate([23+4.75,0,-1])
        cylinder(r=1.7,h=10); 
        
        translate([23-4.75,0,-1])
        cylinder(r=3.5,h=4);    
        translate([23+4.75,0,-1])
        cylinder(r=3.5,h=4); 
    }
}

module solenoid_plate(){
    difference(){
        union(){
            cylinder(r=8.5,h=4.8);
            translate([-16,-5,0])
            cube([32,10,4.8]);
        }
        translate([-12.5,0,-1])
        cylinder(r=2.1,h=10);
        translate([12.5,0,-1])
        cylinder(r=2.1,h=10);        
        
        translate([3/16*in,0,-1])
        cylinder(r=1.8,h=10);
        translate([-3/16*in,0,-1])
        cylinder(r=1.8,h=10);            

        translate([3/16*in,0,1.3])
        cylinder(r=3.2,h=4);
        translate([-3/16*in,0,1.3])
        cylinder(r=3.2,h=4);         
    }    
}

//________________________________________________________________________________
// --------------------individual parts----------------------------------------
//
//$fn=128;
//projection(cut = true){
    solenoid_plate();
//}
//needle_mount_top();

//translate([36,32,-1])
//
//x_plate_top();

//translate([36,32,-1])
//y_plate_top();
//y_plate_bottom();

//y_plate_bottom();


// TOP CUT Z_MOTORPLATE
//translate([32,18.4,-2.5])
//z_motorplate();
//}

// SIDE CUT Z_MOTORPLATE
//translate([0,0,1])
//rotate([-90,0,0])
//translate([32,18.4,-3])
//z_motorplate();
//}
//
//translate([20,10,-4])
//spring_support_plate();
//
//translate([20,10,-10])
//rotate([180,0,0])
//spring_plate();
//
//translate([20,16,-1])
//spring_support_plate_top();
//}

//end_stop_holder();

// _________backpanel__________________
//translate([0,40,0])
//translate([0,180,0])
//rotate([90,0,0])
//difference(){
//	backpanel();
//	translate([-1,10,0])
//	xcablecarrier();
//	translate([+1,10,0])
//	xcablecarrier();
//
//	translate([xs+20,-5,xs+bottomthick+70])
//	rotate([90,0,0])
//	translate([100,53,0])
//	rotate([0,0,180])
//	arduino_mega_holes();
//}
//
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

//belt_end_plate_x();