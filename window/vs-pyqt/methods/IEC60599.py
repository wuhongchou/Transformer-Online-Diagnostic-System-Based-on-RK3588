'''
%Input:
%------
%The input is the gas concentrations stored in a vector named 'ppms' 
%and stored again in the following nine variables:
%h2=ppms(1);ch4=ppms(2);c2h6=ppms(3);c2h4=ppms(4);c2h2=ppms(5);
%co=ppms(6);co2=ppms(7);n2=ppms(8);o2=ppms(9);
%Note that unused gas concentrations take the value -1

% Analysis
%---------
% Implement your fault diagnosis method here 

%Output:
%-------
% set 'Diagnosis' variable to a number between 0 and 7 representing the 
% fault code resulting from your analysis method 
% {0=NF,1=PD,2=D1,3=D2,4=T1,5=T2,6=T3,7=UD}
'''


class IEC60599class:
    def __init__(self, h2, ch4,c2h6,c2h4,c2h2):
        self.h2 = h2
        self.ch4 = ch4
        self.c2h6=c2h6
        self.c2h4=c2h4
        self.c2h2=c2h2

    def IEC60599run(self):
     
     a1=self.c2h2/self.c2h4
     a2=self.ch4/self.h2
     a3=self.c2h4/self.c2h6
     
     result=[]
     for i in range(len(a1)):
         R1=a1[i]
         R2=a2[i]
         R3=a3[i]
         if R1<0.1:
            R1C=0
         elif R1<=3 and R1>=0.1:
            R1C=1
         elif R1>3:
            R1C=2
         
         if R2<0.1:
            R2C=1
         elif R2>=0.1 and R2<=1:
            R2C=0
         elif R2>1:
            R2C=2
      
         if R3<1:
            R3C=0
         elif R3>=1 and R3<=3:
            R3C=1
         elif R3>3:
            R3C=2
         
         
         #%1
         if R1C==0 and R2C==0 and R3C==0 :
            NO_OF_STATE=1
         #%3
         elif R1C==0 and R2C==1 and R3C==0 :
            NO_OF_STATE=3
         #%4
         elif R1C==1 and R2C==1 and R3C==0 :
            NO_OF_STATE=3
         #%5
         elif R1C==2 and R2C==0 and (R3C==1 | R3C==2) :
            NO_OF_STATE=10
         elif R1C==1 and R2C==0 and R3C==1  :
            NO_OF_STATE=10
         #%6
         elif R1C==1 and R2C==0 and R3C==2 : 
            NO_OF_STATE=12
         #%7
         elif R1C==0 and R2C==0 and R3C==1 : 
            NO_OF_STATE=4
         #%8
         elif R1C==0 and R2C==2 and R3C==0 :
            NO_OF_STATE=4
         #%9
         elif R1C==0 and R2C==2 and R3C==1 :
            NO_OF_STATE=7
         #%10
         elif R1C==0 and R2C==2 and R3C==2 :
            NO_OF_STATE=9
         else :
            NO_OF_STATE=2; 
         
         
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
         else:
            Diagnosis=0
         result.append(Diagnosis)
     return result