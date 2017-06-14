//active tray on bruker 450-gc:
// bottom_thick= 18.8;
// middle_thick=6.1;
// top_thick=12.2;
// standoff=44;
// tray_size_x=187.5;
// tray_size_y=119.64;
// hole_diam_middle=15.8;
// hole_diam_top=16.8;
// hole_diam_septa=9.5;
//standoff_diam=7;
// standoff screws #10 -24 coarse countersunk 2.25in
// standoff tube od=7mm (max could be 8mm)




tube_diam=16.5; //diam including gap
tube_top_diam= 17.0; //diam top incl gap
tube_septum_diam= 10; //diam top incl gap
tube_spacing=19.0; // 
bottom_hole_diam=10;

amount_x=5;
amount_y=8;
edge_width_x=4;
edge_width_y=4;

in=25.4;

height_bottom=12.7;
height_top=1/2*in;
height_top_inner=15;
height_top_straight=6;
tube_top_diam_big= 17;

round_corner_r=6.35;

height_solid_bottom=2;
height_solid_top=1.5;

height_middle=12.7;

spacer_hole_diam_bottom=4.2;
spacer_hole_diam_middle=5;
spacer_diam=3/8*in;
spacer_height=75;
tray_height=155;

tray_spacing=6;
$fn=30;


tray_size_x=amount_x*tube_spacing+edge_width_x*2;
tray_size_y=amount_y*tube_spacing+edge_width_y*2;

echo(str("Tray X size: ",tray_size_x, "mm"));
echo(str("Tray Y size: ",tray_size_y, "mm"));

module tray() {
	difference(){
        rounded_cube(amount_x*tube_spacing+edge_width_x*2, amount_y*tube_spacing+edge_width_y*2,height_bottom,round_corner_r);

		for ( j = [1 : amount_y] ) {
			translate(v=[0,edge_width_y+tube_spacing*j-tube_spacing/2,0]){
				for ( i = [1 : amount_x] ) {
					translate([edge_width_x + tube_spacing*i - tube_spacing/2,0, height_solid_bottom]) 
					cylinder(r =tube_diam/2, h=height_bottom);

					translate([edge_width_x + tube_spacing*i - tube_spacing/2,0, -1]) 
					cylinder(r =bottom_hole_diam/2, h=height_bottom);
				 } 
			}
		}
		translate([edge_width_x+tube_spacing,edge_width_y+tube_spacing,height_solid_bottom])
		cylinder(r=spacer_hole_diam_bottom/2,h=height_bottom);
		translate([edge_width_x+tube_spacing*(amount_x-1),edge_width_y+tube_spacing,height_solid_bottom])
		cylinder(r=spacer_hole_diam_bottom/2,h=height_bottom);
		translate([edge_width_x+tube_spacing*(amount_x-1),edge_width_y+tube_spacing*(amount_y-1),height_solid_bottom])
		cylinder(r=spacer_hole_diam_bottom/2,h=height_bottom);
		translate([edge_width_x+tube_spacing,edge_width_y+tube_spacing*(amount_y-1),height_solid_bottom])
		cylinder(r=spacer_hole_diam_bottom/2,h=height_bottom);

	}
}

module tray_top() {
	difference(){
		union(){
            rounded_cube(amount_x*tube_spacing+edge_width_x*2, amount_y*tube_spacing+edge_width_y*2,height_top,round_corner_r);
		}

		translate(v=[edge_width_x+tube_spacing/2,edge_width_y+tube_spacing/2,height_top_inner])
		cube(size=[(amount_x-1)*tube_spacing,(amount_y-1)*tube_spacing,100],center=false);	
		for ( j = [1 : amount_y] ) {
			translate(v=[0,edge_width_y+tube_spacing*j-tube_spacing/2,0]){
				for ( i = [1 : amount_x] ) {
					translate([edge_width_x +tube_spacing*i - tube_spacing/2,0, height_solid_top]) 
					cylinder(r =tube_top_diam/2, h=height_top);
					translate([edge_width_x +tube_spacing*i - tube_spacing/2,0,height_top_straight+0.1])
					cylinder(h =height_top_inner-height_top_straight , r1 = tube_top_diam/2, r2 = tube_top_diam_big/2); 
					translate([edge_width_x +tube_spacing*i - tube_spacing/2,0,height_top_inner])
					cylinder(h =100 , r=tube_top_diam_big/2);
				 } 
			}
		}
		for ( j = [1 : amount_y] ) {
			translate(v=[0,edge_width_y+tube_spacing*j-tube_spacing/2,0]){
				for ( i = [1 : amount_x] ) {
					translate([edge_width_x +tube_spacing*i - tube_spacing/2,0,-1]) 
					cylinder(r =tube_septum_diam/2, h=height_bottom);
				 } 
			}
		}
	}
}

module tray_middle() {
	difference(){
		union(){
            rounded_cube(amount_x*tube_spacing+edge_width_x*2, amount_y*tube_spacing+edge_width_y*2,height_middle,round_corner_r);
		}

		translate([edge_width_x+tube_spacing,edge_width_y+tube_spacing,-1])
		cylinder(r=spacer_hole_diam_middle/2,h=height_middle+2);
		translate([edge_width_x+tube_spacing*(amount_x-1),edge_width_y+tube_spacing,-1])
		cylinder(r=spacer_hole_diam_middle/2,h=height_middle+2);
		translate([edge_width_x+tube_spacing*(amount_x-1),edge_width_y+tube_spacing*(amount_y-1),-1])
		cylinder(r=spacer_hole_diam_middle/2,h=height_middle+2);
		translate([edge_width_x+tube_spacing,edge_width_y+tube_spacing*(amount_y-1),-1])
		cylinder(r=spacer_hole_diam_middle/2,h=height_middle+2);


		for ( j = [1 : amount_y] ) {
			translate(v=[0,edge_width_y+tube_spacing*j-tube_spacing/2,0]){
				for ( i = [1 : amount_x] ) {
					translate([edge_width_x + tube_spacing*i - tube_spacing/2,0, -1]) 
					cylinder(r =tube_diam/2, h=height_middle+2);
				 } 
			}
		}
	}
}

module rounded_cube(cx,cy,cz,cr){
    union(){
        translate([cr,0,0])
        cube([cx-cr*2,cy,cz]);	
        translate([0,cr,0])
        cube([cx,cy-cr*2,cz]);
        translate([cr,cr,0])
        cylinder(r=cr,h=cz);
        translate([cx-cr,cr,0])
        cylinder(r=cr,h=cz);
        translate([cr,cy-cr,0])
        cylinder(r=cr,h=cz);
        translate([cx-cr,cy-cr,0])
        cylinder(r=cr,h=cz);
    }   
}


module spacers(){
	translate([edge_width_x+tube_spacing,edge_width_y+tube_spacing,height_bottom])
	difference(){
		cylinder(r=spacer_diam/2,h=spacer_height);
		translate([0,0,-1])
		cylinder(r=spacer_hole_diam_middle/2,h=spacer_height+2);
	}
	translate([edge_width_x+tube_spacing*(amount_x-1),edge_width_y+tube_spacing,height_bottom])
	difference(){
		cylinder(r=spacer_diam/2,h=spacer_height);
		translate([0,0,-1])
		cylinder(r=spacer_hole_diam_middle/2,h=spacer_height+2);
	}
	translate([edge_width_x+tube_spacing*(amount_x-1),edge_width_y+tube_spacing*(amount_y-1),height_bottom])
	difference(){
		cylinder(r=spacer_diam/2,h=spacer_height);
		translate([0,0,-1])
		cylinder(r=spacer_hole_diam_middle/2,h=spacer_height+2);
	}
	translate([edge_width_x+tube_spacing,edge_width_y+tube_spacing*(amount_y-1),height_bottom])
	difference(){
		cylinder(r=spacer_diam/2,h=spacer_height);
		translate([0,0,-1])
		cylinder(r=spacer_hole_diam_middle/2,h=spacer_height+2);
	}
}


module assembled_tray(){
    tray();
    
    translate([0,0,height_bottom+spacer_height])
    tray_middle();
    
    spacers();
    
}

module tray_outline(){
    rounded_cube(amount_x*tube_spacing+edge_width_x*2, amount_y*tube_spacing+edge_width_y*2,height_middle,round_corner_r);
}  
    
module tray_holder(){    
    difference(){
        rounded_cube(tray_size_x*3+12*2+tray_spacing*2,tray_size_y+12*2,9.5,round_corner_r);
        
        translate([12+tray_size_x/2,6,-1])
        cylinder(r=2.5,h=100);
        translate([12+tray_size_x*2.5+tray_spacing*2,6,-1])
        cylinder(r=2.5,h=100);        
        translate([12+tray_size_x/2,tray_size_y+12+6,-1])
        cylinder(r=2.5,h=100);
        translate([12+tray_size_x*2.5+tray_spacing*2,tray_size_y+12+6,-1])
        cylinder(r=2.5,h=100);     
        translate([12,12,-1]){
            tray_outline();
            translate([109,0,0])
            tray_outline();
            translate([109*2,0,0])
            tray_outline();
        } 
     
    }
    
}
//____________ASSEMBLY_________________________

//tray();
//
//translate([0,tray_size_y,tray_height])
//rotate([180,0,0])
//tray_top();
//
//translate([0,0,height_bottom+spacer_height])
//tray_middle();
//
//spacers();

//
//$fn=32;
//projection(cut = true) {
	translate([tray_size_y,0,-2])
	rotate([0,0,90])
    tray_middle();

	translate([tray_size_y,(tray_size_x+7.5)*1,-2])
	rotate([0,0,90])
    tray_middle();

    
//translate([0,0,-2])
//tray_holder();
//}
//
//	translate([tray_size_y,tray_size_x+8,-2])
//	rotate([0,0,90])
//
//	tray_middle();
//}
