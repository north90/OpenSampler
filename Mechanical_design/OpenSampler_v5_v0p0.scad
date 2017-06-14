include <OpenSampler_v5_CONFIG_v0p0.scad>;
use <OpenSampler_v5_PARTS_v0p0.scad>;
use <20150613_16mm_tube_tray_v0p0.scad>;


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

translate([Lx,-2*xs,-xs/2+Lz])
rotate([0,90,0])
rotate([0,0,-90])
belt_end_plate();

translate([0,-2*xs,-xs/2+Lz])
rotate([0,-90,0])
rotate([0,0,-90])
belt_end_plate_x();

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



first_tray_x=95;

translate([first_tray_x-12,-Ly+26-12,xs+12.5])
tray_holder();

translate([first_tray_x,-Ly+26,xs+12.5])
assembled_tray();

translate([first_tray_x+109,-Ly+26,xs+12.5])
assembled_tray();

translate([first_tray_x+218,-Ly+26,xs+12.5])
assembled_tray();


translate([first_tray_x+4+19/2,-Ly+26+4+19/2,xs+12.5])
cylinder(r=8,h=155);
translate([first_tray_x+4+19/2,-Ly+26+4+19*7.5,xs+12.5])
cylinder(r=8,h=155);
translate([first_tray_x+4+19/2,-Ly+26+4+19*1.5,xs+12.5])
cylinder(r=8,h=130);
translate([first_tray_x+4+19/2,-Ly+26+4+19*6.5,xs+12.5])
cylinder(r=8,h=130);



translate([7+320-320,0,0]){	
    //_________________X-AXIS_____________________________
    translate([xyarm,0,zyarm])
    rotate([90,0,0])
    //rotate([0,0,90])
    E1x2(Ly);
    
    translate([xyarm,-Ly,zyarm])
    rotate([90,0,0])
    rotate([0,0,-90])
    belt_end_plate();
    
    translate([xyarm,0,zyarm])
    rotate([-90,0,0])
    rotate([0,0,90])
    belt_end_plate();
    
    translate([0,-xs*2,0]){
        translate([0,0,Lz+2])
        x_plate_top();

        translate([(104+51.5)/2,32,Lz+3+2+1.8+1])
        rotate([0,180,0])
        stepper();
    }
    
    translate([xyarm+10,-49,zyarm-10])
    rotate([0,90,0])
    rotate([0,0,-90])   
    end_stop_holder();
    
    translate([0,-110-138+138,0]){
        // ________________Y_AXIS________________________________

        
        translate([xyarm+xs/2+plateoffset,0,zyarm])
        rotate([0,0,180])
        rotate([0,-90,0])
        y_plate_top();
        
        translate([xyarm-xs/2-plateoffset,0,zyarm])
        rotate([0,-90,0])
        y_plate_bottom();


        translate([xyarm-xs/2-plateoffset-platethick,0,zyarm+35])
        rotate([0,90,0])
        //rotate([0,0,45])
        stepper();

        translate([xyarm+xs+platethick+plateoffset*2,0,zyarm+LyPlate-36+3+0])
        rotate([0,180,0])
        z_stepper(120);

        translate([xyarm+xs+platethick+plateoffset*2,0,zyarm+LyPlate-36])
        rotate([0,0,-90])
        z_motorplate();



        translate([0,0,-85+75]){
            //_____________Z_AXIS_______________________________

            translate([xyarm+xs+platethick+plateoffset*2,0,zyarm+5])
            E1x2(La);
             translate([xyarm+xs+5+2+xs/2,0,zyarm+20])
             rotate([0,90,0])     
             rotate([0,0,90])   
            needle_mount_bottom();
                
             translate([xyarm+xs+5+2+xs/2+20,0,zyarm+20])
             rotate([0,0,180]) 
             rotate([0,90,0])     
             rotate([0,0,90])   
            needle_mount_top();
    
            translate([xyarm+xs+5+2,0,zyarm+5-6.35]) 
            rotate([0,0,-90])
            spring_support_plate();
            
            translate([xyarm+xs+5+2+xs/2,0,zyarm+5-6.35+70]) 
            rotate([0,0,90])            
            spring_support_plate_top();
                
            translate([xyarm+xs+5+2+20,0,zyarm+5-6.35-55]) 
            rotate([0,0,-90])           
            spring_plate();
            
            translate([xyarm+xs+5+2+20,-15,zyarm+5-6.35-55+6.35]) 
            cylinder(r=2,h=140);
            translate([xyarm+xs+5+2+20,15,zyarm+5-6.35-55+6.35]) 
            cylinder(r=2,h=140);
        }	
    }
}


