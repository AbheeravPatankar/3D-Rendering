int x = 320;
int y = 240;
int diameter = 25;
int i = 0;
String[] dispXYZ = new String[3];
float dispX;
float dispY;
float dispZ;

void setup(){
  
  size(640,480,P3D);
  
  
 }
void draw(){
  
  String[] dispValues = loadStrings("C:\\Users\\91878\\PycharmProjects\\MPU_PLOTS\\dispCSV.txt");
  
  background(51);


    try {
  
      dispXYZ = dispValues[i].split(",");
      dispX = Float.parseFloat(dispXYZ[0]);
      dispY = Float.parseFloat(dispXYZ[1]);
      dispZ = Float.parseFloat(dispXYZ[2]);
      
      dispX = Math.round(dispX * 100.0F)/100.0F;
      dispY = Math.round(dispY * 100.0F)/100.0F;
      dispZ = Math.round(dispZ * 100.0F)/100.0F;
      print(dispX);
      
}
    catch(Exception e) {
  
      print(dispValues[i]);
      print("\n");
      print(e);
      print("\n");
  
}
    
      translate(320 + dispX * 1000.0F,240 -  dispZ * 1000.0F, dispY * 1000.0F);
 
      background(51);   
  
      sphere(35);
      
    i++;

  
  
  
  
}
