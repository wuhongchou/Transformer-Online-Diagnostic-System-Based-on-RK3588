'''
Input:
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
class Keyclass:
    def __init__(self, h2, ch4,c2h6,c2h4,c2h2):
        self.h2 = h2
        self.ch4 = ch4
        self.c2h6=c2h6
        self.c2h4=c2h4
        self.c2h2=c2h2

    def Keyrun(self):    
       t=self.h2+self.ch4+self.c2h2+self.c2h6+self.c2h4
       pr1=self.h2/t 
       pr2=self.ch4/t
       pr3=self.c2h6/t
       pr4=self.c2h4/t
       pr5=self.c2h2/t
       result=[]
       for i in range(len(pr1)):
            P1=pr1[i]*100
            P2=pr2[i]*100
            P3=pr3[i]*100
            P4=pr4[i]*100
            P5=pr5[i]*100
            if P1>=55 and P5<= 1 :
               key=1
            elif  P5>=7 and P5<=50 and P4>=10 and P4<=58 and P3<=6:  
               key=3
            elif    (P5>=5 and P3<=9) | (P5>50): 
               key=2
            elif ( P4<=100  and P3>=1 and P4>=23 and P5<=5 and P2<=35 and P2>=5  ) | (P4>68):
               key=6
            elif  ( P4<=68  and P3<=32 and P3>=4.6 and P4>=10 and P5<=1.05  and P2<=55.22 and P2>=1.7  ) | (P2>40):
               key=5
            elif  P3>=0.01:
               key=4
            else :
               key=7
            result.append(key)
       return result
    
     
