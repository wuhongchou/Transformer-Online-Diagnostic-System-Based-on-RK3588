   
class Rogers4class:
    def __init__(self, h2, ch4,c2h6,c2h4,c2h2):
        self.h2 = h2
        self.ch4 = ch4
        self.c2h6=c2h6
        self.c2h4=c2h4
        self.c2h2=c2h2

    def Rogers4run(self):
         a1=self.ch4/self.h2
         a2=self.c2h6/self.ch4
         a3=self.c2h4/self.c2h6
         a4=self.c2h2/self.c2h4
         result=[]
         for i in range(len(a1)):
            R1=a1[i]
            R2=a2[i]
            R3=a3[i]
            R4=a4[i]
            if R1<0.1:
             R1C=3
            elif R1<1 and R1>=0.1:
             R1C=0
            elif R1>=1 and R1<=3:
               R1C=1
            else:
               R1C=2
   
            if R2<1:
             R2C=0
            elif R2>=1:
               R2C=1
      
            if R3<1:
             R3C=0
            elif R3<=3 and R3>=1:
             R3C=1
            elif R3>3:
               R3C=2
         
            if R4<0.5:
               R4C=0
            elif R4<=3 and R4>=0.5:
               R4C=1
            elif R4>3:
             R4C=2
      
      
            # %1
            if R1C==0 and R2C==0 and R3C==0 and R4C==0:
               NO_OF_STATE=1
            # %3
            elif R1C==3 and R2C==0 and R3C==0 and R4C==0:
             NO_OF_STATE=3
            # %4
            elif (R1C==1 | R1C==2)and R2C==0 and R3C==0 and R4C==0:
               NO_OF_STATE=4
            # %5
            elif (R1C==1 |R1C==2) and R2C==1 and R3C==0 and R4C==0:
               NO_OF_STATE=5
            # %6
            elif R1C==0 and R2C==1 and R3C==0 and R4C==0:
               NO_OF_STATE=6
            # %7
            elif R1C==0 and R2C==0 and R3C==1 and R4C==0:
               NO_OF_STATE=7
            # %8
            elif R1C==1 & R2C==0 and R3C==1 and R4C==0:
             NO_OF_STATE=8
            # %9
            elif R1C==1 and R2C==0 and R3C==2 and R4C==0:
               NO_OF_STATE=9
            #%10
            elif R1C==0 and R2C==0 and R3C==0 and R4C==1:
               NO_OF_STATE=10
            # %11
            elif R1C==0 and R2C==0 and (R3C==1 | R3C==2) and (R4C==1 | R4C==2):
               NO_OF_STATE=11
            # %12
            elif R1C==0 and R2C==0 and R3C==2 and R4C==2:
               NO_OF_STATE=12
            # %13
            elif R1C==3 and R2C==0 and R3C==0 and (R4C==1 | R4C==2):
             NO_OF_STATE=13
            else :
               NO_OF_STATE=2
      
      
            if NO_OF_STATE==1:
               Diagnosis=0
            elif NO_OF_STATE==2:
               Diagnosis=7
            elif NO_OF_STATE==3:
               Diagnosis=1
            elif NO_OF_STATE==4:
               Diagnosis=4
            elif NO_OF_STATE==5:
               Diagnosis=4
            elif NO_OF_STATE==6:
               Diagnosis=4
            elif NO_OF_STATE==7:
               Diagnosis=5
            elif NO_OF_STATE==8:
               Diagnosis=5
            elif NO_OF_STATE==9:
               Diagnosis=6
            elif NO_OF_STATE==10:
               Diagnosis=2
            elif NO_OF_STATE==11:
               Diagnosis=3
            elif NO_OF_STATE==12:
               Diagnosis=3
            elif NO_OF_STATE==13:
               Diagnosis=1
            result.append(Diagnosis)
         return result